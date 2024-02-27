import socket
import threading
import pickle

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def receive_messages(self):
        try:
            while True:
                # Receive pickled message from server
                data = self.client_socket.recv(4096)
                if not data:
                    break

                message = pickle.loads(data)
                print(f"Received message: {message}")
        except Exception as e:
            print(f"Error receiving messages: {e}")
        finally:
            self.client_socket.close()

    def send_message(self, message):
        # Pickle and send the message to the server
        self.client_socket.send(pickle.dumps(message))

    def run(self):
        # Start a thread to receive messages in the background
        threading.Thread(target=self.receive_messages).start()

        try:
            while True:
                # Get input from the user and send it to the server
                message = input("Enter your message: ")
                self.send_message(message)
        except KeyboardInterrupt:
            print("Client shutting down.")
        finally:
            self.client_socket.close()

if __name__ == '__main__':
    client = ChatClient('localhost', 5555)
    client.run()
