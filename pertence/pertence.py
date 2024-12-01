# Variáveis globais
lista_pertence = list()
id_pertence_provisorio = 2220

# Atributos exportados
__all__ = [
    "attach_equipe",
    "detach_equipe",
    "get_equipe_from_projetos",
    "get_projetos_from_equipes",
]

# Códigos de erro
STATUS_OK = 0
DADOS_INVALIDOS = 1
ERRO_AO_DELETAR = 2
CONFLITO = 3
DADO_NÃO_ENCONTRADO = 4
EQUIPE_NÃO_ASSOCIADA_AO_PROJETO = 10
EQUIPE_JÁ_ASSOCIADA_AO_PROJETO = 11


def attach_equipe(id_projeto: int, id_equipe: int) -> tuple[int, dict]:
    """
    Associa uma equipe a um projeto.

    id_projeto: ID do projeto.
    id_equipe: ID da equipe.
    return: Código de status e o objeto de associação criado.
    """
    global lista_pertence
    global id_pertence_provisorio

    for pertence in lista_pertence:
        if pertence["id_projeto"] == id_projeto and pertence["id_equipe"] == id_equipe:
            return EQUIPE_JÁ_ASSOCIADA_AO_PROJETO, {}

    id_pertence_provisorio += 1
    pertence = {
        "id": id_pertence_provisorio,
        "id_projeto": id_projeto,
        "id_equipe": id_equipe,
    }
    lista_pertence.append(pertence)
    return STATUS_OK, pertence


def detach_equipe(id_projeto: int, id_equipe: int) -> tuple[int, dict]:
    """
    Remove a associação de uma equipe a um projeto.

    id_projeto: ID do projeto.
    id_equipe: ID da equipe.
    return: Código de status e o objeto de associação removido.
    """
    global lista_pertence

    for pertence in lista_pertence:
        if pertence["id_projeto"] == id_projeto and pertence["id_equipe"] == id_equipe:
            lista_pertence.remove(pertence)
            return STATUS_OK, pertence

    return EQUIPE_NÃO_ASSOCIADA_AO_PROJETO, {}


def get_equipe_from_projetos(id_projeto: int) -> tuple[int, list[dict]]:
    """
    Retorna todas as equipes associadas a um projeto.

    id_projeto: ID do projeto.
    return: Código de status e lista de equipes associadas.
    """
    global lista_pertence

    equipes = [pertence for pertence in lista_pertence if pertence["id_projeto"] == id_projeto]

    if equipes:
        return STATUS_OK, equipes

    return DADO_NÃO_ENCONTRADO, []


def get_projetos_from_equipes(id_equipe: int) -> tuple[int, list[dict]]:
    """
    Retorna todos os projetos associados a uma equipe.

    id_equipe: ID da equipe.
    return: Código de status e lista de projetos associados.
    """
    global lista_pertence

    projetos = [pertence for pertence in lista_pertence if pertence["id_equipe"] == id_equipe]

    if projetos:
        return STATUS_OK, projetos

    return DADO_NÃO_ENCONTRADO, []

