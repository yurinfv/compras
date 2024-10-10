import tkinter as tk
from tkinter import messagebox, ttk
from produtos import cadastrar_produto, excluir_produto, alterar_duracao, listar_produtos
from compras import registrar_compra, excluir_compra, listar_compras, calcular_validade

def registrar_produto_janela():
    janela = tk.Toplevel(root)
    janela.title("Registrar Produto")
    janela.geometry("400x200")  # Aumente a largura da janela

    tk.Label(janela, text="Nome do Produto:").pack(pady=10)
    entrada_nome = tk.Entry(janela, width=30)
    entrada_nome.pack()

    tk.Label(janela, text="Duração (dias):").pack(pady=10)
    entrada_duracao = tk.Entry(janela, width=30)
    entrada_duracao.pack()

    # Modifique o comando do botão para fechar a janela após o registro
    tk.Button(janela, text="Registrar", command=lambda: (
        cadastrar_produto(entrada_nome.get(), entrada_duracao.get()),
        janela.destroy()
    )).pack(pady=20)

def registrar_compra_janela():
    janela = tk.Toplevel(root)
    janela.title("Registrar Compra")
    janela.geometry("400x200")  # Aumente a largura da janela

    tk.Label(janela, text="Selecione o Produto:").pack(pady=10)
    produtos = listar_produtos()
    combo_produto = ttk.Combobox(janela, values=[p[1] for p in produtos], width=30)  # Aumente a largura da combobox
    combo_produto.pack()

    tk.Label(janela, text="Data da Compra (YYYY-MM-DD):").pack(pady=10)
    entrada_data = tk.Entry(janela, width=30)
    entrada_data.pack()

    tk.Button(janela, text="Registrar", command=lambda: (
        registrar_compra(combo_produto.get(), entrada_data.get()),
        janela.destroy()  # Fecha a janela após registrar
    )).pack(pady=20)

def excluir_compra_janela():
    janela = tk.Toplevel(root)
    janela.title("Excluir Compra")
    janela.geometry("400x200")  # Aumente a largura da janela

    tk.Label(janela, text="Selecione a Compra:").pack(pady=10)
    compras = listar_compras()
    
    # Montando os valores da combobox com o nome do produto e a data da compra
    combo_compra = ttk.Combobox(
        janela, 
        values=[f"ID: {c[0]}, {p[1]}, Data: {c[2]}" for c in compras for p in listar_produtos() if p[0] == c[1]],  
        
        width=40  # Aumente a largura da combobox
    )  
    combo_compra.pack()

    tk.Button(janela, text="Excluir", command=lambda: (
       excluir_compra(int(combo_compra.get().split(",")[0].split(":")[1].strip())),  # Extrai o ID da compra
        janela.destroy()  # Fecha a janela após excluir
    )).pack(pady=20)

def excluir_produto_janela():
    janela = tk.Toplevel(root)
    janela.title("Excluir Produto")
    janela.geometry("400x200")  # Aumente a largura da janela

    tk.Label(janela, text="Selecione o Produto:").pack(pady=10)
    produtos = listar_produtos()
    combo_produto = ttk.Combobox(janela, values=[f"{p[1]} (ID: {p[0]})" for p in produtos], width=30)  # Aumente a largura da combobox
    combo_produto.pack()

    tk.Button(janela, text="Excluir", command=lambda: (
        excluir_produto(int(combo_produto.get().split("ID: ")[1][:-1])),
        janela.destroy()  # Fecha a janela após excluir
    )).pack(pady=20)

def alterar_duracao_janela():
    janela = tk.Toplevel(root)
    janela.title("Alterar Duração do Produto")
    janela.geometry("400x200")  # Aumente a largura da janela

    tk.Label(janela, text="Selecione o Produto:").pack(pady=10)
    produtos = listar_produtos()
    combo_produto = ttk.Combobox(janela, values=[f"{p[1]} (ID: {p[0]})" for p in produtos], width=30)  # Aumente a largura da combobox
    combo_produto.pack()

    tk.Label(janela, text="Nova Duração (dias):").pack(pady=10)
    entrada_duracao = tk.Entry(janela, width=30)
    entrada_duracao.pack()

    tk.Button(janela, text="Alterar", command=lambda: (
        alterar_duracao(int(combo_produto.get().split("ID: ")[1][:-1]), entrada_duracao.get()),
        janela.destroy()  # Fecha a janela após alterar
    )).pack(pady=20)

def alertas_janela():
    janela = tk.Toplevel(root)
    janela.title("Alertas de Compras")
    janela.geometry("600x400")  # Aumente a largura da janela

    # Criação da Treeview
    tree = ttk.Treeview(janela, columns=("Produto", "Data da Compra", "Duração", "Data da Próxima Compra"), show="headings")
    
    # Definição das colunas
    tree.heading("Produto", text="Produto")
    tree.heading("Data da Compra", text="Data da Compra")
    tree.heading("Duração", text="Duração (dias)")
    tree.heading("Data da Próxima Compra", text="Data da Próxima Compra")
    
    tree.column("Produto", anchor=tk.W, width=200)
    tree.column("Data da Compra", anchor=tk.W, width=100)
    tree.column("Duração", anchor=tk.W, width=100)
    tree.column("Data da Próxima Compra", anchor=tk.W, width=150)

    # Inserindo dados na Treeview
    compras = listar_compras()
    for compra in compras:
        produto_id = compra[1]
        data_compra = compra[2]
        
        # Obter o nome e a duração do produto usando o ID
        produto_nome = None
        duracao = None
        for p in listar_produtos():
            if p[0] == produto_id:  # Se o ID do produto coincidir
                produto_nome = p[1]  # O nome do produto é a segunda coluna
                duracao = p[2]  # A duração é a terceira coluna
                break
        
        if duracao is not None and produto_nome is not None:  # Certifique-se de que ambos estão disponíveis
            validade, alerta = calcular_validade(produto_id)  # Obter validade e alerta
            if validade:
                proxima_compra = alerta.date()  # Formatar a data da próxima compra
                tree.insert("", tk.END, values=(produto_nome, data_compra, duracao, proxima_compra))

    tree.pack(expand=True, fill='both')  # Expandir a Treeview para preencher a janela


# Configuração da janela principal
root = tk.Tk()
root.title("Controle de Compras")
root.geometry("300x500")  # Aumente a largura da janela principal

# Adicione os botões e outros elementos da interface gráfica
tk.Button(root, text="Registrar Produto", command=registrar_produto_janela).pack(pady=10)
tk.Button(root, text="Registrar Compra", command=registrar_compra_janela).pack(pady=10)
tk.Button(root, text="Excluir Compra", command=excluir_compra_janela).pack(pady=10)
tk.Button(root, text="Excluir Produto", command=excluir_produto_janela).pack(pady=10)  # Botão para abrir a janela de exclusão de produtos
tk.Button(root, text="Alterar Duração", command=alterar_duracao_janela).pack(pady=10)  # Botão para abrir a janela de alteração de duração
tk.Button(root, text="Alertas", command=alertas_janela).pack(pady=10)  # Botão para abrir a janela de alertas

# Execute a aplicação
root.mainloop()
