import pandas as pd
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch

def generate_visualizations():
    cloud_id = os.environ.get('ELASTIC_ID')
    password = os.environ.get('ELASTIC_PASSWD')
    
    es = Elasticsearch(
        cloud_id=cloud_id,
        basic_auth=("briceno", password)
    )
    
    try:
        # Obtener datos
        response = es.search(index="titanic", body={"size": 1000, "query": {"match_all": {}}})
        hits = response['hits']['hits']
        
        if not hits:
            print("No data found in 'titanic' index")
            return
            
        df = pd.DataFrame([hit['_source'] for hit in hits])
        
        # Limpieza de tipos de datos
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')  # Convierte a float
        df['Fare'] = pd.to_numeric(df['Fare'], errors='coerce')
        df['Pclass'] = pd.to_numeric(df['Pclass'], errors='coerce')
        df['Survived'] = pd.to_numeric(df['Survived'], errors='coerce')
        
        # Eliminar filas con valores faltantes críticos
        df = df.dropna(subset=['Age', 'Pclass', 'Survived'])
        
        print("Datos limpios:")
        print(df.dtypes)  # Verifica los tipos de datos
        
        # Configuración mejorada para las gráficas
        plt.figure(figsize=(14, 6))  # Aumenta el ancho total
        plt.subplots_adjust(wspace=0.4, hspace=0.6)  # Ajusta espacios horizontales y verticales
        
        # Gráfico 1: Supervivencia por clase (izquierda)
        plt.subplot(1, 2, 1)  # 1 fila, 2 columnas, posición 1
        df.groupby(['Pclass', 'Survived']).size().unstack().plot(
            kind='bar',
            stacked=True,
            color=['#ff9999','#66b3ff']  # Colores personalizados
        )
        plt.title('Supervivencia por Clase', pad=20)  # pad añade espacio al título
        plt.xlabel('Clase')
        plt.ylabel('Cantidad')
        plt.legend(['No Sobrevivió', 'Sobrevivió'], bbox_to_anchor=(1.05, 1))  # Leyenda fuera del gráfico
        
        # Gráfico 2: Distribución de edades (derecha)
        plt.subplot(1, 2, 2)  # 1 fila, 2 columnas, posición 2
        df['Age'].hist(bins=20, color='#99ff99', edgecolor='black')
        plt.title('Distribución de Edades', pad=20)
        plt.xlabel('Edad')
        plt.ylabel('Frecuencia')

        # Ajustes finales
        plt.tight_layout(pad=3.0)  # Añade padding general
        
        # Guardar gráficos
        output_dir = os.path.join(os.getcwd(), 'docs')
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'visualizations.png'), dpi=120, bbox_inches='tight')
        print(f"✅ Imagen guardada en: {os.path.abspath(os.path.join(output_dir, 'visualizations.png'))}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise  # Esto hará que el workflow falle claramente

if __name__ == "__main__":
    generate_visualizations()
