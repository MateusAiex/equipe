__all__ = ["set_lider", "validate_unique_lider", "assign_membro", "check_team_roles", "get_membros_from_equipe", "get_equipe_from_membro", "get_membros_by_id"]

# Define global variables
lista_participacoes = []

STATUS_OK = 0
DADO_NAO_ENCONTRADO = 4
MULTIPLOS_LIDERES = 2
PAPEIS_INCOMPLETOS = 5
MEMBRO_JA_ATRIBUIDO = 7

def set_lider(id_equipe: int, id_membro: int) -> int:
    """
    Define um membro como líder de uma equipe.

    Parâmetros:
    id_equipe (int): ID da equipe.
    id_membro (int): ID do membro.

    Retorna:
    int: STATUS_OK se o líder foi definido com sucesso, DADO_NAO_ENCONTRADO se o membro não estiver na equipe.
    """
    global lista_participacoes
    for participacao in lista_participacoes:
        if participacao["id_equipe"] == id_equipe and participacao["id_membro"] == id_membro:
            participacao["elider"] = True
            return STATUS_OK
    return DADO_NAO_ENCONTRADO


def validate_unique_lider(id_equipe: int) -> int:
    """
    Verifica se uma equipe possui exatamente um líder.

    Parâmetros:
    id_equipe (int): ID da equipe.

    Retorna:
    int: STATUS_OK se houver exatamente um líder, MULTIPLOS_LIDERES se houver mais de um líder, DADO_NAO_ENCONTRADO se não houver líder.
    """
    global lista_participacoes
    lideres = [p for p in lista_participacoes if p["id_equipe"] == id_equipe and p["elider"]]
    
    if len(lideres) == 1:
        return STATUS_OK
    elif len(lideres) > 1:
        return MULTIPLOS_LIDERES
    return DADO_NAO_ENCONTRADO


def assign_membro(id_equipe: int, id_membro: int) -> int:
    """
    Atribui um membro a uma equipe.
    
    Parâmetros:
    id_equipe (int): ID da equipe.
    id_membro (int): ID do membro.

    Retorna:
    int: STATUS_OK se o membro foi atribuído com sucesso, MEMBRO_JA_ATRIBUIDO se o membro já estiver atribuído a essa equipe.
    """
    global lista_participacoes
    for participacao in lista_participacoes:
        if participacao["id_equipe"] == id_equipe and participacao["id_membro"] == id_membro:
            return MEMBRO_JA_ATRIBUIDO
    lista_participacoes.append({"id_equipe": id_equipe, "id_membro": id_membro, "elider": False})
    return STATUS_OK


def check_team_roles(id_equipe: int) -> int:
    """
    Verifica se a equipe tem todos os papéis necessários.

    Parâmetros:
    id_equipe (int): ID da equipe.

    Retorna:
    int: STATUS_OK se a equipe tiver todos os papéis necessários, PAPEIS_INCOMPLETOS se faltar algum papel, DADO_NAO_ENCONTRADO se a equipe não for encontrada.
    """
    global lista_participacoes
    membros = [p for p in lista_participacoes if p["id_equipe"] == id_equipe]
    
    if not membros:
        return DADO_NAO_ENCONTRADO
    
    lideres = [m for m in membros if m["elider"]]
    if len(lideres) == 1 and len(membros) > 1:
        return STATUS_OK
    return PAPEIS_INCOMPLETOS


# Funções adicionais

def get_membros_from_equipe(id_equipe: int):
    """
    Retorna todos os membros de uma equipe.

    Parâmetros:
    id_equipe (int): ID da equipe.

    Retorna:
    tuple: STATUS_OK e uma lista de membros, ou DADO_NAO_ENCONTRADO e uma lista vazia se a equipe não for encontrada.
    """
    global lista_participacoes
    membros = [p for p in lista_participacoes if p["id_equipe"] == id_equipe]
    if membros:
        return STATUS_OK, membros
    return DADO_NAO_ENCONTRADO, []


def get_equipe_from_membro(id_membro: int):
    """
    Retorna a equipe de um membro.


    Parâmetros:
    id_membro (int): ID do membro.

    Retorna:
    tuple: STATUS_OK e o ID da equipe, ou DADO_NAO_ENCONTRADO e None se o membro não for encontrado.
    """
    global lista_participacoes
    for participacao in lista_participacoes:
        if participacao["id_membro"] == id_membro:
            return STATUS_OK, participacao["id_equipe"]
    return DADO_NAO_ENCONTRADO, None


# Simulação de banco de dados de membros
mock_members = {
    1: {"id_membro": 1, "nome": "Membro 1"},
    2: {"id_membro": 2, "nome": "Membro 2"},
    3: {"id_membro": 3, "nome": "Membro 3"},
    10: {"id_membro": 10, "nome": "Membro 10"},
    20: {"id_membro": 20, "nome": "Membro 20"},
}

def get_membros_by_id(id_membro: int):
    """
    Simula a obtenção dos membros pelo ID.

    Parâmetros:
    id_membro (int): ID do membro.

    Retorna:
    tuple: STATUS_OK e os dados do membro, ou DADO_NAO_ENCONTRADO e None se o membro não for encontrado.
    """
    membro = mock_members.get(id_membro)
    if membro:
        return STATUS_OK, membro
    return DADO_NAO_ENCONTRADO, None
