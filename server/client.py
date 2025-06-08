import socket

def main():
    host = '127.0.0.2'  # Server address
    port = 3690         # Server port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print("Connected to server.")

        # Puedes enviar un mensaje inicial si lo deseas
        message = "Hello, Server!"
        client_socket.sendall(message.encode())

        # Mantente escuchando mensajes del servidor
        while True:
            response = client_socket.recv(1024)
            if not response:
                print("Server closed the connection.")
                break
            print("Received from server:", response.decode())

    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()