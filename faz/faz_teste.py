import unittest
from unittest.mock import patch
from faz import assign_tarefa, get_tarefas_by_membro, get_membro_by_tarefa, lista_faz

STATUS_OK = 0
DADO_NAO_ENCONTRADO = 4
CONFLITO = 3
DADOS_INVALIDOS = 1
TAREFA_JA_ATRIBUIDA = 8

class TestFazFunctions(unittest.TestCase):

    def setUp(self):
        # Limpar lista_faz para cada teste
        global lista_faz
        lista_faz.clear()

    @patch('tarefa.get_tarefa_by_id')
    @patch('membro.get_membro_by_id')
    def test_assign_tarefa_success(self, mock_get_tarefa_by_id, mock_get_membro_by_id):
        '''
        Testa a função assign_tarefa com sucesso
        '''
        mock_get_membro_by_id.return_value = (STATUS_OK, {"id": 1, "nome": "João"})
        mock_get_tarefa_by_id.return_value = (STATUS_OK, {"id": 1, "descricao": "Tarefa 1", "status": "Aberta"})
        resultado, faz = assign_tarefa(1, 1, mock_get_membro_by_id, mock_get_tarefa_by_id)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(faz["id_membro"], 1)
        self.assertEqual(faz["id_tarefa"], 1)

    @patch('tarefa.get_tarefa_by_id')
    @patch('membro.get_membro_by_id')
    def test_assign_tarefa_id_tarefa_inexistente(self, mock_get_tarefa_by_id, mock_get_membro_by_id):
        '''
        Testa a função assign_tarefa com tarefa inexistente
        '''
        mock_get_membro_by_id.return_value = (STATUS_OK, {"id": 1, "nome": "João"})
        mock_get_tarefa_by_id.return_value = (DADO_NAO_ENCONTRADO, "Tarefa não encontrada")
        resultado, mensagem = assign_tarefa(1, 99, mock_get_membro_by_id, mock_get_tarefa_by_id)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)

    @patch('tarefa.get_tarefa_by_id')
    @patch('membro.get_membro_by_id')
    def test_assign_tarefa_id_membro_inexistente(self, mock_get_tarefa_by_id, mock_get_membro_by_id):
        '''
        Testa a função assign_tarefa com membro inexistente
        '''
        mock_get_membro_by_id.return_value = (DADO_NAO_ENCONTRADO, "Membro não encontrado")
        mock_get_tarefa_by_id.return_value = (STATUS_OK, {"id": 1, "descricao": "Tarefa 1", "status": "Aberta"})
        resultado, mensagem = assign_tarefa(99, 1, mock_get_membro_by_id, mock_get_tarefa_by_id)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)

    @patch('tarefa.get_tarefa_by_id')
    @patch('membro.get_membro_by_id')
    def test_assign_tarefa_tarefa_ja_atribuida(self, mock_get_tarefa_by_id, mock_get_membro_by_id):
        '''
        Testa a função assign_tarefa com tarefa já atribuída
        '''
        mock_get_membro_by_id.return_value = (STATUS_OK, {"id": 1, "nome": "João"})
        mock_get_tarefa_by_id.side_effect = [
            (STATUS_OK, {"id": 1, "descricao": "Tarefa 1", "status": "Aberta"}),
            (STATUS_OK, {"id": 1, "descricao": "Tarefa 1", "status": "Aberta"})
        ]
        assign_tarefa(1, 1, mock_get_membro_by_id, mock_get_tarefa_by_id)
        resultado, mensagem = assign_tarefa(2, 1, mock_get_membro_by_id, mock_get_tarefa_by_id)
        self.assertEqual(resultado, TAREFA_JA_ATRIBUIDA)

    @patch('tarefa.get_tarefa_by_id')
    @patch('membro.get_membro_by_id')
    def test_assign_tarefa_membro_tarefa_nao_concluida(self, mock_get_tarefa_by_id, mock_get_membro_by_id):
        '''
        Testa a função assign_tarefa com membro com tarefa não concluída
        '''
        # Simula membro com tarefa não concluída
        mock_get_membro_by_id.return_value = (STATUS_OK, {"id": 1, "nome": "João"})
        mock_get_tarefa_by_id.return_value = (STATUS_OK, {"id": 1, "descricao": "Tarefa 1", "status": "Aberta"})
        assign_tarefa(1, 1, mock_get_membro_by_id, mock_get_tarefa_by_id)
        mock_get_tarefa_by_id.return_value = (STATUS_OK, {"id": 2, "descricao": "Tarefa 2", "status": "Aberta"})
        resultado, mensagem = assign_tarefa(1, 2, mock_get_membro_by_id, mock_get_tarefa_by_id)
        self.assertEqual(resultado, CONFLITO)
        self.assertEqual(mensagem, "Membro já possui uma tarefa em andamento")

    @patch('tarefa.get_tarefas')
    @patch('membro.get_membro_by_id')
    @patch('tarefa.get_tarefa_by_id')
    def test_get_tarefas_by_membro_success(self, mock_get_tarefas, mock_get_membro_by_id, mock_get_tarefa_by_id):
        '''
        Testa a função get_tarefas_by_membro com sucesso
        '''
        mock_get_membro_by_id.return_value = (STATUS_OK, {"id": 1, "nome": "João"})
        mock_get_tarefas.return_value = (STATUS_OK, [{"id": 1, "descricao": "Tarefa 1", "status": "Aberta"}, {"id": 2, "descricao": "Tarefa 2", "status": "Fechada"}, {"id": 3, "descricao": "Tarefa 3", "status": "Aberta"}])
        mock_get_tarefa_by_id.return_value = (STATUS_OK, {"id": 1, "descricao": "Tarefa 1", "status": "Aberta"})
        assign_tarefa(1, 1, mock_get_membro_by_id, mock_get_tarefa_by_id)
        resultado, tarefas = get_tarefas_by_membro(1, mock_get_membro_by_id, mock_get_tarefas)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(len(tarefas), 1)
        self.assertEqual(tarefas[0]["id"], 1)
    
    @patch('membro.get_membro_by_id')
    @patch('tarefa.get_tarefas')
    def test_get_tarefas_by_membro_inexistente(self, mock_get_tarefas, mock_get_membro_by_id):
        '''
        Testa a função get_tarefas_by_membro com membro inexistente
        '''
        mock_get_membro_by_id.return_value = (DADO_NAO_ENCONTRADO, "Membro não encontrado")
        mock_get_tarefas.return_value = (STATUS_OK, [{"id": 1, "descricao": "Tarefa 1", "status": "Fechada"}, {"id": 2, "descricao": "Tarefa 2", "status": "Aberta"}])
        resultado, mensagem = get_tarefas_by_membro(99, mock_get_membro_by_id, mock_get_tarefas)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
        
    @patch('membro.get_membro_by_id')
    @patch('tarefa.get_tarefa_by_id')
    def test_get_membro_by_tarefa_success(self, mock_get_tarefa_by_id, mock_get_membro_by_id):
        '''
        Testa a função get_membro_by_tarefa com sucesso
        '''
        mock_get_membro_by_id.return_value = (STATUS_OK, {"id": 1, "nome": "João"})
        mock_get_tarefa_by_id.return_value = (STATUS_OK, {"id": 1, "descricao": "Tarefa 1", "status": "Aberta"})
        assign_tarefa(1, 1, mock_get_membro_by_id, mock_get_tarefa_by_id)
        resultado, membro = get_membro_by_tarefa(1, mock_get_tarefa_by_id, mock_get_membro_by_id)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(membro[1]["id"], 1)
        
    @patch('tarefa.get_tarefa_by_id')
    def test_get_membro_by_tarefa_inexistente(self, mock_get_tarefa_by_id):
        '''
        Testa a função get_membro_by_tarefa com tarefa inexistente
        '''
        mock_get_tarefa_by_id.return_value = (DADO_NAO_ENCONTRADO, "Tarefa não encontrada")
        resultado, mensagem = get_membro_by_tarefa(99, mock_get_tarefa_by_id, lambda x: (DADO_NAO_ENCONTRADO, "Membro não encontrado"))
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
    
    @patch('tarefa.get_tarefa_by_id')
    @patch('membro.get_membro_by_id')
    def test_get_membro_by_tarefa_tarefa_nao_atribuida(self, mock_get_tarefa_by_id, mock_get_membro_by_id):
        '''
        Testa a função get_membro_by_tarefa com tarefa não atribuída
        '''
        mock_get_membro_by_id.return_value = (STATUS_OK, {"id": 1, "nome": "João"})
        mock_get_tarefa_by_id.return_value = (STATUS_OK, {"id": 1, "descricao": "Tarefa 1", "status": "Aberta"})
        resultado, mensagem = get_membro_by_tarefa(1, mock_get_tarefa_by_id, mock_get_membro_by_id)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
    
    
if __name__ == "__main__":
    unittest.main()
