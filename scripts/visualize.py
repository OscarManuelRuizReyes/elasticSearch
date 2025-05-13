import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch

def generate_visualizations():
    # Usando el cloud_id proporcionado
    cloud_id = "Steam:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDM4YWRkMjYyYTI3MTQ1OWY4MDQ2M2QxNGNlN2MzYWQyJGY1MTMyYmFjNDVmMzQwMmZiNjg0OGEwYmNiYjFmMjFm"
    password = os.environ.get('ELASTIC_PASSWD')  # Obtiene la contraseña del entorno
    
    # Conexión a Elasticsearch usando el cloud_id
    es = Elasticsearch(
        cloud_id=cloud_id,
        basic_auth=("elastic", password)  # Usuario 'elastic' y la contraseña configurada
    )
    
    try:
        # Obtener datos
        response = es.search(index="titanic", body={"size": 1000, "query": {"match_all": {}}})
        hits = response['hits']['hits']
        
        if not hits:
            print("No data found in 'titanic' index")
            return
            
        df = pd.DataFrame([hit['_source'] for hit in hits])
        
        # Asegurarse de que el orden de las categorías de obesidad esté correcto
        obesidad_order = ['Normal', 'Sobrepeso', 'Obesidad grado 1', 'Obesidad mórbida']
        df['Nivel de Obesidad'] = pd.Categorical(df['Nivel de Obesidad'], categories=obesidad_order, ordered=True)
        
        # Gráfico 1: Relación entre el peso y el nivel de depresión
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Peso', y='Nivel de Depresión', data=df, hue='Nivel de Obesidad', palette='coolwarm', s=100, alpha=0.6)
        plt.title('Relación entre el Peso y el Nivel de Depresión')
        plt.xlabel('Peso (kg)')
        plt.ylabel('Nivel de Depresión')
        plt.legend(title='Nivel de Obesidad', loc='upper left')
        plt.tight_layout()
        plt.savefig('docs/visualizations.png')
        plt.show()

        # Gráfico 2: Distribución del nivel de depresión por nivel de obesidad
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Nivel de Obesidad', y='Nivel de Depresión', data=df, palette='Set2')
        plt.title('Nivel de Depresión por Nivel de Obesidad')
        plt.xlabel('Nivel de Obesidad')
        plt.ylabel('Nivel de Depresión')
        plt.tight_layout()
        plt.show()

        # Gráfico 3: Relación entre horas de sueño y nivel de obesidad
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Nivel de Obesidad', y='Horas de Sueño', data=df, palette='Set3')
        plt.title('Relación entre Horas de Sueño y Nivel de Obesidad')
        plt.xlabel('Nivel de Obesidad')
        plt.ylabel('Horas de Sueño')
        plt.tight_layout()
        plt.show()

        # Gráfico 4: Actividad física según nivel de obesidad
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Nivel de Obesidad', hue='Actividad Física', data=df, palette='Pastel1')
        plt.title('Actividad Física según Nivel de Obesidad')
        plt.xlabel('Nivel de Obesidad')
        plt.ylabel('Número de Personas')
        plt.tight_layout()
        plt.show()

        # Guardar gráficos en docs/
        output_dir = os.path.join(os.getcwd(), 'docs')
        os.makedirs(output_dir, exist_ok=True)

        print(f"✅ Visualizaciones generadas y guardadas en {output_dir}/visualizations.png")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise  # Esto hará que el workflow falle claramente

if __name__ == "__main__":
    generate_visualizations()
