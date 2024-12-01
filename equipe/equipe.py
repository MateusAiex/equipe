__all__ = ['create_equipe', 'get_equipes', 'get_equipe_by_id', 'delete_equipe']

# Variaveis globais
lista_equipes = list()
id_equipe = 0

# Códigos de erro
OPERACAO_REALIZADA_COM_SUCESSO = 0
EQUIPE_NAO_ENCONTRADA = 1
DADOS_INVALIDOS = 2
NOME_DE_EQUIPE_JA_EXISTE = 3


def create_equipe(nome: str, funcoes: list) -> tuple[int, dict]:
    global lista_equipes
    global id_equipe

    if not nome or not isinstance(nome, str) or len(nome) == 0:
        return DADOS_INVALIDOS, "Nome inválido"
    if not isinstance(funcoes, list) or len(funcoes) == 0:
        return DADOS_INVALIDOS, "Funções inválidas"

    equipe = {
        "id": len(lista_equipes) + 1,
        "nome": nome,
        "funcoes": funcoes
    }

    for e in lista_equipes:
        if e["nome"] == nome:
            return NOME_DE_EQUIPE_JA_EXISTE, "Nome já existe"

    lista_equipes.append(equipe)
    return OPERACAO_REALIZADA_COM_SUCESSO, equipe


def get_equipes() -> tuple[int, list]:
    global lista_equipes
    return OPERACAO_REALIZADA_COM_SUCESSO, lista_equipes


def get_equipe_by_id(id_equipe: int) -> tuple[int, dict]:
    global lista_equipes

    for equipe in lista_equipes:
        if equipe["id"] == id_equipe:
            return OPERACAO_REALIZADA_COM_SUCESSO, equipe

    return EQUIPE_NAO_ENCONTRADA, "Equipe não encontrada"


def delete_equipe(id_equipe: int) -> tuple[int, dict]:
    global lista_equipes

    for equipe in lista_equipes:
        if equipe["id"] == id_equipe:
            lista_equipes.remove(equipe)
            return OPERACAO_REALIZADA_COM_SUCESSO, equipe

    return EQUIPE_NAO_ENCONTRADA, "Membro não encontrado"


def delete_equipes():
    global lista_equipes
    lista_equipes.clear()
