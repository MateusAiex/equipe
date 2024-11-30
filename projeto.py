# Variáveis globais
lista_projetos = list()
id_projeto_provisorio = 2420

# Códigos de erro
STATUS_OK = 0
DADOS_INVALIDOS = 1
ERRO_AO_DELETAR = 2
CONFLITO = 3
DADO_NÃO_ENCONTRADO = 4

#Elementos a serem exportados
__all__ = [
    "create_projeto",
    "get_projetos",
    "get_projetos_by_id",
    "delete_projeto",
]
def create_projeto(titulo: str, descricao: str, prazo: tuple[int, int, int]) -> tuple[int, dict]:
    """
    Cria um novo projeto e adiciona à lista global de projetos.

    titulo: Título do projeto.
    descricao: Descrição do projeto.
    prazo: Prazo do projeto (dia, mes, ano).
    return: Código de status e o projeto criado.
    """
    global lista_projetos
    global id_projeto_provisorio

    try:
        id_projeto_provisorio += 1
        projeto = {
            "id": id_projeto_provisorio,
            "titulo": titulo,
            "descricao": descricao,
            "prazo": prazo,
        }
        lista_projetos.append(projeto)
        return STATUS_OK, projeto
    except Exception as e:
        print(f"Erro inesperado ao criar projeto: {e}")
        return DADOS_INVALIDOS, {}

def get_projetos() -> tuple[int, list]:
    """
    Retorna todos os projetos.

    return: Código de status e lista de projetos.
    """
    global lista_projetos
    return STATUS_OK, lista_projetos

def get_projetos_by_id(id_projeto: int) -> tuple[int, dict]:
    """
    Retorna um projeto com base no ID fornecido.

    id_projeto: ID do projeto a ser buscado.
    return: Código de status e o projeto encontrado ou erro.
    """
    global lista_projetos

    for projeto in lista_projetos:
        if projeto["id"] == id_projeto:
            return STATUS_OK, projeto
    
    return DADO_NÃO_ENCONTRADO, {}

def delete_projeto(id_projeto: int) -> tuple[int, dict]:
    """
    Remove um projeto com base no ID fornecido.

    id_projeto: ID do projeto a ser removido.
    return: Código de status e o projeto removido ou erro.
    """
    global lista_projetos

    for projeto in lista_projetos:
        if projeto["id"] == id_projeto:
            lista_projetos.remove(projeto)
            return STATUS_OK, projeto

    return DADO_NÃO_ENCONTRADO, {}

