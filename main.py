import tkinter as tk
from tkinter import simpledialog, messagebox
import json
from equipe import create_equipe, get_equipes
from membro import create_membro, get_membros, get_membro_by_id
from tarefa import create_tarefa, get_tarefas, get_tarefa_by_id, set_status
from projeto import create_projeto, get_projetos
from pertence import attach_equipe
from faz import assign_tarefa
from compactador import compacta, descompacta
from participa import assign_membro, get_membros_from_equipe, get_participacoes

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
    "participa": [],
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
        for membro in lista_membros:
            create_membro(membro["nome"], membro["funcoes"])  
        lista_equipes = dados["equipes"]
        for equipe in lista_equipes:
            create_equipe(equipe["nome"], equipe["funcoes"])
        lista_projetos = dados["projetos"]
        for projeto in lista_projetos:
            create_projeto(projeto["titulo"], projeto["descricao"], projeto["prazo"])
        lista_tarefas = dados["tarefas"]
        for tarefa in lista_tarefas:
            create_tarefa(tarefa["descricao"], tarefa["status"], tarefa["prioridade"], tarefa["id_projeto"])
        lista_faz = dados["faz"]
        for faz in lista_faz:
            assign_tarefa(faz["id_membro"], faz["id_tarefa"], get_membro_by_id, get_tarefa_by_id)
        lista_pertence = dados["pertence"]
        for pertence in lista_pertence:
            attach_equipe(pertence["id_projeto"], pertence["id_equipe"])
        lista_participa = dados["participa"]
        for participa in lista_participa:
            assign_membro(participa["id_membro"], participa["id_equipe"])
        
        

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
        """
        Abre uma janela para associar um membro a uma equipe.
        """
        janela_associacao = tk.Toplevel()
        janela_associacao.title("Associar Membro a Equipe")
        janela_associacao.geometry("600x400")

        membros_frame = tk.LabelFrame(janela_associacao, text="Membros Disponíveis", padx=10, pady=10)
        membros_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        equipes_frame = tk.LabelFrame(janela_associacao, text="Equipes Disponíveis", padx=10, pady=10)
        equipes_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Exibir membros disponíveis
        for membro in dados["membros"]:
            tk.Label(
                membros_frame,
                text=f"ID: {membro['id']}, Nome: {membro['nome']}"
            ).pack(anchor="w")

        # Exibir equipes disponíveis
        for equipe in dados["equipes"]:
            tk.Label(
                equipes_frame,
                text=f"ID: {equipe['id']}, Nome: {equipe['nome']}"
            ).pack(anchor="w")

        # Inputs para associação
        tk.Label(janela_associacao, text="Digite o ID do Membro:").pack(pady=5)
        id_membro_entry = tk.Entry(janela_associacao)
        id_membro_entry.pack(pady=5)

        tk.Label(janela_associacao, text="Digite o ID da Equipe:").pack(pady=5)
        id_equipe_entry = tk.Entry(janela_associacao)
        id_equipe_entry.pack(pady=5)

        def salvar_associacao():
            try:
                # Recuperar IDs digitados
                id_membro = int(id_membro_entry.get())
                id_equipe = int(id_equipe_entry.get())

                # Validar existência do membro e da equipe
                membro = next((m for m in dados["membros"] if m["id"] == id_membro), None)
                equipe = next((e for e in dados["equipes"] if e["id"] == id_equipe), None)

                if not membro:
                    messagebox.showerror("Erro", f"Membro com ID {id_membro} não encontrado.")
                    return
                if not equipe:
                    messagebox.showerror("Erro", f"Equipe com ID {id_equipe} não encontrada.")
                    return

                # Realizar associação
                resultado = assign_membro(id_equipe,id_membro)
                if resultado == 0:
                    dados["participa"].append({"id_membro": id_membro, "id_equipe": id_equipe})
                    messagebox.showinfo("Sucesso", "Membro associado à equipe com sucesso!")
                    janela_associacao.destroy()
                else:
                    messagebox.showerror("Erro", "Falha ao associar membro à equipe. Verifique as regras de associação.")
            except ValueError:
                messagebox.showerror("Erro", "IDs inválidos. Insira valores numéricos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        tk.Button(janela_associacao, text="Salvar Associação", command=salvar_associacao).pack(pady=20)
        
    def associar_projeto_a_equipe():
        """
        Abre uma janela para associar um projeto a uma equipe.
        """
        janela_associacao = tk.Toplevel()
        janela_associacao.title("Associar Projeto a Equipe")
        janela_associacao.geometry("600x400")
        
        projetos_frame = tk.LabelFrame(janela_associacao, text="Projetos Disponíveis", padx=10, pady=10)
        projetos_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        equipes_frame = tk.LabelFrame(janela_associacao, text="Equipes Disponíveis", padx=10, pady=10)
        equipes_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Exibir projetos disponíveis
        if not dados["projetos"]:
            tk.Label(projetos_frame, text="Nenhum projeto cadastrado.").pack(anchor="w")
        else:  
            for projeto in dados["projetos"]:
                tk.Label(
                    projetos_frame,
                    text=f"ID: {projeto['id']}, Título: {projeto['titulo']}"
                ).pack(anchor="w")
            
        # Exibir equipes disponíveis
        if not dados["equipes"]:
            tk.Label(equipes_frame, text="Nenhuma equipe cadastrada.").pack(anchor="w")
        else:
            for equipe in dados["equipes"]:
                tk.Label(
                    equipes_frame,
                    text=f"ID: {equipe['id']}, Nome: {equipe['nome']}"
                ).pack(anchor="w")
        
        # Inputs para associação
        tk.Label(janela_associacao, text="Digite o ID do Projeto:").pack(pady=5)
        id_projeto_entry = tk.Entry(janela_associacao)
        id_projeto_entry.pack(pady=5)
        
        tk.Label(janela_associacao, text="Digite o ID da Equipe:").pack(pady=5)
        id_equipe_entry = tk.Entry(janela_associacao)
        id_equipe_entry.pack(pady=5)
        
        def salvar_associacao():
            try:
                # Recuperar IDs digitados
                id_projeto = int(id_projeto_entry.get())
                id_equipe = int(id_equipe_entry.get())
                
                # Validar existência do projeto e da equipe
                projeto = next((p for p in dados["projetos"] if p["id"] == id_projeto), None)
                equipe = next((e for e in dados["equipes"] if e["id"] == id_equipe), None)
                
                if not projeto:
                    messagebox.showerror("Erro", f"Projeto com ID {id_projeto} não encontrado.")
                    return
                if not equipe:
                    messagebox.showerror("Erro", f"Equipe com ID {id_equipe} não encontrada.")
                    return
                
                # Realizar associação
                resultado, mensagem = attach_equipe(id_projeto, id_equipe)
                if resultado == 0:
                    dados["pertence"].append({"id_equipe": id_equipe, "id_projeto": id_projeto})
                    messagebox.showinfo("Sucesso", "Projeto associado à equipe com sucesso!")
                    janela_associacao.destroy()
                else:
                    messagebox.showerror("Erro", f'Falha ao associar projeto à equipe. Verifique as regras de associação. Resultado: {mensagem}')
            except ValueError:
                messagebox.showerror("Erro", "IDs inválidos. Insira valores numéricos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        
        tk.Button(janela_associacao, text="Salvar Associação", command=salvar_associacao).pack(pady=20)
        
    def associar_tarefa_a_membro():
        janela_associacao = tk.Toplevel()
        janela_associacao.title("Associar Tarefa a Membro")
        janela_associacao.geometry("600x400")

        tarefas_frame = tk.LabelFrame(janela_associacao, text="Tarefas Disponíveis", padx=10, pady=10)
        tarefas_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        membros_frame = tk.LabelFrame(janela_associacao, text="Membros Disponíveis", padx=10, pady=10)
        membros_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Exibir tarefas disponíveis
        for tarefa in dados["tarefas"]:
            tk.Label(
                tarefas_frame,
                text=f"ID: {tarefa['id_tarefa']}, Descrição: {tarefa['descricao']}, Status: {tarefa['status']}"
            ).pack(anchor="w")

        # Exibir membros disponíveis
        for membro in dados["membros"]:
            tk.Label(
                membros_frame,
                text=f"ID: {membro['id']}, Nome: {membro['nome']}"
            ).pack(anchor="w")

        # Inputs para associação
        tk.Label(janela_associacao, text="Digite o ID da Tarefa:").pack(pady=5)
        id_tarefa_entry = tk.Entry(janela_associacao)
        id_tarefa_entry.pack(pady=5)

        tk.Label(janela_associacao, text="Digite o ID do Membro:").pack(pady=5)
        id_membro_entry = tk.Entry(janela_associacao)
        id_membro_entry.pack(pady=5)

        def salvar_associacao():
            try:
                id_tarefa = int(id_tarefa_entry.get())
                id_membro = int(id_membro_entry.get())

                # Verificar se o ID do membro e o ID da tarefa existem
                membro = next((m for m in dados["membros"] if m["id"] == id_membro), None)
                tarefa = next((t for t in dados["tarefas"] if t["id_tarefa"] == id_tarefa), None)

                if not membro:
                    messagebox.showerror("Erro", f"Membro com ID {id_membro} não encontrado.")
                    return
                if not tarefa:
                    messagebox.showerror("Erro", f"Tarefa com ID {id_tarefa} não encontrada.")
                    return
                

                # Realizar a associação usando assign_tarefa
                resultado, mensagem = assign_tarefa(
                    id_membro,
                    id_tarefa,
                    get_membro_by_id,
                    get_tarefa_by_id,
                )

                if resultado == 0:
                    dados["faz"].append({"id_membro": id_membro, "id_tarefa": id_tarefa})
                    set_status(id_tarefa, "Em Andamento")
                    dados["tarefas"][id_tarefa-2621]["status"] = "Em Andamento"
                    messagebox.showinfo("Sucesso", "Tarefa associada ao membro com sucesso!")
                    janela_associacao.destroy()
                else:
                    messagebox.showerror("Erro", f"Erro ao associar: {mensagem}")
            except ValueError:
                messagebox.showerror("Erro", "IDs inválidos. Insira valores numéricos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

        tk.Button(janela_associacao, text="Salvar Associação", command=salvar_associacao).pack(pady=20)
    def conclui_tarefa():
        janela_associacao = tk.Toplevel()
        janela_associacao.title("Concluir Tarefa")
        janela_associacao.geometry("600x400")
        
        tarefas_frame = tk.LabelFrame(janela_associacao, text="Tarefas Disponíveis", padx=10, pady=10)
        tarefas_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Exibir tarefas disponíveis
        for tarefa in dados["tarefas"]:
            tk.Label(
                tarefas_frame,
                text=f"ID: {tarefa['id_tarefa']}, Descrição: {tarefa['descricao']}, Status: {tarefa['status']}"
            ).pack(anchor="w")
        
        # Inputs para associação
        tk.Label(janela_associacao, text="Digite o ID da Tarefa:").pack(pady=5)
        id_tarefa_entry = tk.Entry(janela_associacao)
        id_tarefa_entry.pack(pady=5)
        
        tk.Label(janela_associacao, text="Digite o status da tarefa (Concluída ou em Andamento):").pack(pady=5)
        status_entry = tk.Entry(janela_associacao)
        status_entry.pack(pady=5)
        
        
        def salvar_associacao():
            try:
                id_tarefa = int(id_tarefa_entry.get())
                status = status_entry.get()
                
                tarefa = next((t for t in dados["tarefas"] if t["id_tarefa"] == id_tarefa), None)
                if not tarefa:
                    messagebox.showerror("Erro", f"Tarefa com ID {id_tarefa} não encontrada.")
                    return
                
                set_status(id_tarefa, status)
                dados["tarefas"][id_tarefa-2621]["status"] = status
                messagebox.showinfo("Sucesso", "Tarefa concluída com sucesso!")
                janela_associacao.destroy()
            except ValueError:
                messagebox.showerror("Erro", "IDs inválidos. Insira valores numéricos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
                
        tk.Button(janela_associacao, text="Salvar Conclusão", command=salvar_associacao).pack(pady=20)
            
        return
    # Listagens
    def listar_membros():
        membros = get_membros()[1]
        mensagem = "\n".join([f"ID: {m['id']}, Nome: {m['nome']}" for m in membros])
        messagebox.showinfo("Membros Cadastrados", mensagem or "Nenhum membro cadastrado.")

    def listar_tarefas():
        tarefas = get_tarefas()[1]
        mensagem = "\n".join([f"ID: {t['id_tarefa']}, Descrição: {t['descricao']}" for t in tarefas])
        messagebox.showinfo("Tarefas Cadastradas", mensagem or "Nenhuma tarefa cadastrada.")

    def listar_equipes():
        equipes = get_equipes()[1]
        mensagem = "\n".join([f"ID: {e['id']}, Nome: {e['nome']}" for e in equipes])
        messagebox.showinfo("Equipes Cadastradas", mensagem or "Nenhuma equipe cadastrada.")
    
    def listar_projetos():
        projetos = get_projetos()[1]
        mensagem = "\n".join([f"ID: {p['id']}, Título: {p['titulo']}, Prazo: {p['prazo']}" for p in projetos])
        messagebox.showinfo("Projetos Cadastrados", mensagem or "Nenhum projeto cadastrado.")
    
    def listar_membros_de_uma_equipe():
        janela_associacao = tk.Toplevel()
        janela_associacao.title("Equipes Disponíveis")
        janela_associacao.geometry("600x400")
        equipes_frame = tk.LabelFrame(janela_associacao, text="Equipes Disponíveis", padx=10, pady=10)
        equipes_frame.pack(fill="both", expand=True, padx=10, pady=10)
        for equipe in dados["equipes"]:
            tk.Label(
                equipes_frame,
                text=f"ID: {equipe['id']}, Nome: {equipe['nome']}"
            ).pack(anchor="w")
        tk.Label(janela_associacao, text="ID da Equipe:").pack(pady=5)
        id_equipe_entry = tk.Entry(janela_associacao)
        id_equipe_entry.pack(pady=5)
        
        def pesquisar_membros():
            id_equipe = int(id_equipe_entry.get())
            if id_equipe is None:
                return
            resultado, membros_id = get_membros_from_equipe(id_equipe)
            membros = [get_membro_by_id(m['id_membro'])[1] for m in membros_id]
            if resultado == 0:
                mensagem = "\n".join([f"ID: {m['id']}, Nome: {m['nome']}" for m in membros])
                messagebox.showinfo("Membros da Equipe", mensagem)
            else:
                messagebox.showerror("Erro", "Equipe não encontrada.")
        tk.Button(janela_associacao, text="Pesquisar Membros", command=pesquisar_membros).pack(pady=20)
        
    def listar_para_associar(mensagem, lista):
        return "\n".join([f"ID: {item['id']}, Nome: {item.get('nome', 'N/A')}, Título: {item.get('titulo', 'N/A')}" for item in lista]) or mensagem


    # Botões principais
    botoes = [
        ("Cadastrar Projeto", cadastrar_projeto),
        ("Cadastrar Membro", cadastrar_membro),
        ("Cadastrar Tarefa", cadastrar_tarefa),
        ("Cadastrar Equipe", cadastrar_equipe),
        ("Associar Membro a Equipe", associar_membro_a_equipe),
        ("Associar Projeto a Equipe", associar_projeto_a_equipe),
        ("Associar Tarefa a Membro", associar_tarefa_a_membro),
        ("Mudar Status de Tarefa", conclui_tarefa),
        ("Listar Membros", listar_membros),
        ("Listar Tarefas", listar_tarefas),
        ("Listar Equipes", listar_equipes),
        ("Listar Projetos", listar_projetos),
        ("Listar Membros de uma Equipe", listar_membros_de_uma_equipe),
        ("Salvar Dados", salvar_dados),
        ("Carregar Dados", carregar_dados),
    
    ]

    for texto, comando in botoes:
        tk.Button(janela, text=texto, command=comando).pack(pady=5)

    janela.mainloop()


if __name__ == "__main__":
    carregar_dados()
    criar_janela_principal()
