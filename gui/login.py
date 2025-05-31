import tkinter as tk
import ttkbootstrap as tb

FORMAT = "utf-8"


class LoginGUI(tk.Frame):

    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller

        form_frame = tb.Frame(self, width=1000)
        form_frame.pack(expand=True, fill="both", anchor="center")

        self.user_entry_input = tk.StringVar()
        self.user_entry = tb.Entry(form_frame, width=30, textvariable=self.user_entry_input)
        self.user_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=(200, 20))

        self.user_label = tb.Label(form_frame, text="Username")
        self.user_label.grid(row=1, column=0, sticky=tk.W + tk.E, pady=(200, 20), padx=10)

        self.pass_entry_input = tk.StringVar()
        self.pass_entry = tb.Entry(form_frame, width=30, show="*", textvariable=self.pass_entry_input)
        self.pass_entry.grid(row=2, column=1, sticky=tk.W + tk.E, pady=10)

        self.passw_view = tb.Button(form_frame, text="View Password", command=self.view_password)
        self.passw_view.grid(row=2, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

        self.pass_label = tb.Label(form_frame, text="Password")
        self.pass_label.grid(row=2, column=0, sticky=tk.W + tk.E, pady=10, padx=10)

        self.login_button = tb.Button(form_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=1, pady=20)

        self.create_user_button = tb.Button(form_frame, text="Create Account",
                                            command=self.create_user)
        self.create_user_button.grid(row=4, column=1, pady=20)

        x_pos = self.user_entry.winfo_x()
        y_pos = self.user_entry.winfo_y()

        self.failed_label = tb.Label(self, text=" ", foreground="#eb4b3d")
        self.failed_label.place(x=x_pos+10, y=y_pos+150)

    def view_password(self):
        entry_show = self.pass_entry.cget("show")
        if entry_show == "*":
            self.pass_entry.config(show="")
            self.passw_view.config(text="Hide Password")
        else:
            self.pass_entry.config(show="*")
            self.passw_view.config(text="View Password")

    def login(self):
        client = self.parent_controller.client_socket

        tag = "<l>".encode(FORMAT)
        client.send(tag)

        user = self.user_entry.get()
        passw = self.pass_entry.get()
        user_passw = (user+"||"+passw).encode(FORMAT)
        client.send(user_passw)

    def create_user(self):
        self.parent_controller.show_frame("create")
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.failed_label.config(text="")
