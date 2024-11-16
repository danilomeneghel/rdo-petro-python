import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime
import mysql.connector

# Configuração do logger
logger = logging.getLogger('DataDisplay')
logger.setLevel(logging.INFO)

class DataDisplay:
    def __init__(self, root, db_connection):
        self.root = root
        self.db_connection = db_connection
        self.panel = tk.Frame(self.root)
        self.panel.pack(fill='both', expand=True)

        # Título
        title_label = tk.Label(self.panel, text="Listar Dados RDO", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Filtro de busca
        filter_frame = tk.Frame(self.panel)
        filter_frame.pack(pady=10)

        # Filtro de valor
        self.filter_value = tk.Entry(filter_frame, width=25)
        self.filter_value.pack(side="left", padx=5)

        # Filtro de tipo
        self.filter_type = ttk.Combobox(filter_frame, values=["Nro RDO", "Data RDO", "Nro Contrato"], width=15)
        self.filter_type.set("Nro RDO")  # Valor padrão
        self.filter_type.pack(side="left", padx=5)

        # Botão de busca
        self.search_button = tk.Button(filter_frame, text="Buscar", command=self.load_data, bg="#4CAF50", fg="white")
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

        # Variáveis de paginação
        self.current_page = 1
        self.records_per_page = 20  # Alterado para 20 registros por página
        self.total_records = 0
        self.total_pages = 0
        self.filter_value_text = ""
        self.filter_type_text = "Nro RDO"

        # Barra de navegação (rodapé da tabela)
        self.pagination_frame = tk.Frame(self.panel)
        self.pagination_frame.pack(pady=10)

        self.prev_button = tk.Button(self.pagination_frame, text="<< Anterior", command=self.previous_page, state="disabled")
        self.prev_button.pack(side="left", padx=5)

        self.page_label = tk.Label(self.pagination_frame, text="Página 1 de 1")
        self.page_label.pack(side="left", padx=5)

        self.next_button = tk.Button(self.pagination_frame, text="Próximo >>", command=self.next_page, state="disabled")
        self.next_button.pack(side="left", padx=5)

        # Label para mostrar o total de registros carregados
        self.total_label = tk.Label(self.pagination_frame, text="Total de registros: 0")
        self.total_label.pack(side="left", padx=5)

    def convert_to_mysql_date(self, date_str):
        """
        Converte uma data no formato dd/mm/yyyy para o formato YYYY-MM-DD usado no MySQL
        """
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return None  # Retorna None se a data estiver em formato inválido

    def load_data(self):
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Captura o valor do filtro
        self.filter_value_text = self.filter_value.get().strip()
        self.filter_type_text = self.filter_type.get()

        # Mapeamento entre o valor legível do ComboBox e o nome da coluna no banco de dados
        filter_mapping = {
            "Nro RDO": "r.nro_rdo",
            "Data RDO": "r.data",
            "Nro Contrato": "rc.nro_contrato"
        }

        # Se o filtro for do tipo Data RDO, convertemos a data para o formato MySQL
        if self.filter_type_text == "Data RDO" and self.filter_value_text:
            self.filter_value_text = self.convert_to_mysql_date(self.filter_value_text)
            if not self.filter_value_text:
                messagebox.showerror("Erro", "Data inválida. Use o formato dd/mm/yyyy.")
                return

        connection = None
        try:
            connection = self.db_connection.connect()
            if connection is None:
                logger.info("Falha ao estabelecer conexão com o banco de dados.")
                messagebox.showerror("Erro", "Falha ao estabelecer conexão com o banco de dados.")
                return

            cursor = connection.cursor(dictionary=True)

            # Calculando o offset para paginação
            offset = (self.current_page - 1) * self.records_per_page

            # Consulta para buscar os dados com paginação e filtro
            if self.filter_value_text:
                query = f"""
                    SELECT r.nro_rdo, 
                           DATE_FORMAT(r.data, '%d/%m/%Y') AS data_rdo, 
                           rc.nro_contrato, 
                           DATE_FORMAT(rc.inicio_contrato, '%d/%m/%Y') AS inicio_contrato, 
                           DATE_FORMAT(rc.termino_contrato, '%d/%m/%Y') AS termino_contrato
                    FROM rdo r
                    JOIN rdo_contrato rc ON r.id = rc.id_rdo
                    WHERE {filter_mapping[self.filter_type_text]} = %s
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (self.filter_value_text, self.records_per_page, offset))
            else:
                query = f"""
                    SELECT r.nro_rdo, 
                           DATE_FORMAT(r.data, '%d/%m/%Y') AS data_rdo, 
                           rc.nro_contrato, 
                           DATE_FORMAT(rc.inicio_contrato, '%d/%m/%Y') AS inicio_contrato, 
                           DATE_FORMAT(rc.termino_contrato, '%d/%m/%Y') AS termino_contrato
                    FROM rdo r
                    JOIN rdo_contrato rc ON r.id = rc.id_rdo
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (self.records_per_page, offset))

            rows = cursor.fetchall()

            for row in rows:
                # Insere os dados já com as datas formatadas
                self.tree.insert("", "end", values=(
                    row["nro_rdo"],
                    row["data_rdo"],  # Data já formatada
                    row["nro_contrato"],
                    row["inicio_contrato"],  # Início contrato já formatado
                    row["termino_contrato"]   # Término contrato já formatado
                ))

            # Atualizar a navegação de página e o total de registros
            self.update_pagination()

        except mysql.connector.Error as e:
            logger.error(f"Erro ao carregar os dados: {e}")
            messagebox.showerror("Erro", "Erro ao carregar os dados.")
        finally:
            if connection:
                connection.close()

    def update_pagination(self):
        """
        Atualiza a navegação de página e calcula o número total de páginas.
        """
        connection = None
        try:
            connection = self.db_connection.connect()
            if connection is None:
                return

            cursor = connection.cursor(dictionary=True)

            # Consulta para contar o número total de registros, considerando o filtro
            filter_mapping = {
                "Nro RDO": "r.nro_rdo",
                "Data RDO": "r.data",
                "Nro Contrato": "rc.nro_contrato"
            }

            if self.filter_value_text:
                query = f"""
                    SELECT COUNT(*) AS total_records
                    FROM rdo r
                    JOIN rdo_contrato rc ON r.id = rc.id_rdo
                    WHERE {filter_mapping[self.filter_type_text]} = %s
                """
                cursor.execute(query, (self.filter_value_text,))
            else:
                query = """
                    SELECT COUNT(*) AS total_records
                    FROM rdo r
                    JOIN rdo_contrato rc ON r.id = rc.id_rdo
                """
                cursor.execute(query)

            total = cursor.fetchone()
            self.total_records = total["total_records"]
            self.total_pages = (self.total_records // self.records_per_page) + (1 if self.total_records % self.records_per_page > 0 else 0)

            # Atualizar o rótulo de paginação
            self.page_label.config(text=f"Página {self.current_page} de {self.total_pages}")
            self.total_label.config(text=f"Total de registros: {self.total_records}")

            # Habilitar/Desabilitar botões de navegação
            if self.current_page == 1:
                self.prev_button.config(state="disabled")
            else:
                self.prev_button.config(state="normal")

            if self.current_page == self.total_pages or self.total_pages == 0:
                self.next_button.config(state="disabled")
            else:
                self.next_button.config(state="normal")

        except mysql.connector.Error as e:
            logger.error(f"Erro ao contar registros: {e}")
        finally:
            if connection:
                connection.close()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_data()

# Função que chama a exibição da tela de dados
def show_data_display(frame, db_connection):
    """Exibe a tela de listagem de dados"""
    data_display = DataDisplay(frame, db_connection)
    data_display.load_data()
    data_display.panel.pack(fill="both", expand=True)
