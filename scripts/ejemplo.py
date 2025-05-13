from elasticsearch import Elasticsearch

# Conexión a Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Verificar conexión
if es.ping():
    print("Conectado a Elasticsearch")
else:
    print("No se pudo conectar a Elasticsearch")