import mysql.connector
from mysql.connector import Error
import logging
from tkinter import messagebox

# Configuração do logger
logger = logging.getLogger('DatabaseConnection')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def connect():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='rdo_petro',
            user='root',
            password=''
        )
        logger.info("Conexão bem-sucedida ao banco de dados")
    except Error as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    return connection
