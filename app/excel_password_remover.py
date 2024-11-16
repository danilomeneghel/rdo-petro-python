import os
from datetime import datetime
from logger_config import logger
from app.convert_xlsm_to_csv import convert_xlsm_to_csv

class ExcelPasswordRemover:
    @staticmethod
    def convert_file(input_file):
        dir_planilha = "planilha/"
        current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{dir_planilha}rdo_sem_bloqueio_{current_date_time}.csv"

        try:
            convert_xlsm_to_csv(input_file, output_file)

            # Verifica se o arquivo foi criado com sucesso
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                with open(output_file, "r", encoding="ISO-8859-1") as file:
                    if file.readline() is None:
                        logger.error("O arquivo CSV está vazio.")
                        return None
                logger.info(f"Arquivo convertido com sucesso! Arquivo salvo em: {output_file}")
                return output_file
            else:
                logger.error("O arquivo convertido está vazio ou não foi encontrado.")
                return None

        except Exception as e:
            logger.error(f"Erro na conversão: {e}")
            return None
