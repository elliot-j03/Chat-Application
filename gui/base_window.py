import json
import tkinter as tk
import ttkbootstrap as tb
from PIL import Image, ImageTk

from gui.start_up import StartUpGUI
from gui.login import LoginGUI
from gui.create_user import CreateUserGUI
from gui.server_chat import ChatGUI, ou_update
from gui.user_page import UserPageGUI

HEADER = 64
HOST = "localhost"
PORT = 9999
FORMAT = "utf-8"
INCOMING_MSG = ""


class BaseWindow:
    def __init__(self, app_root):
        self.root = app_root
        self.style = tb.Style(theme="darkly")
        self.root.title("EJ-cord")
        self.root.geometry("1080x720")
        self.root.iconphoto(False, ImageTk.PhotoImage(Image.open("mupasaur_icon_headphones.png")))

        self.client_socket = None

        self.main_frame = tb.Frame(self.root)
        self.main_frame.pack()

        self.start_up_gui = StartUpGUI(self.main_frame, self)

        self.login_gui = LoginGUI(self.main_frame, self)
        self.login_status = None
        self.user_name = ""

        self.create_user_gui = CreateUserGUI(self.main_frame, self)

        self.chat_gui = ChatGUI(self.main_frame, self)

        self.user_edit_page = UserPageGUI(self.main_frame, self)

        self.frames = {
            "startup": self.start_up_gui,
            "login": self.login_gui,
            "create": self.create_user_gui,
            "chat": self.chat_gui,
            "user": self.user_edit_page
        }
        self.show_frame("startup")

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        if name == "user":
            self.user_edit_page.refresh_user_name()
        self.frames[name].pack(expand=False, fill="y")

    def server_recv(self):
        client = self.client_socket
        while True:
            try:
                activity_tag_encoded = client.recv(3)
                activity_tag = activity_tag_encoded.decode(FORMAT)
                print(activity_tag)
                if not activity_tag:
                    self.frames["chat"].logout()
                    break
                if activity_tag == "<l>":
                    success: str = client.recv(HEADER).decode(FORMAT)
                    if success == "True":
                        self.show_frame("chat")
                        self.user_name = self.login_gui.user_entry.get()
                        self.login_gui.user_entry.delete(0, tk.END)
                        self.login_gui.pass_entry.delete(0, tk.END)
                        self.login_gui.failed_label.config(text="")
                        self.chat_gui.refresh_user_name()
                    else:
                        self.login_gui.failed_label.config(text="The username and password do not match")
                elif activity_tag == "<c>":
                    msg_length = client.recv(HEADER).decode(FORMAT)
                    msg = client.recv(int(msg_length)).decode(FORMAT)
                    user = client.recv(HEADER).decode(FORMAT)
                    self.chat_gui.update_text(user, msg)
                elif activity_tag == "<n>":
                    found = client.recv(HEADER).decode(FORMAT)
                    if found == "True":
                        self.create_user_gui.user_taken = True
                        self.create_user_gui.after(0, self.create_user_gui.create_user_final)
                    else:
                        self.create_user_gui.user_taken = False
                        self.create_user_gui.after(0, self.create_user_gui.create_user_final)
                elif activity_tag == "<u>":
                    ou_json = client.recv(HEADER).decode(FORMAT)
                    online_users = json.loads(ou_json)
                    ou_update(self.chat_gui.right_frame, self.chat_gui.online_users_column, online_users)
                elif activity_tag == "<i>":
                    chat_json_len = int(client.recv(HEADER).decode(FORMAT))

                    chat_data = b""
                    while len(chat_data) < chat_json_len:
                        chat_packet = client.recv(chat_json_len - len(chat_data))
                        chat_data += chat_packet
                    chat_json = chat_data.decode(FORMAT)

                    chat: list = json.loads(chat_json)
                    self.chat_gui.load_prev_chat(chat)
                elif activity_tag == "<f>":
                    self.client_socket.close()
                    self.show_frame("startup")
                    break
            except Exception as e:
                print(f"An error has occurred: {e}")
                self.client_socket.close()
                self.show_frame("startup")
                break
