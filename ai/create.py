import json
from bs4 import BeautifulSoup
from py2neo.bulk import merge_nodes, merge_relationships
from ai.similarity import calc_similarity_pairs
from ai.utils import counter

@counter
def create_node_groups_edges(discourse, node_types, fields):
    """
    Function that creates the node groups, and edges
    in-memory objects from the json document.
    """
    # This dictionary separates different types of nodes.
    node_groups = {
        k: [] 
        for k in node_types
    }

    # This list holds all edges.
    edges = [
        (edge['sourceId'],
         {},
        edge['targetId'])
        for edge in discourse['edges']
    ]

    # Iterate all nodes found in the discourse json.
    for node in discourse['nodes']:

        # Find the type of the label, if it exists.
        label = node.get('type')

        if label is not None:
            label = label.capitalize()
            node_groups[label].append({
               field: node.get(field)
               for field in fields
            })

            # Remove all html tags from text.
            node_groups[label][-1]['text'] = \
                BeautifulSoup(node_groups[label][-1]['text'], 
                              features = 'html.parser').get_text()
       
    return (node_groups, edges)

@counter
def create_discourse_graph(database, node_groups, edges, fields):
    """
    Function that creates a discourse subgraph in the database.
    """
    # Create a unique constraint and merge all nodes of each node group.
    for label, nodes in node_groups.items():
        try:
            database.schema.create_uniqueness_constraint(label, 'id')
        except:
            pass
        if nodes: # Merge nodes, if they are not empty.
            merge_nodes(database.auto(), nodes, (label, *fields), labels = {'Node', label})

    # Merge all relationships, depending on source, target id, if they are not empty.
    if edges:
        merge_relationships(
                database.auto(), edges, 'connects', 
                start_node_key = ('Node', 'id'), end_node_key = ('Node', 'id'))

    return

@counter
def create_similarity_graph(database, node_groups, edges, node_types, fields, 
                            en_nlp, el_nlp, lang_det, cutoff):
    """
    Function that creates the similarity subgraph in the database,
    based on the existing discourse graph.
    """
    
    # This dictionary separates different types of nodes.
    # This part assumes that there is only one issue node.
    # That's the reason we skip it.

    node_groups_similarity_pairs = {
        k: [] 
        for k in [
            node_type
            for node_type in node_types
            if node_type != 'Issue'
        ]
    }

    # Calculate all node groups similarity pairs.
    for label, nodes in node_groups.items():
        if label == 'Issue':
            continue

        # Create the list of texts and ids for all nodes of a specific type.
        text_ids = [(node['id'], node['text']) for node in nodes]

        # We need at least two texts to make the comparison.
        if len(text_ids) < 2:
            continue
        else:
            edges = \
                calc_similarity_pairs(text_ids, en_nlp, el_nlp, lang_det, cutoff)

            # Convert the similarity score to a dict, for the call below.
            edges = [(source, {'score': score}, target) for source, score, target in edges]

            # Merge all relationships, depending on source, target id, if they exist.
            if edges:
                merge_relationships(
                    database.auto(), edges, merge_key = ('is_similar', 'score'),
                    start_node_key = ('Node', 'id'), end_node_key = ('Node', 'id'))

    return
