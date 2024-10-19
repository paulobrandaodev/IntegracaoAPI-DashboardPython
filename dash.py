import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from context import get_mysql_data  # Importando do arquivo context.py

# Consulta SQL
query = "SELECT * FROM carros"

# Carregar os dados do MySQL
df = get_mysql_data(query)

# Botão para atualizar os dados
if st.button("Atualizar Dados"):
    df = get_mysql_data(query)

st.sidebar.header("Selecione o Filtro")
marca = st.sidebar.multiselect(
    "Marca Selecionada",
    options=df["marca"].unique(),
    default=df["marca"].unique(),
    key="marca"
)
modelo = st.sidebar.multiselect(
    "Modelo Selecionada",
    options=df["modelo"].unique(),
    default=df["modelo"].unique(),
    key="modelo"
)
ano = st.sidebar.multiselect(
    "Ano Selecionada",
    options=df["ano"].unique(),
    default=df["ano"].unique(),
    key="ano"
)
valor = st.sidebar.multiselect(
    "Valor Selecionada",
    options=df["valor"].unique(),
    default=df["valor"].unique(),
    key="valor"
)
cor = st.sidebar.multiselect(
    "Cor Selecionada",
    options=df["cor"].unique(),
    default=df["cor"].unique(),
    key="cor"
)
numero_Vendas = st.sidebar.multiselect(
    "Número de Vendas Selecionada",
    options=df["numero_Vendas"].unique(),
    default=df["numero_Vendas"].unique(),
    key="numero_Vendas"
)

df_selection = df.query(
    "marca==@marca & modelo==@modelo & ano==@ano & valor==@valor & cor==@cor & numero_Vendas==@numero_Vendas"
)


def Home():
    with st.expander("Tabular"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=[], key="showData_home")
        if showData:
            st.write(df_selection[showData])

    # Compute top analytics
    venda_total = df_selection["numero_Vendas"].sum()
    valor_venda_media = df_selection["numero_Vendas"].mean()
    valor_medio_carro = df_selection["numero_Vendas"].median()

    total1, total2, total3, total4 = st.columns(4, gap='large')
    with total1:
        st.info(' Valor Total da Venda dos Carros', icon='📌')
        st.metric(label="Total", value=f"{venda_total:,.0f}")

    with total2:
        st.info(' Valor Médio de Vendas', icon='📌')
        st.metric(label="Média", value=f"{valor_venda_media:,.0f}")

    with total3:
        st.info(' Valor Médio dos Carros', icon='📌')
        st.metric(label="Mediana", value=f"{valor_medio_carro:,.0f}")

    st.markdown("""-----""")


def graphs():
    if df_selection.empty:
        st.write("Nenhum dado disponível para gerar gráficos.")
        return

    # Gráfico simples de barra
    investimento = df_selection.groupby(by=["marca"]).count()[["valor"]].sort_values(by="valor", ascending=False)
    fig_valores = px.bar(
        investimento,
        x=investimento.index,
        y="valor",
        orientation="h",
        title="<b>Valores de Carros</b>",
        color_discrete_sequence=["#0083b8"],
        template="plotly_white"
    )

    fig_valores.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    # Gráfico simples de linha
    investimento_state = df_selection.groupby(by=["marca"]).count()[["valor"]]
    fig_state = px.line(
        investimento_state,
        x=investimento_state.index,
        y="valor",
        title="<b>Valores por Marca</b>",
        color_discrete_sequence=["#0083b8"],
        template="plotly_white"
    )

    fig_state.update_layout(
        xaxis=dict(showgrid=False),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False)
    )

    left, right = st.columns(2)
    with left:
        st.plotly_chart(fig_state, use_container_width=True)
    with right:
        st.plotly_chart(fig_valores, use_container_width=True)


def BarraProgresso():
    st.markdown(
        """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",
        unsafe_allow_html=True)
    target = 20000000
    current = df_selection["numero_Vendas"].sum()
    percent = round((current / target * 100))
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Valores done!")
    else:
        st.write("Você tem ", percent, "% ", "of ", format(target, 'd'), " TZS")
        for percent_complete in range(percent):
            mybar.progress(percent_complete + 1, text="Target Percentage")


def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        st.subheader(f"Page: {selected}")
        Home()
        graphs()
    if selected == "Progress":
        st.subheader(f"Page: {selected}")
        BarraProgresso()
        graphs()


hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

sideBar()
