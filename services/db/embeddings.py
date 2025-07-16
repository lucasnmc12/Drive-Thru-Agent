import os
import psycopg2
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

load_dotenv()

def conectar():
    url = os.getenv("DATABASE_URL")
    if url.startswith("psql '") and url.endswith("'"):
        url = url[6:-1]
    return psycopg2.connect(url)

# carregar modelo de embeddings
modelo = SentenceTransformer('all-MiniLM-L6-v2')

#Conectar
conn = conectar()
# Registrar suporte ao tipo vector do pgvector
register_vector(conn)

cursor = conn.cursor()


cursor.execute("SELECT id, nome, descricao, preco FROM produtos")
produtos = cursor.fetchall()

# Verifica e cria coluna 'embedding' se necessário
cursor.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name='produtos' AND column_name='embedding'
        ) THEN
            ALTER TABLE produtos ADD COLUMN embedding vector(384);
        END IF;
    END
    $$;
""")
conn.commit()

# buscar produtos
cursor.execute("SELECT id, nome, descricao, preco FROM produtos")
produtos = cursor.fetchall()

for id, nome, descricao, preco in produtos:
    texto = f"{nome}. {descricao}. Preço: R${preco:.2f}"
    vetor = modelo.encode(texto)
    cursor.execute(
        "UPDATE produtos SET embedding = %s WHERE id = %s",
          (vetor.tolist(), id)
          )

conn.commit()
cursor.close()
conn.close()

print("✅ Embeddings gerados e inseridos com sucesso!")
