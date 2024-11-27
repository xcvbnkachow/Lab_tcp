import socket
import time
from datetime import datetime



# we want like to sync server and client, so we can use special codes, which can be sent between server and client
# it helps to solve multiple opening file problem
# _code1a means that file is opened by client
# _code2a is about closed file
# _code3a indicates client that server process with file is over

def start_client(host='127.0.0.1', port=65430):
    print("Starting client...")
    try:
        # Создаем сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))  # Подключение к серверу
            print(f"Connected to server: {host}:{port}")

            for i in range(50):  # 5 iterations
                try:
                    # 1 point: open file and say it to server
                    message = "_code1g"
                    client_socket.sendall(message.encode('utf-8'))
                    file = open("communication.txt", "r")
                    data = file.readline()
                    file.close()

                    file = open("communication.txt", "w")
                    time_ = datetime.now()
                    file.write(str(time_))
                    file.close()
                    print("Sent:", time_)
                    if data != "":
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

    except ConnectionRefusedError as e:
        print(f"(!) Cant connect to server")
    except Exception as e:
        print(f"(!) Client error: {e}")
    except FileNotFoundError as e:
        print(f"(!) Cant open communication file")


if __name__ == "__main__":
    start_client()