import tkinter as tk
import ttkbootstrap as tb
from PIL import Image, ImageTk

FORMAT = "utf-8"
HEADER = 64


class UserPageGUI(tk.Frame):

    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller

        self.user_name = ""
        self.change_name_page = None

        self.user_name_label = tb.Label(self, text=self.user_name)
        self.user_name_label.pack(pady=20)

        self.change_name_button = tb.Button(self, text="Change username", command=self.change_name_attempt)
        self.change_name_button.pack(pady=10)

        self.go_back_button = tb.Button(self, text="Go Back", command=lambda: self.parent_controller.show_frame("chat"))
        self.go_back_button.pack(pady=10)

    def refresh_user_name(self):
        self.user_name_label.config(text=self.parent_controller.user_name)

    def change_name_attempt(self):
        self.change_name_page = ChangeNamePage(self.parent_controller)


def convert_to_bytes(string) -> tuple:
    string_encoded = string.encode(FORMAT)
    string_length = str(len(string)).encode(FORMAT)
    string_length += b" " * (HEADER - len(string_length))

    return string_encoded, string_length


class ChangeNamePage(tk.Frame):

    def __init__(self, parent_controller):
        self.parent_controller = parent_controller

        self.change_name_window = tk.Toplevel(self.parent_controller.root)
        self.change_name_window.geometry("400x200")
        self.change_name_window.title("")
        self.change_name_window.iconphoto(False, ImageTk.PhotoImage(Image.open("mupasaur_icon_headphones.png")))
        
        super().__init__(self.change_name_window)
        self.pack(in_=self.change_name_window)

        self.error_label = tb.Label(self, text=" ", foreground="#eb4b3d")
        self.error_label.pack(pady=5)

        self.new_name_entry_input = tk.StringVar()
        self.new_name_entry = tb.Entry(self, width=30, textvariable=self.new_name_entry_input)
        self.new_name_entry.pack(pady=10)

        self.confirm_button = tb.Button(self, text="Confirm", command=self.request_name_change)
        self.confirm_button.pack(pady=10)
    
    def request_name_change(self):
        client = self.parent_controller.client_socket
        current_user_name = self.parent_controller.user_name
        new_user_name = self.new_name_entry.get()

        self.error_label.config(text=" ", foreground="#eb4b3d")
        if new_user_name:
            tag = "<r>".encode(FORMAT)
            client.send(tag)

            current_user_name_encoded, current_user_length = convert_to_bytes(current_user_name)
            new_user_name_encoded, new_user_length = convert_to_bytes(new_user_name)

            client.send(current_user_length)
            client.send(current_user_name_encoded)
            client.send(new_user_length)
            client.send(new_user_name_encoded)
        else:
            self.error_label.config(text="Please enter a valid username", foreground="#eb4b3d")

