import socket
import pickle

def send_file(file_path, server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(server_address)

        # Read the file and create a file object
        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_object = {'filename': file.name, 'data': file_data}

        # Pickle the file object
        pickled_file = pickle.dumps(file_object)

        # Send the pickled file object to the server
        client_socket.sendall(pickled_file)
        print(f"File '{file.name}' sent successfully")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

def run_client(file_path, server_address):
    send_file(file_path, server_address)

if __name__ == "__main__":
    file_path = "sendfile.txt"  
    server_address = ('localhost', 12345)
    
    run_client(file_path, server_address)
