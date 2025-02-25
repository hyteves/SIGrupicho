import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar o arquivo atualizado
df = pd.read_csv("ubs_atualizado.csv", sep=";")

# Contar a frequência de UBS por estado
df_freq = df['Nome_UF'].value_counts().reset_index()
df_freq.columns = ['Estado', 'Frequência']

# Criar o dashboard
st.title("Dashboard de Unidades Básicas de Saúde (UBS)")

# Gráfico de barras
grafico = px.bar(df_freq, x='Estado', y='Frequência', 
                 title='Frequência de UBS por Estado', 
                 labels={'Estado': 'Estado', 'Frequência': 'Número de UBS'},
                 text_auto=True)

st.plotly_chart(grafico)

# Filtro para estados específicos
estados = st.multiselect("Selecione os estados para tabela", df_freq['Estado'].unique(), key="multiselect_tabela")
if estados:
    df_filtrado = df[df['Nome_UF'].isin(estados)]
    st.write(df_filtrado)

# Filtro para estados específicos (para o mapa)
estados_mapa = st.multiselect("Selecione os estados para mapa", df_freq['Estado'].unique(), key="multiselect_mapa")
if estados_mapa:
    df_filtrado_mapa = df[df['Nome_UF'].isin(estados_mapa)]

    # Mapa de dispersão para localização das UBS
    mapa = px.scatter_geo(df_filtrado_mapa, lat='LATITUDE', lon='LONGITUDE', hover_name='Nome_UF', 
                      title='Localização das UBS Selecionadas',
                      scope='south america', 
                      labels={'Nome_UF': 'Estado'})
    mapa.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")
    st.plotly_chart(mapa)
else:
    st.write("Selecione um ou mais estados para visualizar as UBS no mapa.")
