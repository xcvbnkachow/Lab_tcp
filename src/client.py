import socket
import time




# we want like to sync server and client, so we can use special codes, which can be sent between server and client
# it helps to solve multiple opening file problem
# _code1a means that file is opened by client
# _code2a is about closed file
# _code3a indicates client that server process with file is over

# parameters:
communication_file = "../communication.txt"
port_start = 65430
port_end = 65440

def start_client(host='127.0.0.1'):
    print("Starting client...")

    for port in range(port_start, port_end):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))  # Подключение к серверу
            print(f"Connected to server: {host}:{port}")

            for i in range(50):  # 50 iterations
                try:
                    # 1 point: open file and say it to server
                    message = "_code1g"
                    client_socket.sendall(message.encode('utf-8'))

                    with open(communication_file, "r") as file:
                        data = file.readline()

                    with open(communication_file, "w") as file:
                        request = "ping"
                        file.write(request)
                        print("Sent:", request)

                    if data:
                        print("Received:", data)

                    # 2 point: now we can tell server that file is closed
                    message = "_code2g"
                    client_socket.sendall(message.encode('utf-8'))

                    # 3 point: than we need to wait message from server that its work with file is done
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
        except OSError as e:
            match e:
                case OSError():
                    print(f"(!) Port {port} is already in use or server is on another. Trying next port...")
                case _:
                    print(f"(!) An unexpected error occurred: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    start_client()