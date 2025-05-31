import tkinter as tk
from gui.base_window import BaseWindow


if __name__ == "__main__":
    root = tk.Tk()
    app = BaseWindow(root)
    root.mainloop()
    app.client_socket.close()
