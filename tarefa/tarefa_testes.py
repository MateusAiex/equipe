import unittest
from tarefa import (
    create_tarefa, 
    get_tarefas, 
    get_tarefa_by_id, 
    delete_tarefa, 
    set_status, 
    get_tarefas_by_prioridade, 
    get_tarefas_by_projeto
)

# Definições dos códigos de erro
STATUS_OK = 0
DADOS_INVALIDOS = 1
ERRO_AO_DELETAR = 2
CONFLITO = 3
DADO_NÃO_ENCONTRADO = 4

class TestTarefaFunctions(unittest.TestCase):
    """
    Classe de testes para as funções relacionadas à tarefa. 
    Cada método testa um aspecto específico das operações CRUD das tarefas.
    """

    def setUp(self):
        """
        Configura o ambiente antes de cada teste.
        Limpa a lista de tarefas para garantir que os testes sejam independentes.
        """
        global lista_tarefas
        lista_tarefas = []  # Limpa a lista de tarefas antes de cada teste

    def test_create_tarefa_success(self):
        """
        Testa a criação de uma tarefa com dados válidos.
        Verifica se os dados retornados estão corretos e se a tarefa foi criada corretamente.
        """
        resultado, tarefa = create_tarefa("Descrição teste", "Em andamento", 1, 101)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(tarefa["descricao"], "Descrição teste")
        self.assertEqual(tarefa["status"], "Em andamento")
        self.assertEqual(tarefa["prioridade"], 1)
        self.assertEqual(tarefa["id_projeto"], 101)

    def test_create_tarefa_dados_invalidos(self):
        """
        Testa a criação de uma tarefa com dados inválidos (descrição vazia).
        Espera-se que o código de erro DADOS_INVALIDOS seja retornado.
        """
        resultado, mensagem = create_tarefa("", "Em andamento", 1, 101)
        self.assertEqual(resultado, DADOS_INVALIDOS)
        self.assertEqual(mensagem, {})

    def test_get_tarefas_success(self):
        """
        Testa a recuperação de todas as tarefas.
        Verifica se a função retorna o status correto e se há pelo menos uma tarefa na lista.
        """
        create_tarefa("Tarefa 1", "Em andamento", 2, 102)
        resultado, tarefas = get_tarefas()
        self.assertEqual(resultado, STATUS_OK)
        self.assertTrue(len(tarefas) > 0)

    def test_get_tarefa_by_id_success(self):
        """
        Testa a recuperação de uma tarefa por ID.
        Verifica se a tarefa retornada tem a descrição correta.
        """
        resultado, tarefa_temporaria = create_tarefa("Tarefa única", "Concluída", 3, 103)
        resultado, tarefa = get_tarefa_by_id(tarefa_temporaria["id_tarefa"])
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(tarefa["descricao"], "Tarefa única")

    def test_get_tarefa_by_id_inexistente(self):
        """
        Testa a recuperação de uma tarefa que não existe.
        Espera-se que o código de erro DADO_NÃO_ENCONTRADO seja retornado.
        """
        resultado, mensagem = get_tarefa_by_id(9999)
        self.assertEqual(resultado, DADO_NÃO_ENCONTRADO)
        self.assertEqual(mensagem, {})

    def test_delete_tarefa_success(self):
        """
        Testa a exclusão de uma tarefa.
        Verifica se a tarefa foi removida corretamente da lista de tarefas.
        """
        resultado, tarefa_temporaria = create_tarefa("Tarefa a ser deletada", "Pendente", 4, 104)
        resultado, tarefa = delete_tarefa(tarefa_temporaria["id_tarefa"])
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(tarefa["descricao"], "Tarefa a ser deletada")
        self.assertNotIn(tarefa, lista_tarefas)

    def test_delete_tarefa_inexistente(self):
        """
        Testa a exclusão de uma tarefa inexistente.
        Espera-se que o código de erro DADO_NÃO_ENCONTRADO seja retornado.
        """
        resultado, mensagem = delete_tarefa(9999)
        self.assertEqual(resultado, DADO_NÃO_ENCONTRADO)
        self.assertEqual(mensagem, {})

    def test_set_status_success(self):
        """
        Testa a alteração do status de uma tarefa.
        Verifica se o status foi atualizado corretamente.
        """
        resultado, tarefa_temporaria = create_tarefa("Atualizar status", "Pendente", 5, 105)
        resultado, tarefa = set_status(tarefa_temporaria["id_tarefa"], "Concluído")
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(tarefa["status"], "Concluído")

    def test_set_status_id_inexistente(self):
        """
        Testa a alteração de status para uma tarefa que não existe.
        Espera-se que o código de erro DADO_NÃO_ENCONTRADO seja retornado.
        """
        resultado, mensagem = set_status(9999, "Concluído")
        self.assertEqual(resultado, DADO_NÃO_ENCONTRADO)
        self.assertEqual(mensagem, {})

    def test_get_tarefas_by_prioridade_success(self):
        """
        Testa a recuperação de tarefas por prioridade.
        Verifica se tarefas com a prioridade correta são retornadas.
        """
        create_tarefa("Tarefa prioridade alta", "Em andamento", 1, 106)
        resultado, tarefas = get_tarefas_by_prioridade(1)
        self.assertEqual(resultado, STATUS_OK)
        self.assertTrue(len(tarefas) > 0)

    def test_get_tarefas_by_prioridade_inexistente(self):
        """
        Testa a recuperação de tarefas por uma prioridade inexistente.
        Espera-se que o código de erro DADO_NÃO_ENCONTRADO seja retornado.
        """
        resultado, tarefas = get_tarefas_by_prioridade(9999)
        self.assertEqual(resultado, DADO_NÃO_ENCONTRADO)
        self.assertEqual(tarefas, [])

    def test_get_tarefas_by_projeto_success(self):
        """
        Testa a recuperação de tarefas por projeto.
        Verifica se as tarefas vinculadas ao projeto correto são retornadas.
        """
        create_tarefa("Tarefa vinculada", "Em andamento", 2, 107)
        resultado, tarefas = get_tarefas_by_projeto(107)
        self.assertEqual(resultado, STATUS_OK)
        self.assertTrue(len(tarefas) > 0)

    def test_get_tarefas_by_projeto_inexistente(self):
        """
        Testa a recuperação de tarefas por projeto inexistente.
        Espera-se que o código de erro DADO_NÃO_ENCONTRADO seja retornado.
        """
        resultado, tarefas = get_tarefas_by_projeto(9999)
        self.assertEqual(resultado, DADO_NÃO_ENCONTRADO)
        self.assertEqual(tarefas, [])

if __name__ == "__main__":
    unittest.main()
