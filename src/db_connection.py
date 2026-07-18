import mysql.connector
import pandas as pd


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tiwari",
        database="insightai_db"
    )


def load_data_from_mysql():

    connection = get_connection()

    query = "SELECT * FROM sales"

    df = pd.read_sql(query, connection)

    connection.close()

    return df