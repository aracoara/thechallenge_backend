import logging
import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*utcfromtimestamp.*", category=DeprecationWarning)


def pytest_configure(config):
    # Diretório base onde conftest.py está localizado
    base_dir = os.path.dirname(__file__)

    # Caminho absoluto para o arquivo de log geral
    log_file_path = os.path.join(base_dir, 'app.log')
    # Caminho absoluto para o arquivo de log de erros
    error_log_file_path = os.path.join(base_dir, 'error.log')  # Esta é a correção

    # Configurações básicas do logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    # Cria um FileHandler para escrever logs em um arquivo
    log_file_handler = logging.FileHandler(log_file_path, mode='a')
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
    
    # Cria um FileHandler específico para erros
    error_log_file_handler = logging.FileHandler(error_log_file_path, mode='a')  # Corrigido para usar o caminho correto
    error_log_file_handler.setLevel(logging.ERROR)
    error_log_file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))

    # Adiciona os FileHandlers ao logger raiz
    logger = logging.getLogger()
    logger.addHandler(log_file_handler)
    logger.addHandler(error_log_file_handler)

def pytest_exception_interact(node, call, report):
    logger = logging.getLogger(__name__)
    if report.failed:
        logger.error(f"Erro no teste: {report.longreprtext}")    

