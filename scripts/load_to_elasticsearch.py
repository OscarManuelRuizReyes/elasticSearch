from elasticsearch import Elasticsearch
import pandas as pd
import os
import math

def load_data():
    # Utiliza el cloud_id que has proporcionado
    cloud_id = "Steam:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDM4YWRkMjYyYTI3MTQ1OWY4MDQ2M2QxNGNlN2MzYWQyJGY1MTMyYmFjNDVmMzQwMmZiNjg0OGEwYmNiYjFmMjFm"
    password = os.environ.get('ELASTIC_PASSWD')  # Obtiene la contraseña del entorno
    
    # Conexión a Elasticsearch usando el cloud_id
    es = Elasticsearch(
        cloud_id=cloud_id,
        basic_auth=("elastic", password)  # Usuario 'elastic' y contraseña
    )

    # Cargar datos y limpiar NaN
    df = pd.read_csv("data/Titanic-Dataset.csv").fillna("")  # Reemplaza NaN con strings vacíos
    
    # Convertir a JSON y limpiar valores numéricos NaN
    records = []
    for _, row in df.iterrows():
        record = row.to_dict()
        # Limpieza adicional para NaN en floats/ints
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = None  # O usar "" si prefieres strings
        records.append(record)
    
    # Indexar en Elasticsearch
    for i, record in enumerate(records):
        es.index(index="titanic", id=i+1, document=record)

    print(f"✅ Datos cargados: {len(records)} registros en índice 'titanic'")

if __name__ == "__main__":
    load_data()
