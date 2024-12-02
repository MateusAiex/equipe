import os
import subprocess
import unittest
from unittest.mock import patch, mock_open
from compactador import descompacta, compacta

STATUS_OK = 0
ARQUIVO_TEXTO_NAO_ENCONTRADO = 12
ERRO_CRIAR_ARQUIVO_BINARIO = 13
ARQUIVO_BINARIO_NAO_ENCONTRADO = 14
ERRO_CRIAR_ARQUIVO_TEXTO = 15


class TesteCompactadora(unittest.TestCase):
  
  @patch("os.path.exists")
  @patch("subprocess.run")
  @patch("os.rename")
  def test_compacta_success(self, mock_rename, mock_run, mock_exists):
    '''
    Testa a função compacta com sucesso
    
    A função compacta deve chamar o subprocesso compactador_unix com o arquivo de texto e renomear o arquivo binário gerado
    '''
    mock_exists.side_effect = lambda x: True
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)

    result, message = compacta("arquivo.json", "arquivo.bin")

    mock_run.assert_called_once_with([os.path.join(os.path.dirname(os.path.realpath(__file__)), "compactador_unix"), "arquivo.json"], check=True)
    mock_rename.assert_called_once_with("arquivo.json.bin", "arquivo.bin")
    self.assertEqual(result, STATUS_OK)
    self.assertEqual(message, "Sucesso")

  @patch("os.path.exists")
  def test_compacta_text_not_found(self, mock_exists):
    '''
    Testa a função compacta com arquivo de texto não encontrado
    
    A função compacta deve retornar ARQUIVO_TEXTO_NAO_ENCONTRADO e a mensagem "Arquivo de texto não encontrado"'''
    mock_exists.side_effect = lambda x: False

    result, message = compacta("arquivo.json", "arquivo.bin")

    self.assertEqual(result, ARQUIVO_TEXTO_NAO_ENCONTRADO)
    self.assertEqual(message, "Arquivo de texto não encontrado")

  @patch("os.path.exists")
  @patch("subprocess.run")
  def test_compacta_subprocess_error(self, mock_run, mock_exists):
    '''
    Testa a função compacta com erro no subprocesso
    
    A função compacta deve retornar ERRO_CRIAR_ARQUIVO_BINARIO e a mensagem "Erro ao criar arquivo binário: Command '[]' returned non-zero exit status 1."'''
    
    mock_exists.side_effect = lambda x: True
    mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd=[])

    result, message = compacta("arquivo.json", "arquivo.bin")

    self.assertEqual(result, ERRO_CRIAR_ARQUIVO_BINARIO)
    self.assertEqual(message, "Erro ao criar arquivo binário: Command '[]' returned non-zero exit status 1.")

  @patch("os.path.exists")
  @patch("subprocess.run")
  def test_compacta_unknown_error(self, mock_run, mock_exists):
    '''
    
    Testa a função compacta com erro desconhecido
    
    A função compacta deve retornar ERRO_CRIAR_ARQUIVO_BINARIO e a mensagem "Erro ao criar arquivo binário: Unknown error"'''
    mock_exists.side_effect = lambda x: True
    e = "Unknown error"
    mock_run.side_effect = Exception(e)

    result, message = compacta("arquivo.json", "arquivo.bin")

    self.assertEqual(result, ERRO_CRIAR_ARQUIVO_BINARIO)
    self.assertEqual(message, f"Erro ao criar arquivo binário: {e}")

  @patch("os.path.exists")
  @patch("subprocess.run")
  @patch("os.rename")
  def test_descompacta_success(self, mock_rename, mock_run, mock_exists):
    '''
    
    Testa a função descompacta com sucesso
    
    A função descompacta deve chamar o subprocesso compactador_unix com o arquivo binário e renomear o arquivo de texto gerado'''
    
    mock_exists.side_effect = lambda x: True
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)

    result, message = descompacta("arquivo.bin", "arquivo.json")

    mock_run.assert_called_once_with([os.path.join(os.path.dirname(os.path.realpath(__file__)), "compactador_unix"), "arquivo.bin"], check=True)
    mock_rename.assert_called_once_with("arquivo.json", "arquivo.json")
    self.assertEqual(result, STATUS_OK)
    self.assertEqual(message, "Sucesso")

  @patch("os.path.exists")
  def test_descompacta_bin_not_found(self, mock_exists):
    '''
    Testa a função descompacta com arquivo binário não encontrado
    
    A função descompacta deve retornar ARQUIVO_BINARIO_NAO_ENCONTRADO e a mensagem "Arquivo binário não encontrado"'''
    mock_exists.side_effect = lambda x: False

    result, message = descompacta("arquivo.bin", "arquivo.json")

    self.assertEqual(result, ARQUIVO_BINARIO_NAO_ENCONTRADO)
    self.assertEqual(message, "Arquivo binário não encontrado")

  @patch("os.path.exists")
  @patch("subprocess.run")
  def test_descompacta_subprocess_error(self, mock_run, mock_exists):
    '''
    Testa a função descompacta com erro no subprocesso
    
    A função descompacta deve retornar ERRO_CRIAR_ARQUIVO_TEXTO e a mensagem "Erro desconhecido: Command '[]' returned non-zero exit status 1."'''
    mock_exists.side_effect = lambda x: True
    mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd=[])

    result, message = descompacta("arquivo.bin", "arquivo.json")

    self.assertEqual(result, ERRO_CRIAR_ARQUIVO_TEXTO)
    self.assertEqual(message, "Erro desconhecido: Command '[]' returned non-zero exit status 1.")

  @patch("os.path.exists")
  @patch("subprocess.run")
  def test_descompacta_unknown_error(self, mock_run, mock_exists):
    '''
    Testa a função descompacta com erro desconhecido
    
    A função descompacta deve retornar ERRO_CRIAR_ARQUIVO_TEXTO e a mensagem "Erro desconhecido: Unknown error"'''
    
    mock_exists.side_effect = lambda x: True
    e = "Unknown error"
    mock_run.side_effect = Exception(e)

    result, message = descompacta("arquivo.bin", "arquivo.json")

    self.assertEqual(result, ERRO_CRIAR_ARQUIVO_TEXTO)
    self.assertEqual(message, f"Erro desconhecido: {e}")

if __name__ == "__main__":
    unittest.main()