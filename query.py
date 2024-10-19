import mysql.connector
import pandas as pd

# Função para conectar ao banco de dados MySQL e realizar consultas
def get_mysql_data(query):
    # Conecte ao MySQL
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="toor",
        db="carrosbd"
    )

    # Executar a consulta e carregar os dados
    dataframe = pd.read_sql(query, conn)

    # Fechar a conexão
    conn.close()

    return dataframe
