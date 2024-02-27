import socket
import threading
import pickle

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                # Receive pickled message from client
                data = client_socket.recv(4096)
                if not data:
                    break

                message = pickle.loads(data)

                # Broadcast the message to all connected clients
                with self.lock:
                    for c in self.clients:
                        c.send(pickle.dumps(message))
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            # Remove the client from the list and close the connection
            with self.lock:
                self.clients.remove(client_socket)
            client_socket.close()

    def run(self):
        print(f"Server is listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()

                # Add the client to the list
                with self.lock:
                    self.clients.append(client_socket)

                # Handle the client in a separate thread
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

if __name__ == '__main__':
    server = ChatServer('localhost', 5555)
    server.run()
