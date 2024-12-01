import unittest
from equipe import create_equipe, get_equipes, get_equipe_by_id, delete_equipe, delete_equipes

# Códigos de erro
OPERACAO_REALIZADA_COM_SUCESSO = 0
EQUIPE_NAO_ENCONTRADA = 1
DADOS_INVALIDOS = 2
NOME_DE_EQUIPE_JA_EXISTE = 3

class TestEquipeFunctions(unittest.TestCase):
    
    def test_create_equipe_success(self):
        delete_equipes()
        resultado, equipe = create_equipe("Equipe 1", ["Analista", "Consultor"])
        self.assertEqual(resultado, OPERACAO_REALIZADA_COM_SUCESSO)
        self.assertEqual(equipe["nome"], "Equipe 1")
        self.assertEqual(equipe["funcoes"], ["Analista", "Consultor"])

    def test_create_equipe_nome_vazio(self):
        resultado, mensagem = create_equipe("", ["Analista"])
        self.assertEqual(resultado, DADOS_INVALIDOS)
        self.assertEqual(mensagem, "Nome inválido")

    def test_create_equipe_funcoes_invalidas(self):
        resultado, mensagem = create_equipe("Equipe 1", [])
        self.assertEqual(resultado, DADOS_INVALIDOS)
        self.assertEqual(mensagem, "Funções inválidas")

    def test_create_equipe_ja_existente(self):
        create_equipe("Equipe 1", ["Analista"])
        resultado, mensagem = create_equipe("Equipe 1", ["Analista"])
        self.assertEqual(resultado, NOME_DE_EQUIPE_JA_EXISTE)
        self.assertEqual(mensagem, "Nome já existe")
    
    def test_delete_equipe_success(self):
        resultado, equipe_temporaria = create_equipe("Equipe 2", ["Gestora"])
        resultado, equipe = delete_equipe(equipe_temporaria["id"])
        self.assertEqual(resultado, OPERACAO_REALIZADA_COM_SUCESSO)
        self.assertEqual(equipe["nome"], "Equipe 2")

    def test_delete_equipe_id_inexistente(self):
        resultado, mensagem = delete_equipe(99)
        self.assertEqual(resultado, EQUIPE_NAO_ENCONTRADA)
        self.assertEqual(mensagem, "Membro não encontrado")

    def test_get_equipes_success(self):
        create_equipe("Equipe 3", ["Analista"])
        resultado, equipes = get_equipes()
        for equipe in equipes:
            print(equipe)
        self.assertEqual(resultado, OPERACAO_REALIZADA_COM_SUCESSO)
        self.assertEqual(len(equipes), 4)

    def test_get_equipe_by_id_success(self):
        create_equipe("Equipe 4", ["Analista"])
        resultado, equipe = get_equipe_by_id(1)
        self.assertEqual(resultado, OPERACAO_REALIZADA_COM_SUCESSO)
        self.assertEqual(equipe["nome"], "Equipe 1")

    def test_get_equipe_by_id_inexistente(self):
        create_equipe("Equipe 5", ["Analista"])
        resultado, equipe = get_equipe_by_id(99)
        self.assertEqual(resultado, EQUIPE_NAO_ENCONTRADA)
        self.assertEqual(equipe, "Equipe não encontrada")


if __name__ == '__main__':
    unittest.main()