# Variaveis globais
lista_equipes = list()

# Códigos de erro
OPERACAO_REALIZADA_COM_SUCESSO = 0
EQUIPE_NAO_ENCONTRADA = 1


def create_equipe(nome: str, funcoes: list) -> tuple[int, list]:
    global lista_equipes

    equipe = {
        "id": len(lista_equipes) + 1,
        "nome": nome,
        "funcoes": funcoes
    }

    lista_equipes.append(equipe)
    return OPERACAO_REALIZADA_COM_SUCESSO, equipe


def get_equipes() -> tuple[int, list]:
    global lista_equipes
    return OPERACAO_REALIZADA_COM_SUCESSO, lista_equipes


def get_equipe_by_id(id_equipe: int) -> tuple[int, list]:
    global lista_equipes

    for equipe in lista_equipes:
        if equipe["id"] == id_equipe:
            return OPERACAO_REALIZADA_COM_SUCESSO, equipe

    return EQUIPE_NAO_ENCONTRADA, []


def delete_equipe(id_equipe: int) -> tuple[int, list]:
    global lista_equipes

    for equipe in lista_equipes:
        if equipe["id"] == id_equipe:
            lista_equipes.remove(equipe)
            return OPERACAO_REALIZADA_COM_SUCESSO, equipe

    return EQUIPE_NAO_ENCONTRADA, []
