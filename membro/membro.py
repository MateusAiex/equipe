__all__ = [
  "create_membro",
  "set_funcoes",
  "get_membro_by_id",
  "get_membros",
  "delete_membro",
  "lista_membros"
]

# Variaveis globais
lista_membros = list()
id_membro = 0

# Códigos de erro
STATUS_OK = 0
DADO_NAO_ENCONTRADO = 4
CONFLITO = 3
DADOS_INVALIDOS = 1


def create_membro(nome: str, funcoes: list) -> tuple[int, dict]:
    global lista_membros
    global id_membro

    if not nome or not isinstance(nome, str) or len(nome) == 0:
        return DADOS_INVALIDOS, "Nome inválido"
    if not isinstance(funcoes, list) or len(funcoes) == 0:
        return DADOS_INVALIDOS, "Funções inválidas"

    id_membro += 1
    membro = {
        "id": id_membro,
        "nome": nome,
        "funcoes": funcoes
    }
    for m in lista_membros:
        if m["nome"] == nome and m["funcoes"] == funcoes:
            return CONFLITO, "Membro já existente"

    lista_membros.append(membro)
    return STATUS_OK, membro

def set_funcoes(id: int, funcoes: list) -> tuple[int, dict]:
    global lista_membros
    
    if not isinstance(funcoes, list) or len(funcoes) == 0:
        return DADOS_INVALIDOS, "Funções inválidas"

    for m in lista_membros:
        if m["id"] == id:
            m["funcoes"] = funcoes
            return STATUS_OK, m

    return DADO_NAO_ENCONTRADO, "Membro não encontrado"

def get_membro_by_id(id: int) -> tuple[int, dict]:
    global lista_membros

    for m in lista_membros:
        if m["id"] == id:
            return STATUS_OK, m

    return DADO_NAO_ENCONTRADO, "Membro não encontrado"
  

def get_membros() -> tuple[int, dict]:
    global lista_membros

    return STATUS_OK, lista_membros

def delete_membro(id: int) -> tuple[int, dict]:
    global lista_membros

    for m in lista_membros:
        if m["id"] == id:
            lista_membros.remove(m)
            return STATUS_OK, m

    return DADO_NAO_ENCONTRADO, "Membro não encontrado"
