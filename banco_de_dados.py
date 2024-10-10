import sqlite3

def criar_banco():
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    # Criação da tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            duracao INTEGER NOT NULL
        )
    ''')

    # Criação da tabela de compras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            data_compra TEXT,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')

    conn.commit()
    conn.close()