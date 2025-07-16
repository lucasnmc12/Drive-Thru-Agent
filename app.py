from fastapi import FastAPI, Query
from pydantic import BaseModel
import os
import psycopg2
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv
from pgvector.psycopg2 import vector
from pgvector.psycopg2 import register_vector



load_dotenv()
app = FastAPI()

modelo = SentenceTransformer('all-MiniLM-L6-v2')

def conectar():
    url = os.getenv("DATABASE_URL")
    if url.startswith("psql '") and url.endswith("'"):
        url = url[6:-1]
    conn = psycopg2.connect(url)
    register_vector(conn)
    return conn

class Consulta(BaseModel):
    query: str
    limite: int = 3

@app.post("/search")
def busca_semantica(consulta: Consulta):
    texto = consulta.query
    limite = consulta.limite
    embedding = modelo.encode(texto)



    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, nome, descricao, preco
    FROM produtos
    ORDER BY embedding <-> (%s)::vector
    LIMIT %s
""", ([float(x) for x in embedding], limite))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    
    
    return [
        {
            "id": r[0],
            "nome": r[1],
            "descricao": r[2],
            "preco": float(r[3])
        } for r in resultados
    ]