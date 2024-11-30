import socket
from datetime import datetime
from xmlrpc.client import DateTime

# parameters:
communication_file = "../communication.txt"
port_start = 65430
port_end = 65440

def handle_client(client_socket):
    try:
        while True:
                # receiving a message from client...
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                match message:
                    case "_code1g":
                        # do nothing :)
                        # this section is informative, we can just delete it
                        pass

                    case "_code2g":
                        try:
                            with open(communication_file, "r") as file:
                                data = file.readline()

                            answer = "pong"
                            with open(communication_file, "w") as file:
                                file.write(answer)

                            print(datetime.now().time(), "-> Get from client:", data)
                            print(datetime.now().time(), "-> Sent to client:", answer)
                            
                            message = "_code3g"
                            client_socket.send(message.encode('utf-8'))

                        except Exception as e:
                            print("(!) Error while handling file:", e)
                            break

    except ConnectionResetError:
        print("(!) Client disconnected")
    except Exception as e:
        print("(!) Something went wrong:", e)
    finally:
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(port_start, port_end):
        try:
            server.bind(('localhost', port))
            server.listen(1)
            print("Server listening on port", port)

            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            handle_client(client_socket)
            break

        except OSError as e:
            match e:
                case OSError():
                    print(f"(!) Port {port} is already in use. Trying next port...")
                case _:
                    print(f"(!) An unexpected error occurred: {e}")





if __name__ == "__main__":
    start_server()
