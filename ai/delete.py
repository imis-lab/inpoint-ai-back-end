def delete_discourse_graph(database, node_groups):
    """
    Function that deletes a discourse subgraph in the database,
    if it exists, and returns whether it exists or not.
    """
    # Find all unique ids of the discourse subgraph.
    node_ids = list({
        node['id'] 
        for node_group in node_groups.values() 
        for node in node_group
    })

    # If the discource is empty, return early.
    if not node_ids: return False

    query = f"""UNWIND {node_ids} as node_id 
            MATCH (n {{id: node_id}})-[r]-()
            DELETE r, n"""
    database.execute(query, 'w')
    return True

