import json
import psycopg2
import os
from dotenv import load_dotenv

import os

load_dotenv()


def conectar():
    raw_url = os.getenv("DATABASE_URL")
    print("DEBUG (antes de limpar):", raw_url)

    # Remove prefixo "psql '" e sufixo "'" se existirem
    if raw_url.startswith("psql '") and raw_url.endswith("'"):
        raw_url = raw_url[6:-1]

    print("DEBUG (depois de limpar):", raw_url)
    return psycopg2.connect(raw_url)

def carregar_catalogo(caminho="catalogo.json"):
    with open (caminho, "r", encoding="utf-8") as f:
        return json.load(f)
    
def inserir_produtos(catalogo, conn):
    id_por_nome = {}
    cursor = conn.cursor()

    for item in catalogo:
        cursor.execute("""
        INSERT INTO produtos(nome, preco, descricao, categoria) 
            VALUES (%s, %s, %s, %s)
        RETURNING id 
                       """, (item["nome"], item["preco"], item["descricao"], item["categoria"]))
        
        produto_id = cursor.fetchone()[0]
        id_por_nome[item["nome"]] = produto_id

    conn.commit()
    return id_por_nome

def inserir_combos(catalogo, id_por_nome, conn):
    cursor = conn.cursor()

    for item in catalogo:
        if item["categoria"] != "combo":
            continue

        combo_id = id_por_nome.get(item["nome"])

        # Extrair itens da descrição
        itens_combo = item.get("itens", "")
        nomes_itens = [i.strip().rstrip(".") for i in itens_combo]

        for nome_item in nomes_itens:
            item_id = id_por_nome.get(nome_item)
            if item_id:
                cursor.execute("""
                    INSERT INTO combo_itens (combo_id, item_id)
                    VALUES (%s, %s)
                """, (combo_id, item_id))
            else:
                print(f"[AVISO] Item '{nome_item}' não encontrado para o combo '{item['nome']}'")

    conn.commit()

def main():
        conn = conectar()
        catalogo = carregar_catalogo()
        id_por_nome = inserir_produtos(catalogo, conn)
        inserir_combos(catalogo, id_por_nome, conn)
        conn.close()

        print("Dados inseridos no banco de dados")

if __name__ == "__main__":
        main()
                





