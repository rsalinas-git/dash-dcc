import streamlit as st
import pandas as pd
import plotly.express as px


# Definimos los parámetros de configuración de la aplicación
st.set_page_config(
    page_title="Dashboard DCC 2025", #Título de la página
    page_icon="📊", # Ícono
    layout="wide", # Forma de layout ancho o compacto
    initial_sidebar_state="expanded" # Definimos si el sidebar aparece expandido o colapsado
)

#TITULO PRINCIPAL DEL DASHBOARD *******************
st.title('Departamento de Ciencias de la Computación - Universidad de Cuenca')

# VISTA GENERAL DE LOS RESULTADOS **************
st.header('Estadísticas Generales')

# Cargamos el dataframe desde un CSV
dfDatos = pd.read_csv('DBDCC25.csv', sep=';', encoding='latin-1')
dfDatos['indexacion'] = dfDatos['indexacion'].replace(['', 'N/A', 'None', ' '], 'Por definir') # Replace all these with "Por definir"

# PUBLICACIONES POR AÑO ----------------

df_publications_per_year = dfDatos.groupby('anio_publicacion').size().reset_index(name='Publicaciones')
df_publications_per_year.rename(columns={'anio_publicacion': 'Año'}, inplace=True)
fig = px.bar(df_publications_per_year, x='Año', y='Publicaciones', title='Total de Publicaciones',color='Año',text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# TIPO DE PUBLICACIÓN ----------------
# # métricas en números
# publication_types = dfDatos["tipo_publicacion"].unique()
# for pub_type in publication_types:
#     count = len(dfDatos[dfDatos["tipo_publicacion"] == pub_type])
#     st.metric(f"Publications ({pub_type})", count)

publication_types = dfDatos["tipo_publicacion"].value_counts().reset_index(name='Publicaciones')
publication_types.columns = ['Publicaciones', 'Cantidad']  # Rename columns for clarity

fig_pub_types = px.bar(
    publication_types, 
    x='Publicaciones', 
    y='Cantidad', 
    title='Cantidad de Publicaciones por Tipo',
    color='Publicaciones',  # Color bars by publication type
    text_auto=True  # Show counts on top of bars
)
st.plotly_chart(fig_pub_types, use_container_width=True)

# CLASIFICACION POR INDEXACION -----------------

publication_indexing = dfDatos["indexacion"].value_counts().reset_index(name='Cantidad')
publication_indexing.columns = ['Indexacion', 'Cantidad']  # Rename columns

fig_pub_indexing = px.pie(publication_indexing, names='Indexacion', values='Cantidad',
                          title='Publicaciones según Indexación')
st.plotly_chart(fig_pub_indexing, use_container_width=True)


# CLASIFICACION POR AREA DE CONOCIMIENTO (BETA) -------------------
def classify_publication(title):
    title = title.lower()  # Lowercase for consistency

    if any(keyword in title for keyword in ["ingeniería", "tecnología", "arquitectura", "agropecuari", "agronom", "software", "hardware", "redes", "sistemas"]):
        return "Ingenierías, Tecnologías, Arquitectura, y Agropecuarias"
    elif any(keyword in title for keyword in ["social", "periodismo", "información", "derecho", "comunicación", "leyes"]):
        return "C. Sociales, Periodismo, Información y Derecho"
    elif any(keyword in title for keyword in ["administración", "servicio", "marketing", "gestión", "empresa", "negocio", "finanzas"]):
        return "Administración y Servicios"
    elif any(keyword in title for keyword in ["educación", "arte", "humanidad", "literatura", "historia", "filosofía", "música"]):
        return "Educación, Artes y Humanidades"
    else:
        return "TICs"  # Default category if no keywords match

# Nueva columna de acuerdo con la clasificación
dfDatos['area_conocimiento'] = dfDatos['titulo'].apply(classify_publication)

# Conteo según area de conocimiento y graficar
area_counts = dfDatos.groupby('area_conocimiento').size().reset_index(name='count')
fig_area = px.pie(area_counts, names='area_conocimiento', values='count',
                          title='Publicaciones por Área de Conocimiento (check)',color="area_conocimiento")
st.plotly_chart(fig_area, use_container_width=True)

# PUBLICACIONES SEGUN DOCENTE-INVESTIGADOR --------------

publications_by_author = dfDatos.groupby('autores').size().reset_index(name='Publicaciones')

# Sort by publications (descending)
publications_by_author_sorted = publications_by_author.sort_values('Publicaciones', ascending=False)

# Display using a bar chart
fig_publications_by_author = px.bar(
    publications_by_author_sorted, 
    y='autores',  # Authors on the y-axis for better readability with long names
    x='Publicaciones',  # Publication count on the x-axis
    orientation='h',  # Horizontal bar chart
    title='Publicaciones por Autor (check)',
    color='Publicaciones',
    labels={'autores': 'Autor', 'Publicaciones': 'Número de Publicaciones'},
    text_auto=True  # Show publication count labels on bars
)

st.plotly_chart(fig_publications_by_author, use_container_width=True)

st.text("Analizar opción de clasificar por Grupo de Investigación...")

# PENDIENTE ESTADÍSTICAS DE LOS PROYECTOS


#*********************************************************
#st.header(' ')

st.subheader("Análisis personalizado...")
# Declaramos los parámetros en la barra lateral
with st.sidebar:
    # Filtro de Año de publicación
    parAno=st.selectbox('Año',options=dfDatos['anio_publicacion'].unique(),index=0)
    # Filtro de  Tipo de publicación
    #parMes = st.selectbox('Tipo',options=dfDatos['tipo_publicacion'].unique(),index=0)
    # Filtro por Autor
    #parAutor = st.multiselect('Autor',options=dfDatos['autores'].unique())

    # Filtro por Autor
    parAutor = st.selectbox('Autor',options=dfDatos['autores'].unique())

# Si hay parametros seleccionados aplicamos los filtros
if parAno:
    dfSelected=dfDatos[dfDatos['anio_publicacion']==parAno]

# Mostramos las métricas
#dfAnoActual = dfDatos[dfDatos['anio_publicacion']==parAno]

# Declaramos 2 columnas en una proporción de 50% y 50%
c1,c2,c3 = st.columns(3)
with c1:
    pub_types = dfSelected['tipo_publicacion'].value_counts().reset_index(name='Count')
    fig_pub_types = px.pie(pub_types, names='tipo_publicacion', values='Count',
                          title='Publicaciones según Tipo', color='tipo_publicacion')
    st.plotly_chart(fig_pub_types, use_container_width=True)

with c2:
    pub_indexing = dfSelected['indexacion'].value_counts().reset_index(name='Count')
    fig_pub_indexing = px.pie(pub_indexing, names='indexacion', values='Count',
                          title='Publicaciones según Indexación', color='indexacion')
    st.plotly_chart(fig_pub_indexing, use_container_width=True)

with c3:
    pub_autor = dfSelected['autores'].value_counts().reset_index(name='Count')
    fig_pub_autor = px.pie(pub_autor, names='autores', values='Count',
                          title='Publicaciones según Autor', color='autores')
    st.plotly_chart(fig_pub_autor, use_container_width=True)

st.subheader("Más resultados...")


...

