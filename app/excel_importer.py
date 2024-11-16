import csv
from datetime import datetime
import logging
from tkinter import messagebox
from app.rdo_entities import RdoEntity, RdoContractEntity

# Configuração do logger
logger = logging.getLogger('ExcelImporter')
logger.setLevel(logging.INFO)

class ExcelImporter:
    def get_rdo_data(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

            date_string = rows[9][9]  # Altere o índice conforme a localização da data
            logger.info(f"Data RDO: {date_string}")

            if self.is_valid_date(date_string):
                rdo_data = self.parse_date(date_string)
                nro_rdo = self.parse_integer(rows[9][11])
                logger.info(f"Nro RDO: {nro_rdo}")

                return RdoEntity(rdo_data, nro_rdo)
            else:
                logger.error("Data inválida no arquivo CSV.")
                return None
        except Exception as e:
            logger.error(f"Erro inesperado ao processar o arquivo CSV: {e}")
            messagebox.showerror("Erro", "Erro inesperado ao processar o arquivo CSV.")
            return None

    def get_rdo_contract_data(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

            nro_contrato = rows[3][3]  # Altere o índice conforme a localização do contrato

            rdo_inicio_contrato = self.parse_date(rows[9][1])
            rdo_termino_contrato = self.parse_date(rows[9][6])

            return RdoContractEntity(rdo_inicio_contrato, rdo_termino_contrato, nro_contrato)
        except Exception as e:
            logger.error(f"Erro inesperado ao processar o arquivo CSV para contrato: {e}")
            messagebox.showerror("Erro", "Erro inesperado ao processar o arquivo CSV.")
            return None

    def is_valid_date(self, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def parse_date(self, value):
        return datetime.strptime(value, "%d/%m/%Y")

    def parse_integer(self, value):
        try:
            return int(value)
        except ValueError:
            return 0
