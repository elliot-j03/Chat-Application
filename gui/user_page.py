import tkinter as tk
import ttkbootstrap as tb


class UserPageGUI(tk.Frame):

    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller
