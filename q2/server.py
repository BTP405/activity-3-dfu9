import socket
import pickle
import types
import marshal

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()
    print('Listening for connections...')

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f'Client {client_addr} has connected!')

        try:
            msg_length = int.from_bytes(client_socket.recv(4), byteorder='big')
            print(msg_length)
            raw_msg = client_socket.recv(msg_length)
            bytecode, args = marshal.loads(raw_msg)
            print('Bytecode: ', bytecode)
            print('Arguments: ', args)
            func = types.FunctionType(bytecode, globals(), 'count_even_odd')
            result = func(*args)
            serialized_result = pickle.dumps(result)
            client_socket.send(len(serialized_result).to_bytes(4, byteorder='big'))
            client_socket.send(serialized_result)
        except Exception as e:
            print(f"Error processing task: {e}")
        finally:
            client_socket.close()

if __name__ == '__main__':
    server()
