import socket
import threading
import tkinter as tk
import ttkbootstrap as tb

HOST = "localhost"
PORT = 9999


class StartUpGUI(tk.Frame):
    def __init__(self, parent, parent_controller):
        super().__init__(parent)
        self.parent_controller = parent_controller

        self.label = tb.Label(self, text="Connecting...")
        self.label.pack()

        self.try_connection = tb.Button(self, text="Retry", command=self.start_auto_connect)
        self.try_connection.pack()

        self.start_auto_connect()

    def start_auto_connect(self):
        threading.Thread(target=self.connect, daemon=True).start()

    def connect(self):
        self.label.config(text="Connecting...")
        self.try_connection.forget()
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            self.parent_controller.client_socket = client

            self.label.config(text=" ")
            if client is not None and client.fileno() != -1:
                self.parent_controller.show_frame("login")

                listening_thread = threading.Thread(target=self.parent_controller.server_recv)
                listening_thread.daemon = True
                listening_thread.start()
            else:
                self.parent_controller.client_socket.close()
        except (ConnectionRefusedError,
                ConnectionResetError,
                ConnectionAbortedError,
                TimeoutError,
                socket.timeout,
                socket.gaierror,
                socket.herror) as error:
            self.label.config(text=f"Connection failed: {error}")
        self.try_connection.pack()
