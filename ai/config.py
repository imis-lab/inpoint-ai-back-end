# Initial Setup
input_path = r'C:\Users\Nick\Desktop\example.json'
debug = True


# Connection data
uri = 'bolt://localhost:7687'
username = 'neo4j'
password = '123'


# Supported data types
node_types = ['Issue', 'Solution', 'Note', 'Position-against', 'Position-in-favor']
fields = ['author', 'date', 'dislikes', 'id', 'likes', 'text']


# Algorithmic values
cutoff = 0.5
top_n = 10
top_sent = 5

