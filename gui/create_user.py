import tkinter as tk
import ttkbootstrap as tb

FORMAT = "utf-8"
HEADER = 64


def check_pass(pass_one, pass_two) -> bool:
    if pass_one != pass_two:
        return False
    return True


class CreateUserGUI(tk.Frame):

    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller

        self.failed_label = tb.Label(self, text=" ", foreground="#eb4b3d")
        self.failed_label.pack(pady=10)

        self.user_entry_input = tk.StringVar()
        self.user_entry = tb.Entry(self, width=30, textvariable=self.user_entry_input)
        self.user_entry.pack(pady=20)

        self.user_taken = None
        self.user_name_pending = None
        self.pass_one_pending = None
        self.pass_two_pending = None

        self.failed_label_pass = tb.Label(self, text=" ", foreground="#eb4b3d")
        self.failed_label_pass.pack(pady=10)

        self.passw_entry_input_one = tk.StringVar()
        self.passw_entry_one = tb.Entry(self, width=30, textvariable=self.passw_entry_input_one)
        self.passw_entry_one.pack(pady=20)

        self.passw_entry_input_two = tk.StringVar()
        self.passw_entry_two = tb.Entry(self, width=30, textvariable=self.passw_entry_input_two)
        self.passw_entry_two.pack(pady=20)

        self.go_back_button = tb.Button(self, text="Create Account",
                                        command=self.create_user)
        self.go_back_button.pack(pady=20)

        self.go_back_button = tb.Button(self, text="Go back",
                                        command=self.go_back)
        self.go_back_button.pack(pady=20)

    def check_user(self, user_name):
        client = self.parent_controller.client_socket

        tag = "<n>".encode(FORMAT)
        client.send(tag)

        user_name_encoded = user_name.encode(FORMAT)
        user_length = str(len(user_name)).encode(FORMAT)
        user_length += b" " * (HEADER - len(user_length))

        client.send(user_length)
        client.send(user_name_encoded)

    def add_user(self, user_name, passw):
        client = self.parent_controller.client_socket

        tag = "<a>".encode(FORMAT)
        client.send(tag)

        user_enc = user_name.encode(FORMAT)
        user_length: int = len(user_enc)
        send_length = str(user_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))

        pass_enc = passw.encode(FORMAT)
        pass_length: int = len(pass_enc)
        pass_send_length = str(pass_length).encode(FORMAT)
        pass_send_length += b" " * (HEADER - len(pass_send_length))

        client.send(send_length)
        client.send(user_enc)

        client.send(pass_send_length)
        client.send(pass_enc)

    def create_user(self):
        self.failed_label.config(text="")
        self.failed_label_pass.config(text="")

        self.user_taken = None
        self.user_name_pending = self.user_entry_input.get()
        self.pass_one_pending = self.passw_entry_input_one.get()
        self.pass_two_pending = self.passw_entry_input_two.get()

        self.check_user(self.user_name_pending)

    def create_user_final(self):
        user_name = self.user_name_pending
        pass_one = self.pass_one_pending
        pass_two = self.pass_two_pending
        taken = self.user_taken
        p_match = check_pass(pass_one, pass_two)

        if p_match and not taken:
            self.add_user(user_name, pass_one)
            self.user_entry.delete(0, tk.END)
            self.passw_entry_one.delete(0, tk.END)
            self.passw_entry_two.delete(0, tk.END)
            self.parent_controller.show_frame("login")
        elif not p_match and not taken:
            self.failed_label_pass.config(text="Passwords do not match")
        elif p_match and taken:
            self.failed_label.config(text="This username is already taken")
        else:
            self.failed_label_pass.config(text="Passwords do not match")
            self.failed_label.config(text="This username is already taken")

    def go_back(self):
        self.parent_controller.show_frame("login")
        self.user_entry.delete(0, tk.END)
        self.passw_entry_one.delete(0, tk.END)
        self.passw_entry_two.delete(0, tk.END)
        self.failed_label_pass.config(text="")
        self.failed_label.config(text="")
