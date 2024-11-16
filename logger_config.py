import logging
import os

# Função para configurar o logger
def setup_logger():
    """
    Configura o logger para registrar informações no console e em um arquivo.
    """
    # Criação do diretório para armazenar logs, caso não exista
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Definindo o nome do arquivo de log
    log_file = os.path.join(log_dir, 'app.log')

    # Configuração do formato dos logs
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Criação de um handler para o arquivo de log
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Criação de um handler para o console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))

    # Configuração do logger com ambos os handlers
    logger = logging.getLogger('DataDisplay')
    logger.setLevel(logging.INFO)  # Define o nível global para INFO
    logger.addHandler(file_handler)  # Adiciona o handler do arquivo
    logger.addHandler(console_handler)  # Adiciona o handler do console

    return logger

# Configuração do logger
logger = setup_logger()
