import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")



def get_connection():
    return psycopg2.connect(DB_URL)

def buscar_produtos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, descricao, preco FROM produtos")
    resultados = cur.fetchall()
    cur.close()
    conn.close()

    return resultados