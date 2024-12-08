import os
import socket
from datetime import datetime
import threading
import time
import random

# parameters:
MAX_CLIENTS = 3
PORT_START = 65410
PORT_END = 65440
THREADS = []
USERS_ID = []
HOST = "127.0.0.1"

def start_server(given_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, given_port))
        server.listen(1)
        print("Server listening on port", given_port)

        client_socket, addr = server.accept()
        client_id = 1
        while True:
            client_id = str(random.randint(1, 1000))
            if client_id not in USERS_ID:
                USERS_ID.append(client_id)
                break
        print(f"Accepted connection from {addr}, id is {client_id}")

        # creating a special file
        communication_file = "../" + client_id + ".txt"
        with open(communication_file, "w") as file:
            pass  # just create the file

        client_socket.send(client_id.encode("utf-8"))

        # starting communication...
        while True:
            # receiving a message from client...
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            match message:
                case "_code1g":
                    pass  # do nothing :)

                case "_code2g":
                    with open(communication_file, "r") as file:
                        data = file.readline()
                        answer = "pong"
                        with open(communication_file, "w") as file:
                            file.write(answer)

                        print(datetime.now().time(), f"-> Get from client({client_id}):", data)
                        print(datetime.now().time(), f"-> Sent to client({client_id}):", answer)

                        # tell client that file is already closed
                        message = "_code3g"
                        client_socket.send(message.encode('utf-8'))

        os.remove(communication_file)
        client_socket.close()
    except OSError as e:
        print(f"Error on port {given_port}: Port is already in use")

if __name__ == "__main__":
    for port in range(PORT_START, PORT_END):
        if len(THREADS) >= MAX_CLIENTS:
            break

        thread = threading.Thread(target=start_server, args=(port,))
        thread.start()
        time.sleep(5)
        if thread.is_alive():
            THREADS.append(thread)



    for thread in THREADS:
        thread.join()
