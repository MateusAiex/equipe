import tkinter as tk
from tkinter import simpledialog, messagebox
import json
from equipe import create_equipe, get_equipes
from membro import create_membro, get_membros
from tarefa import create_tarefa, get_tarefas
from projeto import create_projeto, get_projetos
from pertence import attach_equipe
from faz import assign_tarefa
from compactador import compacta, descompacta
from participa import assign_membro

# Arquivo para persistência de dados
DATA_FILE = "dados_projeto.json"

# Estrutura de dados global
dados = {
    "equipes": [],
    "membros": [],
    "tarefas": [],
    "projetos": [],
    "pertence": [],
    "faz": [],
}

# Persistência
def salvar_dados():
    """
    Salva os dados da aplicação em um arquivo JSON e o compacta.
    """
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(dados, f, indent=4)
        compacta(DATA_FILE, DATA_FILE.replace(".json", ".bin"))
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")

def carregar_dados():
    """
    Carrega os dados da aplicação a partir de um arquivo JSON descompactado.
    """
    global dados, lista_membros, lista_equipes, lista_tarefas, lista_projetos
    try:
        descompacta(DATA_FILE.replace(".json", ".bin"), DATA_FILE)
        with open(DATA_FILE, "r") as f:
            dados = json.load(f)

        lista_membros = dados["membros"]
        lista_equipes = dados["equipes"]
        lista_tarefas = dados["tarefas"]
        lista_projetos = dados["projetos"]

        messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Nenhum arquivo de dados encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")

# Interface
def criar_janela_principal():
    janela = tk.Tk()
    janela.title("Gerenciamento de Projetos")
    janela.geometry("800x600")

    # Cadastro de entidades
    def cadastrar_projeto():
        janela_cadastro = tk.Toplevel()
        janela_cadastro.title("Cadastrar Projeto")
        janela_cadastro.geometry("400x300")

        tk.Label(janela_cadastro, text="Título do Projeto:").pack(pady=5)
        titulo_entry = tk.Entry(janela_cadastro)
        titulo_entry.pack(pady=5)

        tk.Label(janela_cadastro, text="Descrição do Projeto:").pack(pady=5)
        descricao_entry = tk.Entry(janela_cadastro)
        descricao_entry.pack(pady=5)

        tk.Label(janela_cadastro, text="Prazo (Dia/Mês/Ano):").pack(pady=5)
        prazo_dia_entry = tk.Entry(janela_cadastro, width=5)
        prazo_dia_entry.pack(side="left", padx=5)
        prazo_mes_entry = tk.Entry(janela_cadastro, width=5)
        prazo_mes_entry.pack(side="left", padx=5)
        prazo_ano_entry = tk.Entry(janela_cadastro, width=5)
        prazo_ano_entry.pack(side="left", padx=5)

        def salvar_projeto():
            titulo = titulo_entry.get()
            descricao = descricao_entry.get()
            prazo = (
                int(prazo_dia_entry.get()),
                int(prazo_mes_entry.get()),
                int(prazo_ano_entry.get()),
            )
            resultado, projeto = create_projeto(titulo, descricao, prazo)
            if resultado == 0:
                dados["projetos"].append(projeto)
                messagebox.showinfo("Sucesso", "Projeto cadastrado com sucesso!")
                janela_cadastro.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar projeto.")

        tk.Button(janela_cadastro, text="Salvar", command=salvar_projeto).pack(pady=20)

    def cadastrar_membro():
        janela_cadastro = tk.Toplevel()
        janela_cadastro.title("Cadastrar Membro")
        janela_cadastro.geometry("400x300")

        tk.Label(janela_cadastro, text="Nome do Membro:").pack(pady=5)
        nome_entry = tk.Entry(janela_cadastro)
        nome_entry.pack(pady=5)

        tk.Label(janela_cadastro, text="Funções (separadas por vírgula):").pack(pady=5)
        funcoes_entry = tk.Entry(janela_cadastro)
        funcoes_entry.pack(pady=5)

        def salvar_membro():
            nome = nome_entry.get()
            funcoes = [f.strip() for f in funcoes_entry.get().split(",")]
            resultado, membro = create_membro(nome, funcoes)
            if resultado == 0:
                dados["membros"].append(membro)
                messagebox.showinfo("Sucesso", "Membro cadastrado com sucesso!")
                janela_cadastro.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar membro.")

        tk.Button(janela_cadastro, text="Salvar", command=salvar_membro).pack(pady=20)


    def cadastrar_tarefa():
        janela_cadastro = tk.Toplevel()
        janela_cadastro.title("Cadastrar Tarefa")
        janela_cadastro.geometry("400x400")

        tk.Label(janela_cadastro, text="Descrição da Tarefa:").pack(pady=5)
        descricao_entry = tk.Entry(janela_cadastro)
        descricao_entry.pack(pady=5)

        tk.Label(janela_cadastro, text="Status (Ex: Pendente, Em Andamento):").pack(pady=5)
        status_entry = tk.Entry(janela_cadastro)
        status_entry.pack(pady=5)

        tk.Label(janela_cadastro, text="Prioridade (1 a 5):").pack(pady=5)
        prioridade_entry = tk.Entry(janela_cadastro)
        prioridade_entry.pack(pady=5)

        tk.Label(janela_cadastro, text="ID do Projeto:").pack(pady=5)
        id_projeto_entry = tk.Entry(janela_cadastro)
        id_projeto_entry.pack(pady=5)

        def salvar_tarefa():
            descricao = descricao_entry.get()
            status = status_entry.get()
            prioridade = int(prioridade_entry.get())
            id_projeto = int(id_projeto_entry.get())
            resultado, tarefa = create_tarefa(descricao, status, prioridade, id_projeto)
            if resultado == 0:
                dados["tarefas"].append(tarefa)
                messagebox.showinfo("Sucesso", "Tarefa cadastrada com sucesso!")
                janela_cadastro.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar tarefa.")

        tk.Button(janela_cadastro, text="Salvar", command=salvar_tarefa).pack(pady=20)

    def cadastrar_equipe():
        janela_cadastro = tk.Toplevel()
        janela_cadastro.title("Cadastrar Equipe")
        janela_cadastro.geometry("400x300")

        tk.Label(janela_cadastro, text="Nome da Equipe:").pack(pady=5)
        nome_entry = tk.Entry(janela_cadastro)
        nome_entry.pack(pady=5)

        tk.Label(janela_cadastro, text="Funções (separadas por vírgula):").pack(pady=5)
        funcoes_entry = tk.Entry(janela_cadastro)
        funcoes_entry.pack(pady=5)

        def salvar_equipe():
            nome = nome_entry.get()
            funcoes = [f.strip() for f in funcoes_entry.get().split(",")]
            resultado, equipe = create_equipe(nome, funcoes)
            if resultado == 0:
                dados["equipes"].append(equipe)
                messagebox.showinfo("Sucesso", "Equipe cadastrada com sucesso!")
                janela_cadastro.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar equipe.")

        tk.Button(janela_cadastro, text="Salvar", command=salvar_equipe).pack(pady=20)


    # Associações
    def associar_membro_a_equipe():
        janela_associacao = tk.Toplevel()
        janela_associacao.title("Associar Membro a Equipe")
        janela_associacao.geometry("600x400")

        membros_frame = tk.LabelFrame(janela_associacao, text="Membros")
        membros_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        equipes_frame = tk.LabelFrame(janela_associacao, text="Equipes")
        equipes_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Exibir membros
        for membro in dados["membros"]:
            tk.Label(membros_frame, text=f"ID: {membro['id']}, Nome: {membro['nome']}").pack()

        # Exibir equipes
        for equipe in dados["equipes"]:
            tk.Label(equipes_frame, text=f"ID: {equipe['id']}, Nome: {equipe['nome']}").pack()

        id_membro = tk.simpledialog.askinteger("Associar", "ID do Membro:")
        id_equipe = tk.simpledialog.askinteger("Associar", "ID da Equipe:")
        resultado, mensagem = assign_membro(id_membro, id_equipe)
        if resultado == 0:
            messagebox.showinfo("Sucesso", "Membro associado à equipe com sucesso!")
        else:
            messagebox.showerror("Erro", mensagem)


    def associar_tarefa_a_projeto():
        janela_associacao = tk.Toplevel()
        janela_associacao.title("Associar Tarefa a Projeto")
        janela_associacao.geometry("600x400")

        tarefas_frame = tk.LabelFrame(janela_associacao, text="Tarefas Disponíveis", padx=10, pady=10)
        tarefas_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        projetos_frame = tk.LabelFrame(janela_associacao, text="Projetos Disponíveis", padx=10, pady=10)
        projetos_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        for tarefa in dados["tarefas"]:
            tk.Label(
                tarefas_frame,
                text=f"ID: {tarefa['id_tarefa']}, Descrição: {tarefa['descricao']}, Status: {tarefa['status']}",
            ).pack(anchor="w")

        for projeto in dados["projetos"]:
            tk.Label(
                projetos_frame,
                text=f"ID: {projeto['id']}, Título: {projeto['titulo']}, Prazo: {projeto['prazo']}",
            ).pack(anchor="w")

        tk.Label(janela_associacao, text="ID da Tarefa:").pack(pady=5)
        id_tarefa_entry = tk.Entry(janela_associacao)
        id_tarefa_entry.pack(pady=5)

        tk.Label(janela_associacao, text="ID do Projeto:").pack(pady=5)
        id_projeto_entry = tk.Entry(janela_associacao)
        id_projeto_entry.pack(pady=5)

        def salvar_associacao():
            id_tarefa = int(id_tarefa_entry.get())
            id_projeto = int(id_projeto_entry.get())
            resultado, _ = attach_equipe(id_projeto, id_tarefa)  # Substitua pelo método correto de associação
            if resultado == 0:
                messagebox.showinfo("Sucesso", "Tarefa associada ao projeto com sucesso!")
                janela_associacao.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao associar tarefa ao projeto.")

        tk.Button(janela_associacao, text="Salvar Associação", command=salvar_associacao).pack(pady=20)

    # Listagens
    def listar_membros():
        membros = get_membros()[1]
        mensagem = "\n".join([f"ID: {m['id']}, Nome: {m['nome']}" for m in membros])
        messagebox.showinfo("Membros Cadastrados", mensagem or "Nenhum membro cadastrado.")

    def listar_tarefas():
        tarefas = get_tarefas()[1]
        mensagem = "\n".join([f"ID: {t['id']}, Descrição: {t['descricao']}" for t in tarefas])
        messagebox.showinfo("Tarefas Cadastradas", mensagem or "Nenhuma tarefa cadastrada.")

    def listar_equipes():
        equipes = get_equipes()[1]
        mensagem = "\n".join([f"ID: {e['id']}, Nome: {e['nome']}" for e in equipes])
        messagebox.showinfo("Equipes Cadastradas", mensagem or "Nenhuma equipe cadastrada.")
    
    def listar_projetos():
        projetos = get_projetos()[1]
        mensagem = "\n".join([f"ID: {p['id']}, Título: {p['titulo']}, Prazo: {p['prazo']}" for p in projetos])
        messagebox.showinfo("Projetos Cadastrados", mensagem or "Nenhum projeto cadastrado.")

    def listar_para_associar(mensagem, lista):
        return "\n".join([f"ID: {item['id']}, Nome: {item.get('nome', 'N/A')}, Título: {item.get('titulo', 'N/A')}" for item in lista]) or mensagem


    # Botões principais
    botoes = [
        ("Cadastrar Projeto", cadastrar_projeto),
        ("Cadastrar Membro", cadastrar_membro),
        ("Cadastrar Tarefa", cadastrar_tarefa),
        ("Cadastrar Equipe", cadastrar_equipe),
        ("Associar Membro a Equipe", associar_membro_a_equipe),
        ("Associar Tarefa a Projeto", associar_tarefa_a_projeto),
        ("Listar Membros", listar_membros),
        ("Listar Tarefas", listar_tarefas),
        ("Listar Equipes", listar_equipes),
        ("Salvar Dados", salvar_dados),
        ("Carregar Dados", carregar_dados),
        ("Listar Projetos", listar_projetos),
    ]

    for texto, comando in botoes:
        tk.Button(janela, text=texto, command=comando).pack(pady=5)

    janela.mainloop()


if __name__ == "__main__":
    carregar_dados()
    criar_janela_principal()
