import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar o arquivo atualizado
df = pd.read_csv("ubs_atualizado.csv", sep=";")

df["LATITUDE"] = df["LATITUDE"].str.replace(",", ".").astype(float)
df["LONGITUDE"] = df["LONGITUDE"].str.replace(",", ".").astype(float)

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
else:
    df_filtrado = df  # Exibir todos os estados se nenhum for selecionado


# Criar o mapa de dispersão
st.subheader("Mapa das Unidades Básicas de Saúde")

fig_mapa = px.scatter_map(df_filtrado, 
                             lat="LATITUDE", 
                             lon="LONGITUDE", 
                             hover_name="NOME", 
                             hover_data={"Nome_Município": True, "Nome_UF": True, "LATITUDE": False, "LONGITUDE": False},
                             color_discrete_sequence=["red"], 
                             zoom=4, 
                             height=500)

# Configurar mapa com estilo
fig_mapa.update_layout(mapbox_style="open-street-map", 
                       mapbox_center={"lat": df["LATITUDE"].mean(), "lon": df["LONGITUDE"].mean()})

st.plotly_chart(fig_mapa)
st.subheader("Lista de todas as UBS do país")
st.write(df)
