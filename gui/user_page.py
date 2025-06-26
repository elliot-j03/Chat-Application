import tkinter as tk
import ttkbootstrap as tb


class UserPageGUI(tk.Frame):

    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller

        self.user_name = ""

        self.user_name_label = tb.Label(self, text=self.user_name)
        self.user_name_label.pack(pady=20)

        self.change_name_button = tb.Button(self, text="Change username")
        self.change_name_button.pack(pady=10)

        self.go_back_button = tb.Button(self, text="Go Back", command=lambda: self.parent_controller.show_frame("chat"))
        self.go_back_button.pack(pady=10)

    def refresh_user_name(self):
        self.user_name_label.config(text=self.parent_controller.user_name)