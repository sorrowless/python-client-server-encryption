import ast
import base64
import socket


def save_to_file(data, filepath):
    '''Save data to file

    :param data: data to save
    :type data: str
    :param filepath: path to file in which data should be saved
    :type filepath: str

    :returns: None
    '''
    print(f"Start saving data into {filepath}")
    with open(filepath, 'wt') as fh:
        fh.write(data)
    print("Saved to data to file")


def decipher_data(data):
    '''Decipher given data

    Just decipher given data. Remember to ask something more complex than just
    base64 encoding next time, lol.

    :param data: data to decipher
    :type data: str

    :returns: deciphered data
    :rtype: str
    '''

    print("Start deciphering")
    # We gonna get bytes-like object
    data = b''.join(data)
    deciphered_data = base64.b64decode(data).decode('utf-8')
    return deciphered_data


def receive(host, port, decipher_method):
    '''Listen and receive data on given socket

    :param host: host to listen on
    :type host: str
    :param port: port to listen on
    :type port: int
    :param decipher_method: method to decipher received data
    :type decipher_method: callable object (function supposed)

    :returns: deciphered data
    :rtype: str
    '''
    s = socket.socket()
    s.bind((host, port))
    s.listen()
    while True:
        c, addr = s.accept()
        with c:
            print(f"Got connection from {addr}")
            print("Start receiving")
            data = list()
            # Hardcode chunk size to avoid complexity
            chunk = c.recv(1024)
            while chunk:
                data.append(chunk)
                chunk = c.recv(1024)
            print("Received, closing connection")
        yield decipher_method(data)


if __name__ == "__main__":
    # Hardcode socket to avoid complexity also
    host = '0.0.0.0'
    port = 5555
    print("Start listening for data")
    for data in receive(host, port, decipher_data):
        print(f"Got deciphered data: {data}")
        try:
            data = ast.literal_eval(data)
        except SyntaxError:
            print(f"Got wrong or incomplete data to decode: {data}")
            continue
        filename = data['filename'] + ".xml"
        save_to_file(data['data'], f"/tmp/xml_data/{filename}")
