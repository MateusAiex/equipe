import os
import subprocess
import sys
import stat

# Exportando funções do módulo
__all__ = ["compacta", "descompacta"]

STATUS_OK = 0
ARQUIVO_TEXTO_NAO_ENCONTRADO = 12
ERRO_CRIAR_ARQUIVO_BINARIO = 13
ARQUIVO_BINARIO_NAO_ENCONTRADO = 14
ERRO_CRIAR_ARQUIVO_TEXTO = 15

# Diretórios e caminhos globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
_COMPACTADOR_PATH: str

if os.name == "nt":
    _COMPACTADOR_PATH = os.path.join(_SCRIPT_DIR_PATH, "compactador_win.exe")
elif os.name == "posix":
    _COMPACTADOR_PATH = os.path.join(_SCRIPT_DIR_PATH, "compactador_unix")
    os.chmod(_COMPACTADOR_PATH, os.stat(_COMPACTADOR_PATH).st_mode | stat.S_IEXEC)
else:
    print(f"Sistema operacional {os.name} não suportado")
    sys.exit(1)

# Funções principais


def compacta(arquivo_json: str, arquivo_bin: str) -> int:
    """
    Compacta um arquivo JSON para BIN usando o compactador de Software Básico.
    """
    if not os.path.exists(arquivo_json):
        return ARQUIVO_TEXTO_NAO_ENCONTRADO, "Arquivo de texto não encontrado"  

    try:
        subprocess.run([_COMPACTADOR_PATH, arquivo_json], check=True)
        os.rename(arquivo_json + ".bin", arquivo_bin)
        return STATUS_OK, "Sucesso"  # Sucesso
    except subprocess.CalledProcessError as e:
        return ERRO_CRIAR_ARQUIVO_BINARIO, f"Erro ao criar arquivo binário: {e}"  # Erro ao criar arquivo binário
    except Exception as e:
        return ERRO_CRIAR_ARQUIVO_BINARIO, f"Erro ao criar arquivo binário: {e}"


def descompacta(arquivo_bin: str, arquivo_json: str) -> int:
    """
    Descompacta um arquivo BIN para JSON  usando o descompactador de Software Básico.
    """
    if not os.path.exists(arquivo_bin):
        return ARQUIVO_BINARIO_NAO_ENCONTRADO, "Arquivo binário não encontrado"  

    try:
        subprocess.run([_COMPACTADOR_PATH, arquivo_bin], check=True)
        os.rename(arquivo_bin.replace(".bin", ".json"), arquivo_json)
        return STATUS_OK, "Sucesso" 
    except subprocess.CalledProcessError as e:
        return ERRO_CRIAR_ARQUIVO_TEXTO, f"Erro desconhecido: {e}"  
    except Exception as e:
        return ERRO_CRIAR_ARQUIVO_TEXTO, f"Erro desconhecido: {e}"

