import tkinter as tk
from tkinter import ttk, messagebox
import logging
import mysql.connector

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

        # Tabela
        self.tree = ttk.Treeview(self.panel, columns=("Nro RDO", "Data RDO", "Nro Contrato", "Início Contrato", "Término Contrato"), show="headings")
        self.tree.pack(fill='both', expand=True)

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)

    def load_data(self):
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        connection = None
        try:
            connection = self.connect()
            if connection is None:
                logger.info("Falha ao estabelecer conexão com o banco de dados.")
                messagebox.showerror("Erro", "Falha ao estabelecer conexão com o banco de dados.")
                return

            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT r.nro_rdo, r.data, rc.nro_contrato, rc.inicio_contrato, rc.termino_contrato
                FROM rdo r
                JOIN rdo_contrato rc ON r.id = rc.id_rdo
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=(
                    row["nro_rdo"],
                    row["data"],
                    row["nro_contrato"],
                    row["inicio_contrato"],
                    row["termino_contrato"]
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
