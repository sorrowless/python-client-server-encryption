from json2xml import json2xml, readfromjson  # noqa
from textwrap import wrap

import base64
import os
import socket


def get_file(directory):
    '''Gets list of files from given directory and send it back

    :param directory: directory to search in. Only this directory without any
        subdirectories will be searched
    :type directory: str

    :returns: path to each file with directory included
    :rtype: str
    '''
    if not os.path.isdir(directory):
        raise IOError(f"{directory} doesn't look as a directory")
    for f in os.listdir(directory):
        yield os.path.join(directory, f)


def convert_file(filepath):
    '''Converts given filename from json to xml

    :param filepath: path to file to convert. It supposed to exist
    :type filepath: str

    :returns: converted xml or None if any input was not valid
    :rtype: str or None
    '''
    print(f"Processing {filepath}")
    xml_data = None
    try:
        json_data = readfromjson(filepath)
        xml_data = json2xml.Json2xml(json_data).to_xml()
    except SystemExit:
        print(f"Unable to convert {filepath}. Check if it is valid json")
    return xml_data


def cipher_data(data):
    '''Cipher given data

    Method to cipher data. In current case does nothing but base64 encoding -
    nothing more was asked ;)

    :param data: data to cipher
    :type data: str

    :returns: enciphered data
    :rtype: bytes
    '''
    print(f"Got some data to cipher:\n{data}")
    if not isinstance(data, str):
        data = str(data).encode('utf-8')
    return base64.b64encode(data)


def send_data(data, filepath, cipher_method):
    '''Send data over network

    :param data: data to send
    :type data: str
    :param filepath: path to file to send. Used as metadata only
    :type filepath: str
    :param cipher_method: function with which data will be ciphered
    :type cipher_method: callable object (function supposed)

    :returns: None
    '''
    print(f"Got some data to send:\n{data}")
    print(f"Sending encoded {filepath} to server")
    filename = os.path.basename(filepath)
    data = {
            "filename": os.path.splitext(filename)[0],
            "data": data
    }
    s = socket.socket()
    host = os.getenv('RECEIVER_HOSTNAME', socket.gethostname())
    # Port is hardcoded due to not add more complexity with additional configs
    port = 5555
    s.settimeout(10)
    s.connect((host, port))
    s.settimeout(None)
    s.send(cipher_method(data))
    print(f"Sent encoded {filepath} to server")
    s.shutdown(socket.SHUT_RDWR)
    s.close()


if __name__ == '__main__':
    directory_to_search = os.getenv('JSON_DIR', '/tmp/json_data')
    for filepath in get_file(directory_to_search):
        converted_file = convert_file(filepath)
        # There can be different cases, for example if file is not in json
        if not converted_file:
            print(f"Skip {filepath}, was not converted")
            continue
        send_data(converted_file, filepath, cipher_data)
