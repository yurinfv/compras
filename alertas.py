import sqlite3
from datetime import datetime, timedelta

def verificar_alertas():
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.nome, c.data_compra, p.duracao FROM compras c
        JOIN produtos p ON c.produto_id = p.id
    ''')
    compras = cursor.fetchall()
    conn.close()

    hoje = datetime.today()

    for nome, data_compra_str, duracao in compras:
        data_compra = datetime.strptime(data_compra_str, '%Y-%m-%d')
        validade = data_compra + timedelta(days=duracao)
        alerta = validade - timedelta(days=2)

        if hoje >= alerta and hoje < validade:
            print(f"Alerta: O produto '{nome}' vai expirar em breve!")