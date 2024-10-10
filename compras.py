import sqlite3
from datetime import datetime, timedelta

def registrar_compra(produto_nome, data_compra):
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    # Primeiro, obtenha o ID do produto usando o nome
    cursor.execute('SELECT id FROM produtos WHERE nome = ?', (produto_nome,))
    produto = cursor.fetchone()

    if produto:
        produto_id = produto[0]
        cursor.execute('''INSERT INTO compras (produto_id, data_compra) VALUES (?, ?)''', (produto_id, data_compra))
        conn.commit()
    else:
        print("Produto não encontrado.")

    conn.close()

def listar_compras():
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, produto_id, data_compra FROM compras')
    compras = cursor.fetchall()

    conn.close()
    return compras

def excluir_compra(compra_id):
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    # Exclui a compra pelo ID
    cursor.execute('DELETE FROM compras WHERE id = ?', (compra_id,))

    conn.commit()
    conn.close()

    print(f"Compra ID {compra_id} foi excluída com sucesso.")

def calcular_validade(produto_id):
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT c.data_compra, p.duracao FROM compras c
        JOIN produtos p ON c.produto_id = p.id
        WHERE p.id = ?
        ORDER BY c.id DESC LIMIT 1
    ''', (produto_id,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        data_compra_str, duracao = resultado
        data_compra = datetime.strptime(data_compra_str, '%Y-%m-%d')
        validade = data_compra + timedelta(days=duracao)
        alerta = validade - timedelta(days=2)
        return validade, alerta
    else:
        return None, None