import tkinter as tk
from tkinter import ttk, messagebox
import logging
import mysql.connector
from datetime import datetime

# Configuração do logger
logger = logging.getLogger('DataDisplay')
logger.setLevel(logging.INFO)

class DataDisplay:
    def __init__(self, root):
        self.root = root
        self.panel = tk.Frame(self.root)
        self.panel.pack(fill='both', expand=True)

        # Título
        title_label = tk.Label(self.panel, text="Listar Dados RDO", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Filtro de busca
        filter_frame = tk.Frame(self.panel)
        filter_frame.pack(pady=10)

        self.filter_value = tk.Entry(filter_frame, width=25)
        self.filter_value.pack(side="left", padx=5)

        # Atualizando os rótulos do ComboBox para exibir "Nro RDO", "Data RDO" e "Nro Contrato"
        self.filter_type = ttk.Combobox(filter_frame, values=["Nro RDO", "Data RDO", "Nro Contrato"], width=15)
        self.filter_type.set("Nro RDO")  # Valor padrão
        self.filter_type.pack(side="left", padx=5)

        self.search_button = tk.Button(filter_frame, text="Buscar", command=self.load_data)
        self.search_button.pack(side="left", padx=5)

        # Tabela
        self.tree = ttk.Treeview(self.panel, columns=("Nro RDO", "Data RDO", "Nro Contrato", "Início Contrato", "Término Contrato"), show="headings")
        self.tree.pack(fill='both', expand=True)

        # Definindo o tamanho das colunas para apertar mais
        self.tree.column("Nro RDO", width=100, anchor="center")
        self.tree.column("Data RDO", width=100, anchor="center")
        self.tree.column("Nro Contrato", width=120, anchor="center")
        self.tree.column("Início Contrato", width=120, anchor="center")
        self.tree.column("Término Contrato", width=120, anchor="center")

        # Definindo os cabeçalhos
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)

    def format_date(self, date_value):
        """
        Converte uma data para o formato DD/MM/YYYY
        """
        if isinstance(date_value, str):
            # Tenta converter string no formato "YYYY-MM-DD" para "DD/MM/YYYY"
            try:
                date_obj = datetime.strptime(date_value, "%Y-%m-%d")
                return date_obj.strftime("%d/%m/%Y")
            except ValueError:
                return date_value  # Retorna o valor sem alterações se não for uma data válida
        elif isinstance(date_value, datetime):
            return date_value.strftime("%d/%m/%Y")  # Converte datetime para o formato desejado
        return date_value  # Se for outro tipo, retorna sem alterações

    def load_data(self):
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        filter_value = self.filter_value.get().strip()
        filter_type = self.filter_type.get()

        # Mapeamento entre o valor legível do ComboBox e o nome da coluna no banco de dados
        filter_mapping = {
            "Nro RDO": "r.nro_rdo",
            "Data RDO": "r.data",
            "Nro Contrato": "rc.nro_contrato"
        }

        connection = None
        try:
            connection = self.connect()
            if connection is None:
                logger.info("Falha ao estabelecer conexão com o banco de dados.")
                messagebox.showerror("Erro", "Falha ao estabelecer conexão com o banco de dados.")
                return

            cursor = connection.cursor(dictionary=True)

            # Se o valor do filtro for fornecido, ajusta a consulta
            if filter_value:
                query = f"""
                    SELECT r.nro_rdo, r.data, rc.nro_contrato, rc.inicio_contrato, rc.termino_contrato
                    FROM rdo r
                    JOIN rdo_contrato rc ON r.id = rc.id_rdo
                    WHERE {filter_mapping[filter_type]} = %s
                """
                cursor.execute(query, (filter_value,))
            else:
                query = """
                    SELECT r.nro_rdo, r.data, rc.nro_contrato, rc.inicio_contrato, rc.termino_contrato
                    FROM rdo r
                    JOIN rdo_contrato rc ON r.id = rc.id_rdo
                """
                cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                # Converte as datas para o formato DD/MM/YYYY antes de adicionar na tabela
                data_rdo = self.format_date(row["data"])
                inicio_contrato = self.format_date(row["inicio_contrato"])
                termino_contrato = self.format_date(row["termino_contrato"])

                # Insere os dados formatados na tabela
                self.tree.insert("", "end", values=(
                    row["nro_rdo"],
                    data_rdo,  # Data formatada
                    row["nro_contrato"],
                    inicio_contrato,  # Início contrato formatado
                    termino_contrato   # Término contrato formatado
                ))

        except mysql.connector.Error as e:
            logger.error(f"Erro ao carregar os dados: {e}")
            messagebox.showerror("Erro", "Erro ao carregar os dados.")
        finally:
            if connection:
                connection.close()

    def connect(self):
        return mysql.connector.connect(
            host="localhost",
            database="rdo_petro",
            user="root",
            password=""
        )

def show_data_display(frame):
    """Exibe a tela de listagem de dados"""
    data_display = DataDisplay(frame)
    data_display.load_data()
    data_display.panel.pack(fill="both", expand=True)
