import tkinter as tk
import ttkbootstrap as tb

HEADER = 64
FORMAT = "utf-8"
bold_font = ("Helvetica", 11, "bold")
font = ("Helvetica", 11)

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


class ChatGUI(tk.Frame):

    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        # Top row
        top_row = tb.Frame(self)
        top_row.grid(row=0, column=1, sticky="ew")

        self.user_page_button = tb.Button(top_row, text="USER", command=lambda: self.parent_controller.show_frame("user"))
        self.user_page_button.pack(pady=10, side="right")

        # Left column
        left_frame = tk.Frame(self)
        left_frame.grid(row=1, column=0, sticky="n")

        left_title = tb.Label(left_frame, text="Chats")
        left_title.pack(pady=20)

        # Main column
        main_frame = tk.Frame(self)
        main_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.chat_text = tk.Text(main_frame, width=110, font=font)
        self.chat_text.grid(row=0, column=0)
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.tag_configure("bold", font=bold_font)

        entry_frame = tk.Frame(main_frame)
        entry_frame.grid(row=1, column=0)
        
        self.msg_entry_input = tk.StringVar()
        self.msg_entry = tb.Entry(entry_frame, width=100, textvariable=self.msg_entry_input)
        self.msg_entry.grid(row=0, column=0, pady=5)
        self.msg_entry.bind("<Return>", self.message_send)

        self.previous_chat_user = ""

        self.send_button = tb.Button(entry_frame, text=">", style="success", width=2, command=self.message_send)
        self.send_button.grid(row=0, column=1, pady=5)

        self.logout_button = tb.Button(entry_frame, text="L/O", style="danger", width=4,
                                       command=self.logout)
        self.logout_button.grid(row=1, sticky="w")

        # Right column
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=1, column=2, sticky="n", padx=10, pady=10)

        self.user_logged_in = tb.Label(self.right_frame, text=self.parent_controller.user_name)
        self.user_logged_in.pack(pady=20)

        self.online_users_label = tb.Label(self.right_frame, text="Online users - 0", name="ou_label")
        self.online_users_label.pack()

        self.online_users_column = tk.Frame(self.right_frame)
        self.online_users_column.pack()

    # FUNCTIONS ---------------------------------------------------------------------------
    def refresh_user_name(self):
        self.user_logged_in.config(text=f"Logged in as {self.parent_controller.user_name}")

    def logout(self):
        tag = "<o>".encode(FORMAT)
        self.parent_controller.client_socket.send(tag)
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete("1.0", "end")
        self.chat_text.config(state=tk.DISABLED)

        self.parent_controller.show_frame("login")

    def update_text(self, user, msg):
        self.chat_text.config(state=tk.NORMAL)
        if self.previous_chat_user != user:
            self.chat_text.insert("end", user+"\n", "bold")
            self.previous_chat_user = user
        self.chat_text.insert("end", msg+"\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)

    def message_send(self, event=None):
        client = self.parent_controller.client_socket

        chat_msg = self.msg_entry.get()
        if chat_msg != "":
            tag = "<c>".encode(FORMAT)
            client.send(tag)

            message = chat_msg.encode(FORMAT)
            msg_length: int = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))

            client.send(send_length)
            client.send(message)

            self.msg_entry.delete(0, tk.END)
    
    def load_prev_chat(self, chat):
        self.chat_text.config(state=tk.NORMAL)
        for c in chat:
            if c[0] == "!":
                un = c.replace("!", "")
                self.chat_text.insert("end", un+"\n", "bold")
            else:
                self.chat_text.insert("end", c+"\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
