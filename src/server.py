import os
import threading
import socket
import time
import random
from datetime import datetime

# const parameters:
MAX_CLIENTS = 2
PORT_START = 65430
PORT_END = 65440
THREADS = list()
USERS_ID = list()
HOST = "127.0.0.1"

state_file = "client_state.txt"
with open(state_file, "w") as f:
    f.write(f"{PORT_START}")

count_of_clients_file = "count_of_clients.txt"
with open(count_of_clients_file, "w") as f:
    f.write("0")

stop_event = threading.Event()

def start_server(given_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, given_port))
    server.listen(1)
    try:
        print("Server listening on port", given_port)

        client_socket, addr = server.accept()

        client_id = str(random.randint(1, 1000))
        while client_id in USERS_ID:
            client_id = str(random.randint(1, 1000))
        USERS_ID.append(client_id)

        print(f"Accepted connection from ('{HOST}', {given_port}), id is {client_id}")

        # creating a special file
        communication_file = f"../{client_id}.txt"
        with open(communication_file, "w"):
            pass # just create the file

        client_socket.send(client_id.encode("utf-8"))

        # starting communication...
        while True:
            # receiving a message from client...
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message == "_code1g":
                pass # do nothing :)

            elif message == "_code2g":
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

        with open(count_of_clients_file, "r") as f:
            curr_count = int(f.read())

        with open(count_of_clients_file, "w") as f:
            f.write(f"{curr_count - 1}")

        os.remove(communication_file)
        client_socket.close()
    except OSError as e:
        print(f"Error on port {given_port}: {e}")


if __name__ == "__main__":
    for port in range(PORT_START, PORT_END):
        thread = threading.Thread(target=start_server, args=(port,))
        thread.start()
        time.sleep(1.2)
        THREADS.append(thread)

    i = -1
    for thread in THREADS[:]:
        thread.join()
        i += 1
        print(f"---> Thread on port '6543{i}' to client({USERS_ID[i]}) finished <--- ")
