# Variáveis globais
lista_tarefas = list()
id_tarefa_provisorio = 2620

# Códigos de erro
STATUS_OK = 0
DADOS_INVALIDOS = 1
ERRO_AO_DELETAR = 2
CONFLITO = 3
DADO_NÃO_ENCONTRADO = 4

#Elementos a serem exportados
__all__ = [
    "create_tarefa",
    "get_tarefas",
    "get_tarefa_by_id",
    "delete_tarefa",
    "set_status",
    "get_tarefas_by_prioridade",
    "get_tarefas_by_projeto",
]

def create_tarefa(descricao: str, status: str, prioridade: int, id_projeto: int) -> tuple[int, dict]:
    """
    Cria uma nova tarefa e adiciona à lista global de tarefas.

    descricao: Descrição da tarefa.
    status: Status da tarefa.
    prioridade: Qual a ordem de prioridade da tarefa.
    id_projeto: ID do projeto que a tarefa está vinculada.
    return: Código de status e a tarefa criada.
    """
    global lista_tarefas
    global id_tarefa_provisorio
    if not descricao or not status or not prioridade or not id_projeto:
        return DADOS_INVALIDOS, {}

    try:
        id_tarefa_provisorio += 1
        tarefa = {
            "id_tarefa": id_tarefa_provisorio,
            "descricao": descricao,
            "status": status,
            "prioridade": prioridade,
            "id_projeto": id_projeto,
        }
        lista_tarefas.append(tarefa)
        return STATUS_OK, tarefa
    except Exception as e:
        print(f"Erro inesperado ao criar tarefa: {e}")
        return DADOS_INVALIDOS, {}


def get_tarefas() -> tuple[int, list]:
    """
    Retorna todos as tarefas.

    return: Código de status e lista de tarefas.
    """
    global lista_tarefas
    return STATUS_OK, lista_tarefas


def get_tarefa_by_id(id_tarefa: int) -> tuple[int, dict]:
    """
    Retorna uma tarefa com base no ID fornecido.

    id_tarefa: ID da terafa a ser buscado.
    return: Código de status e a tarefa encontrada ou erro.
    """
    global lista_tarefas

    for tarefa in lista_tarefas:
        if tarefa["id_tarefa"] == id_tarefa:
            return STATUS_OK, tarefa
    
    return DADO_NÃO_ENCONTRADO, {}

def delete_tarefa(id_tarefa: int) -> tuple[int, dict]:
    """
    Remove uma tarefa com base no ID fornecido.

    id_tarefa: ID da tarefa a ser removida.
    Código de status e a tarefa removida ou erro.
    """
    global lista_tarefas

    for tarefa in lista_tarefas:
        if tarefa["id_tarefa"] == id_tarefa:
            lista_tarefas.remove(tarefa)
            return STATUS_OK, tarefa

    return DADO_NÃO_ENCONTRADO, {}

def set_status(id_tarefa: int, status: str) -> tuple[int, dict]:
    """
    Altera o status de uma tarefa com base no ID fornecido.

    id_tarefa: ID da terafa selecionada.
    status: Status da tarefa selecionada.
    return: Código de status e a tarefa selecionada ou erro.
    """
    global lista_tarefas

    for tarefa in lista_tarefas:
        if tarefa["id_tarefa"] == id_tarefa:
            tarefa["status"] = status
            return STATUS_OK, tarefa
    
    return DADO_NÃO_ENCONTRADO, {}

def get_tarefas_by_prioridade(prioridade: int) -> tuple[int, list]:
    """
    Retorna a ordem de prioridade das tarefas

    prioridade: ordem de prioriade das tarefas
    return: Código de status e a lista de tarefas em ordem ou erro.
    """

    global lista_tarefas

    tarefas_filtradas = [tarefa for tarefa in lista_tarefas if tarefa["prioridade"] == prioridade]

    if tarefas_filtradas:
        return STATUS_OK, tarefas_filtradas

    return DADO_NÃO_ENCONTRADO, []

def get_tarefas_by_projeto(id_projeto: int) -> tuple[int, list]:
    """
    Retorna as tarefas vinculadas a um projeto específico.

    id_projeto: ID do projeto a ser buscado
    return: Código de status e a a lista de tarefas ou erro.
    """

    global lista_tarefas

    tarefas_filtradas = [tarefa for tarefa in lista_tarefas if tarefa["id_projeto"] == id_projeto]

    if tarefas_filtradas:
        return STATUS_OK, tarefas_filtradas

    return DADO_NÃO_ENCONTRADO, []



