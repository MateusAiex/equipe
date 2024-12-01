import unittest
from projeto import (create_projeto, 
                    get_projetos, 
                    get_projetos_by_id, 
                    delete_projeto, 
                    lista_projetos)

# Códigos de erro
STATUS_OK = 0
DADOS_INVALIDOS = 1
CONFLITO = 3
DADO_NÃO_ENCONTRADO = 4

class TestProjetoFunctions(unittest.TestCase):

    def setUp(self):
        """
        Configuração inicial do teste. Reseta a lista de projetos e o ID provisório.
        """
        global lista_projetos, id_projeto_provisorio
        lista_projetos = []  # Garante que a lista comece vazia
        id_projeto_provisorio = 2420  # Reseta o ID provisório

    def test_create_projeto_success(self):
        """
        Testa a criação de um projeto com dados válidos.
        """
        resultado, projeto = create_projeto("Projeto A", "Descrição do Projeto A", (31, 12, 2024))
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(projeto["titulo"], "Projeto A")
        self.assertEqual(projeto["descricao"], "Descrição do Projeto A")
        self.assertEqual(projeto["prazo"], (31, 12, 2024))

    def test_create_projeto_dados_invalidos(self):
        """
        Testa a criação de um projeto com dados inválidos (título e descrição vazios).
        """
        resultado, projeto = create_projeto("", "", (31, 12, 2024))
        self.assertEqual(resultado, DADOS_INVALIDOS)
        self.assertEqual(projeto, {})

    def test_get_projetos_success(self):
        """
        Testa a obtenção de todos os projetos.
        """
        create_projeto("Projeto B", "Descrição do Projeto B", (1, 1, 2025))
        resultado, projetos = get_projetos()
        self.assertEqual(resultado, STATUS_OK)
        self.assertTrue(len(projetos) > 0)

    def test_get_projetos_by_id_success(self):
        """
        Testa a obtenção de um projeto pelo seu ID.
        """
        _, projeto_temporario = create_projeto("Projeto C", "Descrição do Projeto C", (15, 5, 2025))
        resultado, projeto = get_projetos_by_id(projeto_temporario["id"])
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(projeto["titulo"], "Projeto C")

    def test_get_projetos_by_id_inexistente(self):
        """
        Testa a obtenção de um projeto por um ID inexistente.
        """
        resultado, projeto = delete_projeto(9999)
        self.assertEqual(resultado, DADO_NÃO_ENCONTRADO)
        self.assertEqual(projeto, {})

    def test_delete_projeto_success(self):
        """
        Testa a remoção de um projeto com ID válido.
        """
        _, projeto_temporario = create_projeto("Projeto D", "Descrição do Projeto D", (20, 8, 2025))
        resultado, projeto = delete_projeto(projeto_temporario["id"])
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(projeto["titulo"], "Projeto D")

    def test_delete_projeto_id_inexistente(self):
        """
        Testa a remoção de um projeto com ID inexistente.
        """
        resultado, projeto = delete_projeto(9999)
        self.assertEqual(resultado, DADO_NÃO_ENCONTRADO)
        self.assertEqual(projeto, {})

    

if __name__ == "__main__":
    unittest.main()
