import sys
import ai.config as config

from py2neo import Graph
from neo4j import ServiceUnavailable

from ai.neo4j_wrapper import Neo4jDatabase
from ai.graph_algos import GraphAlgos
from ai.delete import delete_discourse_graph
from ai.utils import Models, counter
from ai.select import summarize_communities
from ai.create import (
    create_node_groups_edges,
    create_discourse_graph,
    create_similarity_graph
)


def add_discourses(discourses):
    # Load all required models.
    en_nlp, el_nlp, lang_det = Models.load_models()

    # Connect to the database.
    try:
        database = Neo4jDatabase(config.uri, config.username, config.password)
        graph = Graph(config.uri, auth = (config.username, config.password))
    except ServiceUnavailable as error: # The Neo4j server is unavailable.
        print('\t* Neo4j database is unavailable.')
        print('\t* Please check the database connection before running this script.')
        # FIXME: Raise an exception instead.
        sys.exit(1)

    for discourse in discourses:
        # Create node groups and edges from the json file.
        node_groups, edges = create_node_groups_edges(
            discourse, config.node_types, config.fields)

        # Delete the entire discourse graph.
        exists = delete_discourse_graph(database, node_groups)
        if not exists: return # If the discource is empty, return early.

        # Create the discourse graph in the Neo4j Database.
        create_discourse_graph(graph, node_groups, edges, config.fields)

        # Create the similarity graph.
        create_similarity_graph(graph, node_groups, edges,
                                config.node_types, config.fields,
                                en_nlp, el_nlp, lang_det, config.cutoff)

        # Calculate the community score for the similarity graph.
        with GraphAlgos(database, ['Node'], ['is_similar']) as graph:
            graph.louvain(write_property = 'community')

        # Summarization debug.
        for id, item in summarize_communities(database, en_nlp, el_nlp, lang_det,
                                              config.top_n, config.top_sent).items():
            print(f'{id}: {item[0]}\n')
            print(f'{id}: {item[1]}\n')
            print(f'{id}: {item[2]}\n')
            print(f'{id}: {item[3]}\n\n')