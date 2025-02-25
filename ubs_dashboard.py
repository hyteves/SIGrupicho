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
estados = st.multiselect("Selecione os estados", df_freq['Estado'].unique())
if estados:
    df_filtrado = df[df['Nome_UF'].isin(estados)]
    st.write(df_filtrado)

# Histograma da Quantidade de UBS por Município
# Contar a frequência de UBS por município
df_mun_freq = df['Nome_Município'].value_counts().reset_index()
df_mun_freq.columns = ['Município', 'Frequência']

# Controle deslizante para o número mínimo de UBS
num_min_ubs = st.slider("Selecione o número mínimo de UBS", min_value=1, max_value=int(df_mun_freq['Frequência'].max()), value=1)

# Filtrar municípios com pelo menos o número mínimo de UBS
df_mun_filtrado = df_mun_freq[df_mun_freq['Frequência'] >= num_min_ubs]

# Criar histograma
grafico_histograma = px.histogram(df_mun_filtrado, x='Município', y='Frequência',
                                  title='Quantidade de UBS por Município',
                                  labels={'Município': 'Município', 'Frequência': 'Número de UBS'},
                                  text_auto=True)

st.plotly_chart(grafico_histograma)