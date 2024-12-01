import unittest
from pertence import (
    attach_equipe,
    detach_equipe,
    get_equipe_from_projetos,
    get_projetos_from_equipes,
)

# Códigos de erro
STATUS_OK = 0 
DADOS_INVALIDOS = 1
ERRO_AO_DELETAR = 2
CONFLITO = 3
DADO_NÃO_ENCONTRADO = 4
EQUIPE_NÃO_ASSOCIADA_AO_PROJETO = 10
EQUIPE_JÁ_ASSOCIADA_AO_PROJETO = 11

class TestPertenceFunctions(unittest.TestCase):

    def test_attach_equipe_success(self):
        """
        Testa a associação de uma equipe a um projeto com sucesso.
        """
        resultado, pertence = attach_equipe(2, 202)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(pertence["id_projeto"], 2)
        self.assertEqual(pertence["id_equipe"], 202)

    def test_attach_equipe_already_attached(self):
        """
        Testa o caso onde a equipe já está associada ao projeto.
        """
        attach_equipe(1, 101)
        resultado, _ = attach_equipe(1, 101)
        self.assertEqual(resultado, EQUIPE_JÁ_ASSOCIADA_AO_PROJETO)
    def test_detach_equipe_success(self):
        """
        Testa a remoção de uma equipe associada a um projeto com sucesso.
        """
        attach_equipe(1, 101)
        resultado, pertence = detach_equipe(1, 101)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(pertence["id_projeto"], 1)
        self.assertEqual(pertence["id_equipe"], 101)

    def test_detach_equipe_not_associated(self):
        """
        Testa o caso onde a equipe não está associada ao projeto.
        """
        resultado, _ = detach_equipe(1, 999)  # Tentando remover uma equipe não associada
        self.assertEqual(resultado, EQUIPE_NÃO_ASSOCIADA_AO_PROJETO)

    def test_get_equipe_from_projetos_success(self):
        """
        Testa a obtenção das equipes associadas a um projeto com sucesso.
        """
        attach_equipe(1, 101)
        attach_equipe(1, 102)
        resultado, equipes = get_equipe_from_projetos(1)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(len(equipes), 2)
    def test_get_projetos_from_equipes_no_association(self):
        """
        Testa a obtenção dos projetos de uma equipe que não está associada a nenhum projeto.
        """
        resultado, projetos = get_projetos_from_equipes(999)
        self.assertEqual(resultado, DADO_NÃO_ENCONTRADO)
        self.assertEqual(projetos, []) 

    def test_get_projetos_from_equipes_success(self):
        """
        Testa a obtenção dos projetos de uma equipe associada a vários projetos.
        """
        attach_equipe(1, 101)
        attach_equipe(2, 101)
        resultado, projetos = get_projetos_from_equipes(101)
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(len(projetos), 2)


if __name__ == "__main__":
    unittest.main() 
