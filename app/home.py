import tkinter as tk

def show_home(frame):
    """Exibe o conteúdo da tela inicial"""

    # Título principal
    label = tk.Label(frame, text="Bem-vindo ao RDO Petrobras", font=("Arial", 24))
    label.pack(pady=50)

    # Descrição principal
    description_label = tk.Label(frame, text="Utilize o menu acima para navegar pelas opções.", font=("Arial", 14))
    description_label.pack(pady=10)

    # Frame para o rodapé
    footer_frame = tk.Frame(frame, bg="#d3d3d3", height=30)  # Fundo cinza claro para o rodapé
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X)  # Posiciona o rodapé na parte inferior

    # Label para a versão
    version_label = tk.Label(footer_frame, text="Versão 1.1.5", font=("Arial", 10), bg="#d3d3d3")
    version_label.pack(side=tk.BOTTOM, pady=5)  # Ajusta o padding para centralizar a label no rodapé
