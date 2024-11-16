import tkinter as tk

class Frame:
    def __init__(self, root):
        self.root = root
        self.root.title("RDO Petrobras")  # Título da janela principal
        self.root.geometry("800x600")  # Define o tamanho da janela principal
        self.root.resizable(False, False)  # Impede que a janela seja redimensionada

        # Frame que vai abrigar o conteúdo das telas
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Inicia a tela Home por padrão
        self.show_home()

    def show_home(self):
        """Exibe a tela inicial"""
        import app.home  # Importa o módulo que contém o conteúdo textual da tela inicial
        app.home.show_home(self.main_frame)  # Passa o main_frame para o módulo home
