from decouple import config


# Initial Setup
debug = config('AI_BACKEND_DEBUG', cast=bool)


# Connection data
BOLT_PORT = config('NEO4J_BOLT_PORT', cast=int)
NEO4J_URL = config('NEO4J_URL')
uri = f'bolt://{NEO4J_URL}:{BOLT_PORT}'
username = 'neo4j'
password = config('NEO4J_INITDB_ROOT_PASSWORD')


# Supported data types
node_types = ['Issue', 'Solution', 'Note', 'Position-against', 'Position-in-favor']
fields = ['authorId', 'dislikes', 'id', 'likes', 'text']


# Algorithmic values
cutoff = 0.5
top_n = 10
top_sent = 5