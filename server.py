import socket
import random
#server

def handle_client(client_socket):
    while True:
        # Получаем сообщение от клиента
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        match message:
            case "_code1g":
                # do nothing :)
                # this section is informative, we can just delete it
                None

            case "_code2g":
                file = open("communication.txt", "r")
                data = file.readline()
                file.close()

                file = open("communication.txt", "w")
                answer = random.randint(5, 100) * "+"
                file.write(answer)
                file.close()
                print("Get from client:", data)
                print("Sent to client:", answer)

                message = "_code3g"
                client_socket.send(message.encode('utf-8'))

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 65430
    server.bind(('localhost', port))
    server.listen(1)
    print("Server listening on port", port)


    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    handle_client(client_socket)


if __name__ == "__main__":
    start_server()
