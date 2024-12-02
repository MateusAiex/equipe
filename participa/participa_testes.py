import unittest
from unittest.mock import patch
from participa import (
    lista_participacoes, set_lider, validate_unique_lider,
    assign_membro, check_team_roles, get_membros_from_equipe, get_equipe_from_membro,
    get_membros_by_id
)


STATUS_OK = 0
DADO_NAO_ENCONTRADO = 4
MULTIPLOS_LIDERES = 2
PAPEIS_INCOMPLETOS = 5
MEMBRO_JA_ATRIBUIDO = 7

class TestParticipaFunctions(unittest.TestCase):

    def setUp(self):
        """
        Configura o ambiente de testes inicializando a lista de participações 
        e criando um mock de membros.
        """
        global lista_participacoes
        lista_participacoes.clear()
        lista_participacoes.extend([
            {"id_equipe": 1, "id_membro": 1, "elider": False},
            {"id_equipe": 1, "id_membro": 2, "elider": False},
            {"id_equipe": 2, "id_membro": 3, "elider": False},
        ])
        self.mock_members = {
            1: {"id_membro": 1, "nome": "Membro 1"},
            2: {"id_membro": 2, "nome": "Membro 2"},
            3: {"id_membro": 3, "nome": "Membro 3"},
            10: {"id_membro": 10, "nome": "Membro 10"},
            20: {"id_membro": 20, "nome": "Membro 20"},
        }

    def mock_get_membros_by_id(self, id_membro):
        """
        Função mock para simular a busca de membros pelo ID.
        """
        membro = self.mock_members.get(id_membro)
        if membro:
            return STATUS_OK, membro
        return DADO_NAO_ENCONTRADO, None

    def test_set_lider(self):
        """
        Teste para verificar se a função set_lider está funcionando corretamente.
        """
        self.assertEqual(set_lider(1, 1), STATUS_OK)
        self.assertTrue(lista_participacoes[0]["elider"])

    def test_validate_unique_lider(self):
        """
        Teste para verificar a validação de líder único na equipe.
        """
        set_lider(1, 1)
        self.assertEqual(validate_unique_lider(1), STATUS_OK)
        set_lider(1, 2)
        self.assertEqual(validate_unique_lider(1), MULTIPLOS_LIDERES)
        self.assertEqual(validate_unique_lider(2), DADO_NAO_ENCONTRADO)

    def test_assign_membro_success(self):
        """
        Teste para verificar a atribuição de um membro à equipe com sucesso.
        """
        self.assertEqual(assign_membro(1, 10), STATUS_OK)

    def test_assign_membro_duplicate(self):
        """
        Teste para verificar se o erro MEMBRO_JA_ATRIBUIDO é retornado 
        quando o membro já está atribuído à equipe.
        """
        assign_membro(1, 20)
        self.assertEqual(assign_membro(1, 20), MEMBRO_JA_ATRIBUIDO)

    def test_team_with_all_roles(self):
        """
        Teste para verificar se a equipe tem todos os papéis necessários (pelo menos um líder).
        """
        set_lider(1, 1)
        self.assertEqual(check_team_roles(1), STATUS_OK)

    def test_team_with_missing_roles(self):
        """
        Teste para verificar se a equipe com papéis faltando retorna PAPEIS_INCOMPLETOS.
        """
        self.assertEqual(check_team_roles(2), PAPEIS_INCOMPLETOS)

    def test_nonexistent_team(self):
        """
        Teste para verificar se uma equipe inexistente retorna DADO_NAO_ENCONTRADO.
        """
        global lista_participacoes
        lista_participacoes.clear()
        self.assertEqual(check_team_roles(30), DADO_NAO_ENCONTRADO)

    @patch('participa.get_membros_by_id', side_effect=mock_get_membros_by_id)
    def test_get_membros_from_equipe(self, mock_get):
        """
        Teste para verificar se a função get_membros_from_equipe retorna os membros corretamente.
        """
        assign_membro(1, 1)
        assign_membro(1, 2)
        status, membros = get_membros_from_equipe(1)
        self.assertEqual(status, STATUS_OK)
        self.assertEqual(len(membros), 2)

    @patch('participa.get_membros_by_id', side_effect=mock_get_membros_by_id)
    def test_get_equipe_from_membro(self, mock_get):
        """
        Teste para verificar se a função get_equipe_from_membro retorna a equipe corretamente.
        """
        assign_membro(1, 1)
        status, equipe = get_equipe_from_membro(1)
        self.assertEqual(status, STATUS_OK)
        self.assertEqual(equipe, 1)

if __name__ == "__main__":
    unittest.main()
