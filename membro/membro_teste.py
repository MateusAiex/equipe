
import unittest
from membro import create_membro, delete_membro, set_funcoes, get_membro_by_id, get_membros, lista_membros

# Definições dos códigos de erro
STATUS_OK = 0
DADOS_INVALIDOS = 1
ERRO_AO_DELETAR = 2
CONFLITO = 3
DADO_NAO_ENCONTRADO = 4

class TestMembroFunctions(unittest.TestCase):
    def setUp(self):
        # Limpar lista_membros para cada teste
        global lista_membros
        lista_membros.clear()

    def test_create_membro_success(self):
        '''
        Testa a função create_membro com sucesso
        '''
        resultado, membro = create_membro("João", ["Analista", "Consultor"])
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(membro["nome"], "João")
        self.assertEqual(membro["funcoes"], ["Analista", "Consultor"])

    def test_create_membro_nome_vazio(self):
        '''
        Testa a função create_membro com nome vazio
        '''
        resultado, mensagem = create_membro("", ["Analista"])
        self.assertEqual(resultado, DADOS_INVALIDOS)
        self.assertEqual(mensagem, "Nome inválido")

    def test_create_membro_funcoes_invalidas(self):
        '''
        Testa a função create_membro com funções inválidas
        '''
        resultado, mensagem = create_membro("João", [])
        self.assertEqual(resultado, DADOS_INVALIDOS)
        self.assertEqual(mensagem, "Funções inválidas")

    def test_create_membro_ja_existente(self):
        '''
        Testa a função create_membro com membro já existente
        '''
        create_membro("João", ["Analista"])
        resultado, mensagem = create_membro("João", ["Analista"])
        self.assertEqual(resultado, CONFLITO)
        self.assertEqual(mensagem, "Membro já existente")

    def test_delete_membro_success(self):
        '''
        Testa a função delete_membro com sucesso
        '''
        resultado, membro_temporario = create_membro("Maria", ["Gestora"])
        resultado, membro = delete_membro(membro_temporario["id"])
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(membro["nome"], "Maria")

    def test_delete_membro_id_inexistente(self):
        '''
        Testa a função delete_membro com id inexistente
        '''
        resultado, mensagem = delete_membro(99)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
        self.assertEqual(mensagem, "Membro não encontrado")

    def test_set_funcoes_success(self):
        '''
        Testa a função set_funcoes com sucesso
        '''
        create_membro("Carlos", ["Analista"])
        resultado, membro = set_funcoes(1, ["Gerente"])
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(membro["funcoes"], ["Gerente"])

    def test_set_funcoes_id_inexistente(self):
        '''
        Testa a função set_funcoes com id inexistente
        '''
        resultado, mensagem = set_funcoes(99, ["Gerente"])
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
        self.assertEqual(mensagem, "Membro não encontrado")

    def test_set_funcoes_funcoes_invalidas(self):
        '''
        Testa a função set_funcoes com funções inválidas
        '''
        resultado, membro = create_membro("Ana", ["Consultora"])
        resultado, mensagem = set_funcoes(membro["id"], [])
        self.assertEqual(resultado, DADOS_INVALIDOS)
        self.assertEqual(mensagem, "Funções inválidas")

    def test_get_membros_success(self):
        '''
        Testa a função get_membros com sucesso
        '''
        create_membro("Lucas", ["Designer"])
        resultado, membros = get_membros()
        self.assertEqual(resultado, STATUS_OK)
        self.assertTrue(len(membros) > 0)

    def test_get_membro_by_id_success(self):
        '''
        Testa a função get_membro_by_id com sucesso
        '''
        resultado, membro_temporario = create_membro("Beatriz", ["Arquiteta"])
        resultado, membro = get_membro_by_id(membro_temporario["id"])
        self.assertEqual(resultado, STATUS_OK)
        self.assertEqual(membro["nome"], "Beatriz")

    def test_get_membro_by_id_inexistente(self):
        '''
        Testa a função get_membro_by_id com id inexistente
        '''
        resultado, mensagem = get_membro_by_id(99)
        self.assertEqual(resultado, DADO_NAO_ENCONTRADO)
        self.assertEqual(mensagem, "Membro não encontrado")

if __name__ == "__main__":
    unittest.main()
