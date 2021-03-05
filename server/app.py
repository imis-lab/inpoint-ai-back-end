from fastapi import FastAPI
from server.routes.event import router as EventRouter

app = FastAPI()

app.include_router(EventRouter, tags=['Event'], prefix='/events')

@app.get('/', tags=['Root'])
async def read_root():
    return {'message': 'Welcome to this fantastic app!'}


@app.get('/summarization', tags=['Root'])
async def summarize():
    # Load all required models.
    en_nlp, el_nlp, lang_det = load_models()

    # Connect to the database.
    try:
        database = Neo4jDatabase(config.uri, config.username, config.password)
        graph = Graph(config.uri, auth = (config.username, config.password))
    except ServiceUnavailable as error: # The Neo4j server is unavailable.
        print('\t* Neo4j database is unavailable.')
        print('\t* Please check the database connection before running this script.')
        sys.exit(1)

    # Create node groups and edges from the json file.
    node_groups, edges = create_node_groups_edges(
        config.input_path, config.node_types, config.fields)

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

    # Return the summarization json object.
    return summarize_communities(database, en_nlp, el_nlp, lang_det,
                                 config.top_n, config.top_sent)

