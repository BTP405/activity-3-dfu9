import socket
import pickle
import os

def receive_file(server_socket, save_directory):
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    try:
        # receive pickled file 
        pickled_file = client_socket.recv(4096)
        file_object = pickle.loads(pickled_file)

        # extract data
        filename, data = file_object['filename'], file_object['data']

        # complete path to save file
        save_path = os.path.join(save_directory, filename)

        # save file on device
        with open(save_path, 'wb') as file:
            file.write(data)

        print(f"File '{filename}' received and saved to {save_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

def run_server(save_directory):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Server is listening for incoming connections...")

    while True:
        receive_file(server_socket, save_directory)

if __name__ == "__main__":
    save_directory = "Activity 3\save q1 files"  
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    run_server(save_directory)
