__all__ = ["assign_tarefa", "get_tarefas_by_membro", "get_membro_by_tarefa", "lista_faz"]

lista_faz = []
id_faz = 0

STATUS_OK = 0
DADO_NAO_ENCONTRADO = 4
CONFLITO = 3
DADOS_INVALIDOS = 1
TAREFA_JA_ATRIBUIDA = 8

def assign_tarefa(id_membro: int, id_tarefa: int, get_membro_by_id, get_tarefa_by_id) -> tuple[int, dict]:
    '''
    Função que atribui uma tarefa a um membro específico e retorna a relação criada entre eles em caso de sucesso ou um erro caso contrário
    '''
    global lista_faz
    global id_faz

    # Verificar existência de membro e tarefa
    status_membro, membro = get_membro_by_id(id_membro)
    if status_membro != STATUS_OK:
        return DADO_NAO_ENCONTRADO, "Membro não encontrado"

    status_tarefa, tarefa = get_tarefa_by_id(id_tarefa)
    if status_tarefa != STATUS_OK:
        return DADO_NAO_ENCONTRADO, "Tarefa não encontrada"

    # Verificar se a tarefa já foi concluída
    if tarefa["status"] == "Concluída":
        return DADOS_INVALIDOS, "Tarefa já concluída"

    # Verificar conflitos na atribuição
    for faz in lista_faz:
        if faz["id_tarefa"] == id_tarefa:
            return TAREFA_JA_ATRIBUIDA, "Tarefa já atribuída a outro membro"
    
    for faz in lista_faz:
        if faz["id_membro"] == id_membro:
            if not (_tarefa_foi_concluida(faz["id_tarefa"], get_tarefa_by_id)[1]):
                return CONFLITO, "Membro já possui uma tarefa em andamento"
    # Atribuir tarefa
    id_faz += 1
    nova_faz = {
        "id": id_faz,
        "id_membro": id_membro,
        "id_tarefa": id_tarefa,
    }
    lista_faz.append(nova_faz)
    return STATUS_OK, nova_faz
    
  
def get_tarefas_by_membro(id_membro: int, get_membro_by_id, get_tarefas) -> tuple[int, list]:
  '''
  Dado um id de membro, retorna todas as tarefas atribuídas a ele, caso o membro não exista, retorna um erro
  '''
  membro = get_membro_by_id(id_membro)
  if membro[0] != STATUS_OK:
      return membro
    
  global lista_faz
  status, lista_tarefas = get_tarefas()
  
  tarefas = []
  for faz in lista_faz:
      if faz["id_membro"] == id_membro:
          for tarefa in lista_tarefas:
              if tarefa["id"] == faz["id_tarefa"]:
                  tarefas.append(tarefa)
  if len(tarefas) == 0:
      return DADO_NAO_ENCONTRADO, "Tarefas não encontradas"
  return STATUS_OK, tarefas

def get_membro_by_tarefa(id_tarefa: int, get_tarefa_by_id, get_membro_by_id) -> tuple[int, dict]:
  '''
  Dado um id de tarefa, retorna o membro atribuído a ela, caso a tarefa não exista, retorna um erro
  '''
  global lista_faz
  tarefa = get_tarefa_by_id(id_tarefa)
  if tarefa[0] != STATUS_OK:
      return tarefa
  
  for faz in lista_faz:
      if faz["id_tarefa"] == id_tarefa:
          return STATUS_OK, get_membro_by_id(faz["id_membro"])
  return DADO_NAO_ENCONTRADO, "Tarefa não atribuída a nenhum membro"
    
    
  
def _tarefa_foi_concluida(id_tarefa: int, get_tarefa_by_id) -> tuple[int, bool]:
    '''
    Função auxiliar que verifica se uma tarefa foi concluída
    '''
    status_tarefa, tarefa = get_tarefa_by_id(id_tarefa)
    if status_tarefa != STATUS_OK:
        return status_tarefa, False
    return STATUS_OK, tarefa["status"].lower() == "concluída"



