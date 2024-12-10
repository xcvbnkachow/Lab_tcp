import socket
import time

"""
we want like to sync server and client, so we can use special codes, which can be sent between server and client
it helps to solve multiple opening file problem
_code1a means that file is opened by client
_code2a is about closed file
_code3a indicates client that server process with file is over
"""

# const parameters:
ITER_COUNT = 50
MAX_CLIENTS = 2
PORT_START = 65430
PORT_END = 65440
state_file = "client_state.txt"
count_of_clients_file = "count_of_clients.txt"

def start_client(HOST="127.0.0.1"):
    with open(state_file, "r") as f:
        curr_port = int(f.read())

    with open(count_of_clients_file, "r") as f:
        curr_count = int(f.read())

    print("Starting client...")

    curr_count += 1

    if curr_count > MAX_CLIENTS:
        with open(state_file, "w") as f:
            f.write(f"{curr_port}")

        curr_count = MAX_CLIENTS
        with open(count_of_clients_file, "w") as f:
            f.write(f"{curr_count}")

        print(f"(!) A number of clients has exceeded the limit! Connection has not been installed...")
        exit(0)

    else:
        with open(state_file, "w") as f:
            f.write(f"{curr_port + 1}")

        with open(count_of_clients_file, "w") as f:
            f.write(f"{curr_count}")


    for port in range(curr_port, PORT_END):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, port))
            print(f"Connected to server: {HOST}:{port}")
            id = client_socket.recv(1024)
            communication_file = f"../{id.decode()}.txt"

            for i in range(ITER_COUNT):
                try:
                    # 1 point: open file and inform server
                    message = "_code1g"
                    client_socket.sendall(message.encode('utf-8'))

                    with open(communication_file, "r") as file:
                        data = file.readline()

                    with open(communication_file, "w") as file:
                        request = "ping"
                        file.write(request)

                    if i > 0:
                        print("Sent:", request)
                    if data:
                        print("Received:", data)

                    # 2 point: now we can tell server that file is closed
                    message = "_code2g"
                    client_socket.sendall(message.encode('utf-8'))

                    # 3 point: then we need to wait for a message from the server that its work with the file is done
                    response = client_socket.recv(1024).decode('utf-8')
                    if response == "_code3g":
                        time.sleep(1)
                        continue
                    else:
                        print("Error")
                        exit(0)

                except Exception as e:
                    print(f"(!) Data communication error: {e}")
                    break
            break
        except ConnectionRefusedError:
            print(f"(!) Connection refused on port {port}. Server may not be running.")
        except OSError as e:
            print(f"(!) An unexpected OS error occurred: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_client()
