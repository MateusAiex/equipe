__all__ = [
    "attach_equipe",
    "detach_equipe",
    "get_equipe_from_projeto",
    "get_projetos_from_equipe"
]

# Variáveis globais
relacoes = []
id_relacao = 0

# Códigos de erro
STATUS_OK = 0
DADOS_INVALIDOS = 1
CONFLITO = 3
DADO_NAO_ENCONTRADO = 4

def attach_equipe(id_projeto: int, id_equipe: int) -> tuple[int, dict]:
    global relacoes
    global id_relacao

    # Validações
    if not isinstance(id_projeto, int) or not isinstance(id_equipe, int):
        return DADOS_INVALIDOS, "IDs inválidos."

    for relacao in relacoes:
        if relacao["id_projeto"] == id_projeto and relacao["id_equipe"] == id_equipe:
            return CONFLITO, "Equipe já associada ao projeto."

    id_relacao += 1
    relacao = {
        "id": id_relacao,
        "id_projeto": id_projeto,
        "id_equipe": id_equipe
    }
    relacoes.append(relacao)
    return STATUS_OK, relacao


def detach_equipe(id_projeto: int, id_equipe: int) -> tuple[int, dict]:
    global relacoes

    for relacao in relacoes:
        if relacao["id_projeto"] == id_projeto and relacao["id_equipe"] == id_equipe:
            relacoes.remove(relacao)
            return STATUS_OK, relacao

    return DADO_NAO_ENCONTRADO, "Associação não encontrada."


def get_equipe_from_projeto(id_projeto: int) -> tuple[int, list]:
    global relacoes

    equipes = [relacao["id_equipe"] for relacao in relacoes if relacao["id_projeto"] == id_projeto]

    if not equipes:
        return DADO_NAO_ENCONTRADO, "Nenhuma equipe associada ao projeto."
    return STATUS_OK, equipes


def get_projetos_from_equipe(id_equipe: int) -> tuple[int, list]:
    global relacoes

    projetos = [relacao["id_projeto"] for relacao in relacoes if relacao["id_equipe"] == id_equipe]

    if not projetos:
        return DADO_NAO_ENCONTRADO, "Nenhum projeto associado à equipe."
    return STATUS_OK, projetos

def reset_relacoes():
    global relacoes, id_relacao
    relacoes.clear()
    id_relacao = 0
