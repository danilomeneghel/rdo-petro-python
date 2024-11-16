import tkinter as tk
from app.menu_bar import MenuBar

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuBar(root)
    root.mainloop()
