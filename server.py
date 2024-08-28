#!/usr/bin/python3

import socket
import threading

from colorama import Back, Fore, Style


def client_thread(client_socket, clients, usernames):
    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username
    print(Fore.BLUE + f"[!] Usuario {username} conectado al chat.")

    for client in clients:
        if client is not client_socket:
            client.sendall(
                f"[+] El usuario {username} se ha conectado al chat.\n".encode()
            )

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            for client in clients:
                if client is not client_socket:
                    client.sendall(message.encode())
        except:
            break


def init_server():

    HOST = "localhost"
    PORT = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(Fore.CYAN + f"\n[+] Servidor a la espera de conexiones...\n")

    clients = []
    usernames = {}

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        print(Fore.GREEN + f"[!] Nuevo cliente conectado: {address}\n")

        thread = threading.Thread(
            target=client_thread, args=(client_socket, clients, usernames)
        )

        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    init_server()
