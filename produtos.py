import sqlite3

def cadastrar_produto(nome, duracao):
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO produtos (nome, duracao) 
        VALUES (?, ?)
    ''', (nome, duracao))

    conn.commit()
    conn.close()

def listar_produtos():
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nome, duracao FROM produtos')
    produtos = cursor.fetchall()

    conn.close()
    return produtos

def excluir_produto(produto_id):
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    # Exclui todas as compras associadas ao produto
    cursor.execute('DELETE FROM compras WHERE produto_id = ?', (produto_id,))

    # Exclui o produto em si
    cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))

    conn.commit()
    conn.close()

    print(f"Produto ID {produto_id} e suas compras associadas foram excluídos com sucesso.")

def alterar_duracao(produto_id, nova_duracao):
    conn = sqlite3.connect('controle_compras.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE produtos SET duracao = ? WHERE id = ?
    ''', (nova_duracao, produto_id))

    conn.commit()
    conn.close()

    print(f"Duração do produto ID {produto_id} atualizada para {nova_duracao} dias.")