import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

from colorama import Fore


def send_message(event, client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f"{username} > {message}\n".encode())

    text_widget.insert(END, f"{username} > {message}\n")
    entry_widget.delete(0, END)


def recieve_message(client_socket, text_widget):
    while True:
        try:
            messages = client_socket.recv(1024).decode()
            if not messages:
                break
            text_widget.insert(END, messages)
            pass
        except:
            break


def client_program():
    HOST = "localhost"
    PORT = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    username = input(Fore.GREEN + f"\n[!] Ingrese tu nombre de usuario: ")
    client_socket.sendall(username.encode())

    windows = Tk()
    windows.title("Chat")

    text_widget = ScrolledText(windows)
    text_widget.pack(pady=10, padx=10)

    entry_widget = Entry(windows)
    entry_widget.bind(
        "<Return>",
        lambda event: send_message(
            event, client_socket, username, text_widget, entry_widget
        ),
    )
    entry_widget.pack(pady=5, padx=5, fill=BOTH)

    thread = threading.Thread(target=recieve_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    windows.mainloop()
    client_socket.close()


if __name__ == "__main__":
    client_program()
