import unittest
from pertence import (
    attach_equipe, detach_equipe, get_equipe_from_projeto, get_projetos_from_equipe, reset_relacoes
)

# Códigos de erro
STATUS_OK = 0
DADOS_INVALIDOS = 1
CONFLITO = 3
DADO_NAO_ENCONTRADO = 4

class TestPertenceFunctions(unittest.TestCase):

    def setUp(self):
        reset_relacoes()

    def test_attach_equipe_success(self):
        resultado, relacao = attach_equipe(1, 1)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(relacao["id_projeto"], 1)
        self.assertEqual(relacao["id_equipe"], 1)

    def test_attach_equipe_conflito(self):
        attach_equipe(1, 1)
        resultado, mensagem = attach_equipe(1, 1)
        self.assertEqual(resultado, CONFLITO)
        self.assertEqual(mensagem, "Equipe já associada ao projeto.")

    def test_attach_equipe_dados_invalidos(self):
        resultado, mensagem = attach_equipe("projeto", 1)
        self.assertEqual(resultado, DADOS_INVALIDOS)
        self.assertEqual(mensagem, "IDs inválidos.")

    def test_detach_equipe_success(self):
        attach_equipe(1, 2)
        resultado, relacao = detach_equipe(1, 2)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(relacao["id_equipe"], 2)

    def test_detach_equipe_nao_encontrada(self):
        resultado, mensagem = detach_equipe(99, 99)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
        self.assertEqual(mensagem, "Associação não encontrada.")

    def test_get_equipe_from_projeto_success(self):
        attach_equipe(2, 3)
        resultado, equipes = get_equipe_from_projeto(2)
        self.assertEqual(resultado, STATUS_OK)
        self.assertIn(3, equipes)

    def test_get_equipe_from_projeto_nao_encontrado(self):
        resultado, mensagem = get_equipe_from_projeto(99)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
        self.assertEqual(mensagem, "Nenhuma equipe associada ao projeto.")

    def test_get_projetos_from_equipe_success(self):
        attach_equipe(3, 4)
        resultado, projetos = get_projetos_from_equipe(4)
        self.assertEqual(resultado, STATUS_OK)
        self.assertIn(3, projetos)

    def test_get_projetos_from_equipe_nao_encontrado(self):
        resultado, mensagem = get_projetos_from_equipe(99)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
        self.assertEqual(mensagem, "Nenhum projeto associado à equipe.")


if __name__ == "__main__":
    unittest.main()
