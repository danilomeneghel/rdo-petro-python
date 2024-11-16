import tkinter as tk
import app.frame  # Importa o módulo com as configurações da janela principal

class MenuBar:
    def __init__(self, root):
        self.root = root
        self.frame = app.frame.Frame(self.root)  # Cria uma instância da classe Frame, que configura a janela

        self.menu = tk.Menu(self.root)  # Inicializa a barra de menu
        self.create_menus()

    def create_menus(self):
        """Cria os menus da barra superior sem submenus"""
        # Home
        self.menu.add_command(label="Home", command=self.show_home)

        # Importar Planilha
        self.menu.add_command(label="Importar Planilha", command=self.import_file)

        # Listar Dados
        self.menu.add_command(label="Listar Dados", command=self.list_data)

        # Sair
        self.menu.add_command(label="Sair", command=self.exit_program)

        self.root.config(menu=self.menu)

    def show_home(self):
        """Carrega a tela Home e limpa qualquer outra tela anterior"""
        self.clear_frame()  # Limpa o conteúdo atual da tela
        self.frame.show_home()  # Chama a função show_home para exibir a tela inicial novamente

    def import_file(self):
        """Carrega a tela de Importação de arquivos e limpa qualquer outra tela anterior"""
        self.clear_frame()
        import app.excel_picker
        app.excel_picker.show_excel_picker(self.frame.main_frame)

    def list_data(self):
        """Carrega a tela de Listagem de dados e limpa qualquer outra tela anterior"""
        self.clear_frame()
        import app.data_display
        app.data_display.show_data_display(self.frame.main_frame)

    def exit_program(self):
        """Fecha o programa"""
        self.root.quit()

    def clear_frame(self):
        """Limpa completamente a área de conteúdo (remove qualquer widget antigo)"""
        for widget in self.frame.main_frame.winfo_children():
            widget.destroy()  # Remove todos os widgets antigos
