import tkinter as tk
from tkinter import filedialog, messagebox
from app.excel_password_remover import ExcelPasswordRemover
from app.excel_importer import ExcelImporter
from app.data_persister import DataPersister

class ExcelPicker:
    def __init__(self, root):
        self.panel = tk.Frame(root, bg="#d3d3d3")  # Definindo a cor de fundo como cinza claro (#d3d3d3)
        self.panel.pack(fill="both", expand=True)

        self.title_label = tk.Label(self.panel, text="Importar Planilha Excel", font=("Arial", 20, "bold"), bg="#d3d3d3")
        self.title_label.pack(pady=20)

        # Frame para agrupar o campo de texto e o botão 'Selecione' horizontalmente
        file_select_frame = tk.Frame(self.panel, bg="#d3d3d3")
        file_select_frame.pack(pady=20)

        self.file_path_field = tk.Entry(file_select_frame, width=50)
        self.file_path_field.config(state="readonly")
        self.file_path_field.pack(side="left", padx=5)  # Alinha à esquerda

        self.select_button = tk.Button(file_select_frame, text="Selecione", command=self.select_file, bg="#4CAF50", fg="white")
        self.select_button.pack(side="left", padx=5)  # Alinha à direita do campo

        self.import_button = tk.Button(self.panel, text="Importar", command=self.import_data, bg="#008CBA", fg="white")
        self.import_button.pack(pady=20)

    def select_file(self):
        # Usando a sintaxe simples para o filtro de arquivos Excel, que é bem compatível
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo Excel",
            filetypes=[("Arquivos Excel", "*.xls"), ("Arquivos Excel", "*.xlsx"), ("Arquivos Excel", "*.xlsm")]  # Filtros mais explícitos
        )
        if file_path:
            self.file_path_field.config(state="normal")
            self.file_path_field.delete(0, tk.END)
            self.file_path_field.insert(0, file_path)
            self.file_path_field.config(state="readonly")

    def import_data(self):
        file_path = self.file_path_field.get()
        if not file_path:
            return

        converted_file_path = ExcelPasswordRemover.convert_file(file_path)
        if converted_file_path:
            excel_importer = ExcelImporter()
            rdo_data = excel_importer.get_rdo_data(converted_file_path)
            rdo_contract_data = excel_importer.get_rdo_contract_data(converted_file_path)

            if rdo_data and rdo_contract_data:
                data_persister = DataPersister()
                data_persister.persist_data(rdo_data, rdo_contract_data)
            else:
                messagebox.showerror("Erro", "Falha ao processar os dados do arquivo.")
        else:
            messagebox.showerror("Erro", "Falha ao converter o arquivo Excel.")

    def get_panel(self):
        return self.panel

def show_excel_picker(frame):
    """Exibe a tela de importação de planilha"""
    excel_picker = ExcelPicker(frame)
    excel_picker.get_panel().pack(fill="both", expand=True)
