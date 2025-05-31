import tkinter as tk
import ttkbootstrap as tb


class UserPageGUI(tk.Frame):

    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller

        self.user_name = ""

        self.user_name_label = tb.Label(self, text=self.user_name)
        self.user_name_label.pack(pady=20)

    def refresh_user_name(self):
        self.user_name_label.config(text=self.parent_controller.user_name)