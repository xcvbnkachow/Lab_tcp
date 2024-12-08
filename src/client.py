import socket
import time
import os

# Parameters
port_start = 65410
port_end = 65440

def start_client(host='127.0.0.1'):
    print("Starting client...")

    for port in range(port_start, port_end):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))
            print(f"Connected to server: {host}:{port}")
            id = client_socket.recv(1024)
            communication_file = "../" + str(id.decode()) + ".txt"

            for i in range(100):  # 500 iterations
                try:
                    # 1 point: open file and inform server
                    message = "_code1g"
                    client_socket.sendall(message.encode('utf-8'))

                    with open(communication_file, "r") as file:
                        data = file.readline()
                    request = ""
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
