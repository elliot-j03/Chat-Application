import tkinter as tk
import ttkbootstrap as tb

HEADER = 64
FORMAT = "utf-8"


def ou_update(frame, user_frame, ou_dict):
    ou_list = ou_dict["online_users"]
    ou_label = frame.nametowidget("ou_label")
    ou_label.config(text=f"Online users - {len(ou_list)}")
    u_current = {}
    u_keep = []
    for widget in user_frame.winfo_children():
        u_current.update({widget.cget("text"): widget})

    for user in u_current:
        if user in ou_list:
            u_keep.append(user)
        elif user not in ou_list:
            u_current[user].destroy()

    for row, user in enumerate(u_keep):
            u_current[user].grid(row=u_keep.index(user))

    row: int = len(u_keep)
    for user in ou_list:
        if user not in u_keep:
            label = tb.Label(user_frame, text=user)
            label.grid(column=0, row=row)
            row += 1


    for widget in user_frame.winfo_children():
        print(widget)


class ChatGUI(tk.Frame):

    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        # Top row
        top_row = tb.Frame(self)
        top_row.grid(row=0, column=1)

        self.user_page_button = tb.Button(top_row, text="USER", command=lambda: self.parent_controller.show_frame("user"))
        self.user_page_button.pack()

        # Left column
        left_frame = tb.Frame(self)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        chat_text_frame = tb.Frame(left_frame)
        chat_text_frame.pack(fill="both", expand=True)

        self.chat_text = tk.Text(chat_text_frame, width=110)
        self.chat_text.grid(row=0, column=0, sticky="nsew")
        self.chat_text.config(state=tk.DISABLED)

        scrollbar = tb.Scrollbar(chat_text_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_text.config(yscrollcommand=scrollbar.set)

        self.msg_entry_input = tk.StringVar()
        self.msg_entry = tb.Entry(left_frame, width=100, textvariable=self.msg_entry_input)
        self.msg_entry.pack(pady=20)
        self.msg_entry.bind("<Return>", self.message_send)

        self.send_button = tb.Button(left_frame, text="Send", style="success", width=20, command=self.message_send)
        self.send_button.pack(pady=20, padx=20)

        self.logout_button = tb.Button(left_frame, text="Log out", style="danger", width=20,
                                       command=self.logout)
        self.logout_button.pack()

        # Right column
        self.right_frame = tb.Frame(self)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.user_logged_in = tb.Label(self.right_frame, text=self.parent_controller.user_name)
        self.user_logged_in.pack(pady=20)

        self.online_users_label = tb.Label(self.right_frame, text="Online users - 0", name="ou_label")
        self.online_users_label.pack()

        self.online_users_column = tb.Frame(self.right_frame)
        self.online_users_column.pack()

    # FUNCTIONS ---------------------------------------------------------------------------
    def refresh_user_name(self):
        self.user_logged_in.config(text=f"Logged in as {self.parent_controller.user_name}")

    def logout(self):
        tag = "<o>".encode(FORMAT)
        self.parent_controller.client_socket.send(tag)

        self.parent_controller.show_frame("login")

    def update_text(self, text):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.INSERT, text+"\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)

    def message_send(self, event=None):
        client = self.parent_controller.client_socket

        tag = "<c>".encode(FORMAT)
        client.send(tag)

        chat_msg = self.msg_entry.get()

        message = chat_msg.encode(FORMAT)
        msg_length: int = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))

        client.send(send_length)
        client.send(message)

        self.msg_entry.delete(0, tk.END)
