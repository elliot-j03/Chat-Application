import socket
import threading
import time
import json
import tkinter as tk
import ttkbootstrap as tb
from PIL import Image, ImageTk

HEADER = 64
HOST = "localhost"
PORT = 9999
FORMAT = "utf-8"

clients: list = []
clients_info: list = []
clients_lock = threading.Lock()


# Checks if the user has entered the correct details upon login
def user_check(user_passw) -> bool:
    with open("user_data.txt", "r") as file:
        lines: list = []
        for line in file.readlines():
            line = line.strip()
            user, passw = line.split("||")
            lines.append(user+"||"+passw)
        if user_passw in lines:
            return True


# Handles login request
def login_handle(client):
    client.send(b"<l>")

    user_passw: str = client.recv(HEADER).decode(FORMAT)
    user_correct: bool = user_check(user_passw)
    user_name = user_passw.split("||")[0]

    if user_correct:
        success = "True".encode(FORMAT)
        client.send(success)
        return user_name, True
    else:
        success = "False".encode(FORMAT)
        client.send(success)
        return user_name, False
    

def replace_chat_log_names(old_name, new_name):
    
    lines: list = []
    indexes: list = []
    old = "!" + old_name
    new = "!" + new_name

    print(f"old name: {old} and new: {new}")
    with open("server_chat.txt", "r") as file:
        lines = file.readlines()
    
    if lines:
        for i, line in enumerate(lines):
            if old == line.rstrip():
                indexes.append(i)

        with open("server_chat.txt", "w") as file:
            for i, line in enumerate(lines):
                for index in indexes:
                    if index == i:
                        file.writelines(new+"\n")
                    else:
                        file.writelines(line)


# Tries to find the username passed in user_data.txt
def user_name_find(user_name) -> bool:
    with open("user_data.txt", "r") as file:
        for line in file.readlines():
            user_info = line.split("||")
            if user_info[0] == user_name:
                return True
        return False


# Handles the create account request
def new_user_check(client):
    user_name_length_encoded = client.recv(HEADER)
    user_name_length = user_name_length_encoded.decode(FORMAT)
    if user_name_length:
        user_name_length = int(user_name_length)
        user_name_encoded = client.recv(user_name_length)
        user_name = user_name_encoded.decode(FORMAT)

        tag = "<n>".encode(FORMAT)
        client.send(tag)
        if user_name_find(user_name):
            found = "True".encode(FORMAT)
        else:
            found = "False".encode(FORMAT)
        client.send(found)


# Updates text for clients
def update_text_client(msg, user_name):
    msg_encoded = msg.encode(FORMAT)
    user = user_name.encode(FORMAT)

    msg_length: int = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    for client in clients:
        with clients_lock:
            client.sendall("<c>".encode(FORMAT))
            client.sendall(send_length)
            client.sendall(msg_encoded)
            client.sendall(user)


# Updates online user list
def update_online_users(c_info):
    online_users = []
    for c in c_info:
        online_users.append(c.user_name)
    app.online_users = online_users
    ou_json = json.dumps({"online_users": online_users})
    tag = "<u>".encode(FORMAT)
    for client in clients:
        with clients_lock:
            client.sendall(tag)
            client.sendall(ou_json.encode(FORMAT))


# Loads the previous chat for the client
def load_prev_chat(client):
    chat: list = []
    with open("server_chat.txt", "r") as file:
        for line in file.readlines():
            chat.append(line.strip())
    tag = "<i>".encode(FORMAT)
    chat_json = json.dumps(chat)
    client.send(tag)

    json_len = len(chat_json)
    send_len = str(json_len).encode(FORMAT)
    send_len += b" " * (HEADER - len(send_len))
    
    client.send(send_len)
    client.send(chat_json.encode(FORMAT))


# Adds a user to user_data.txt
def add_user(client):
    user_length = int(client.recv(HEADER).decode(FORMAT))
    user_name = client.recv(user_length).decode(FORMAT)

    pass_length = int(client.recv(HEADER).decode(FORMAT))
    passw = client.recv(pass_length).decode(FORMAT)

    with open("user_data.txt", "a") as file:
        file.write("\n"+user_name+"||"+passw)


# Client class that stores details of the current user
class ClientDetails:

    def __init__(self):
        self.user_name = "undefined_user"
        self.user_id = "undefined_id"


# Server GUI class
class ServerGUI:

    def __init__(self, app_root):
        self.root = app_root
        self.style = tb.Style(theme="darkly")
        self.root.title("EJ-cord Server Manager")
        self.root.geometry("1080x720")
        self.root.iconphoto(False, ImageTk.PhotoImage(Image.open("mupasaur_icon_headphones.png")))

        self.server_socket = None
        self.running = False
        self.online_users = None
        self.previous_chat_user = ""

        button_frame = tb.Frame(self.root)
        button_frame.pack()

        self.start_server = tb.Button(button_frame, text="Start Server", style="secondary", width=20,
                                      command=lambda: threading.Thread(target=self.server_start, daemon=True).start())
        self.start_server.grid(column=0, row=0, pady=5, padx=5)

        self.stop_server = tb.Button(button_frame, text="Stop Server", style="danger", width=20,
                                     command=self.server_stop)
        self.stop_server.grid(column=1, row=0, pady=5, padx=5)

        self.main_frame = tb.Frame(self.root, padding=20)
        self.main_frame.pack(expand=True, fill="both")

        self.chat_text = tk.Text(self.main_frame, width=110)
        self.chat_text.pack(pady=20)
        self.chat_text.config(state=tk.DISABLED)

        self.msg_entry_input = tk.StringVar()
        self.msg_entry = tb.Entry(self.main_frame, width=100, textvariable=self.msg_entry_input)
        self.msg_entry.pack(pady=20)

    # Updates server chat
    def update_text_local(self, text):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, text+"\n")
        self.chat_text.config(state=tk.DISABLED)
    
    # Updates server_chat.txt
    def update_chat_log(self, msg, user_name):
        with open("server_chat.txt", "a") as file:
            if self.previous_chat_user != user_name:
                file.writelines("!"+user_name+"\n")
                self.previous_chat_user = user_name
            file.writelines(msg+"\n")

    # Handles messages to server and client
    def msg_handle(self, client, user_name):
        msg_length_encoded = client.recv(HEADER)
        msg_length = msg_length_encoded.decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg_encoded = (client.recv(msg_length))
            msg = msg_encoded.decode(FORMAT)

            # Chat log
            self.update_chat_log(msg, user_name)

            # Server text
            text = f"{user_name}: {msg}"
            self.update_text_local(text)

            # Client text
            update_text_client(msg, user_name)
    
    # Replaces old user name with new one upon change name request
    def update_user_name(self, old_name, new_name):
        # change in user_data.txt
        lines: list = []
        with open("user_data.txt", "r") as file:
            lines: list = file.readlines()
            for i, line in enumerate(lines):
                user_name, passw = line.split("||")
                if user_name == old_name:
                    lines[i] = new_name+"||"+passw
        with open("user_data.txt", "w") as file:
            for line in lines:
                file.writelines(line)
        # update client details
        for i, c in enumerate(clients_info):
            if c.user_name == old_name:
                clients_info[i].user_name = new_name
        # update users logged in list
        update_online_users(clients_info)
        # log on server
        msg = f"{old_name} has changed their name to {new_name}"
        self.update_text_local(msg)
        # updates chat_log
        replace_chat_log_names(old_name, new_name)


    # Handles change username
    def change_user_name(self, client):
        current_user_length_encoded = client.recv(HEADER)
        current_user_length = current_user_length_encoded.decode(FORMAT)
        current_user_length = int(current_user_length)
        current_user_encoded = client.recv(current_user_length)
        current_user_name = current_user_encoded.decode(FORMAT)

        user_name_length_encoded = client.recv(HEADER)
        user_name_length = user_name_length_encoded.decode(FORMAT)
        user_name_length = int(user_name_length)
        user_name_encoded = client.recv(user_name_length)
        user_name = user_name_encoded.decode(FORMAT)
    
        tag = "<r>".encode(FORMAT)
        client.send(tag)
        if user_name_find(user_name):
            found = "True".encode(FORMAT)
            client.send(found)
        else:
            found = "False".encode(FORMAT)
            client.send(found)
            client.send(user_name_encoded)
            self.update_user_name(current_user_name, user_name)

    # The client requests
    ### BUG: Tags occasionally become incorrect, make sure all tag function occur independently
    ### TODO: Update other clients of name change
    def client_requests(self, tag, client, cds):
        # self, tag, client socket, client object
        if tag == "<l>":
            # Log In
            user_name, success = login_handle(client)
            cds.user_name = user_name
            if success:
                clients_info.append(cds)
                text = f"{cds.user_name} is online"

                load_prev_chat(client)
                update_online_users(clients_info)
                self.update_text_local(text)
            else:
                pass
        elif tag == "<c>":
            # Chat
            self.msg_handle(client, cds.user_name)
        elif tag == "<n>":
            # New User
            new_user_check(client)
        elif tag == "<a>":
            # Add New User
            add_user(client)
        elif tag == "<r>":
            self.change_user_name(client)
            # load_prev_chat(client)
        elif tag == "<o>":
            # Log Out
            text = f"{cds.user_name} is now offline"
            clients_info.remove(cds)
            update_online_users(clients_info)
            self.update_text_local(text)

    def client_handle(self, client, addr):
        client_details = ClientDetails()
        with clients_lock:
            clients.append(client)
        try:
            while True:
                client_request_tag = client.recv(3)
                if not client_request_tag:
                    break
                client_request_decoded = client_request_tag.decode(FORMAT)

                # Viewing the tags
                print(client_request_decoded)

                self.client_requests(client_request_decoded, client, client_details)
        except Exception as e:
            print(f"[SERVER] An error has occurred: {e}")
        finally:
            with clients_lock:
                clients.remove(client)
            client.close()
            if client_details in clients_info:
                clients_info.remove(client_details)
                update_online_users(clients_info)
                self.update_text_local(f"{client_details.user_name} is now offline")

    # Starting the server and threads
    def server_start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(0.1)
        self.server_socket = server
        self.running = True
        try:
            server.bind((HOST, PORT))
            print(f"Successfully connected to host {HOST}, port {PORT}")
            self.update_text_local("Server has started...")

            server.listen()
            while self.running:
                try:
                    client, addr = server.accept()
                except socket.timeout:
                    continue

                thread = threading.Thread(target=self.client_handle, args=(client, addr))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
        except ConnectionRefusedError:
            print(f"Unable to connect to host {HOST}, port {PORT}")

    # Shuts down clients and stops server
    def server_stop(self):
        self.running = False
        for client in clients:
            with clients_lock:
                client.sendall("<f>".encode(FORMAT))
                client.shutdown(socket.SHUT_RDWR)
                client.close()
        time.sleep(1)
        if self.server_socket:
            try:
                self.server_socket.close()
                print(f"Successfully shut down host {HOST}, port {PORT}")
            except Exception as e:
                print(f"Error while shutting down the server: {e}")
        self.update_text_local("Server has closed...")


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()
    app.server_socket.close()
