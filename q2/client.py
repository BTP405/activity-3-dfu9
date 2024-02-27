import socket
import pickle
import marshal

def count_num(*numbers):
    even_count = 0
    odd_count = 0
    for num in numbers:
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    return {'even': even_count, 'odd': odd_count}

arguments = ([1, 2, 3, 4, 5, 6])

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5001))
    print('Connected to the server!')

    try:
        # pickle the task along with its arguments
        serialized_msg = marshal.dumps((count_num.__code__, arguments))
        # send the length of the message
        client_socket.send(len(serialized_msg).to_bytes(4, byteorder='big'))
        # send the pickled message
        client_socket.send(serialized_msg)
        # read the length of the result
        result_length = int.from_bytes(client_socket.recv(4), byteorder='big')
        # read the pickled result
        raw_result = client_socket.recv(result_length)
        # unpickle the result
        result = pickle.loads(raw_result)
        print(f'Result: ', result)
    except Exception as e:
        print(f"Error processing task: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    client()
