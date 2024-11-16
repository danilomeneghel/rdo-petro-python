import mysql.connector
from tkinter import messagebox
import logging

# Configuração do logger
logger = logging.getLogger('DataPersister')
logger.setLevel(logging.INFO)

class DataPersister:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        return mysql.connector.connect(
            host="localhost",
            database="rdo_petro",
            user="root",
            password=""
        )

    def persist_data(self, rdo_entity, rdo_contract_entity):
        if self.connection is None:
            logger.info("Falha ao estabelecer conexão com o banco de dados.")
            messagebox.showerror("Erro", "Falha ao estabelecer conexão com o banco de dados.")
            return

        # Verifica se o RDO já existe no banco
        if self.is_rdo_exists(rdo_entity.nro_rdo):
            logger.error(f"O RDO com o número {rdo_entity.nro_rdo} já foi importado.")
            messagebox.showwarning("Erro - Duplicação de RDO", f"O RDO com o número {rdo_entity.nro_rdo} já foi importado.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO rdo (data, nro_rdo) VALUES (%s, %s)", (rdo_entity.data, rdo_entity.nro_rdo))
            self.connection.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            id_rdo = cursor.fetchone()[0]

            self.insert_contract_data(id_rdo, rdo_contract_entity)
            messagebox.showinfo("Sucesso", "Dados importados com sucesso!")

        except mysql.connector.Error as e:
            logger.error(f"Erro ao persistir dados no banco: {e}")
            messagebox.showerror("Erro", "Erro ao persistir os dados no banco.")
        finally:
            if self.connection:
                self.connection.close()

    def insert_contract_data(self, id_rdo, rdo_contract_entity):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO rdo_contrato (id_rdo, inicio_contrato, termino_contrato, nro_contrato) VALUES (%s, %s, %s, %s)",
            (id_rdo, rdo_contract_entity.inicio_contrato, rdo_contract_entity.termino_contrato, rdo_contract_entity.nro_contrato)
        )
        self.connection.commit()

    def is_rdo_exists(self, nro_rdo):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM rdo WHERE nro_rdo = %s", (nro_rdo,))
        result = cursor.fetchone()
        return result[0] > 0
