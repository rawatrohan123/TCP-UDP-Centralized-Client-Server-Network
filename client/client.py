########################################################################################################################
# Class: Computer Networks
# Date: 09/17/2021
# Lab3: TCP Client Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Rohan Rawat
# Student ID: 917018484
# Student Github Username: rawatrohan123
# Instructions: Read each problem carefully, and implement them correctly.
########################################################################################################################

# don't modify this imports.
import socket
import pickle
from client_helper import ClientHelper
from client_input import get_port, get_server_ip

######################################## Client Socket ###############################################################3
"""
Client class that provides functionality to create a client socket is provided. Implement all the methods but bind(..)
"""


class Client(object):

    def __init__(self):
        """
        Class constructor
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = 0
        self.server_ip = None
        self.server_port = 0

    def connect(self, server_ip_address, server_port):
        """
        TODO: Create a connection from client to server
              Note that this method must handle any exceptions
        :server_ip_address: the know ip address of the server
        :server_port: the port of the server
        """
        self.server_ip = server_ip_address
        self.server_port = server_port
        try:
            self.client.connect((server_ip_address, server_port))
            print("Successfully connected to server: " + str(server_ip_address) + "/" + str(server_port))
            self.client_helper()
        except ConnectionError as conerror:
            print("Error" + conerror.args[1])

    def bind(self, client_ip='', client_port=12000):
        """
        DO NOT IMPLEMENT, ALREADY IMPLEMENTED
        This method is optional and only needed when the order or range of the ports bind is important
        if not called, the system will automatically bind this client to a random port.
        :client_ip: the client ip to bind, if left to '' then the client will bind to the local ip address of the machine
        :client_port: the client port to bind.
        """
        self.client.bind((client_ip, client_port))

    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data: the raw data to serialize (note that data can be in any format.... string, int, object....)
        :return: VOID
        """
        serialized_data = pickle.dumps(data)
        self.client.send(serialized_data)

    def receive(self, max_alloc_buffer=4090):
        """
        TODO: Deserializes the data received by the server
        :param max_alloc_buffer: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        data = self.client.recv(max_alloc_buffer)
        deserialized_data = pickle.loads(data)
        return deserialized_data

    def client_helper(self):
        """
         TODO: create an object of the client helper and start it.
        """
        client_helper = ClientHelper(self)
        client_helper.start()

    def close(self):
        """
        TODO: close this client
        :return: VOID
        """
        print("Client disconnected")
        self.client.close()


# main code to run client
if __name__ == '__main__':
    result = None
    while result is None:
        try:
            server_ip = get_server_ip()
            server_port = get_port()
            client = Client()
            client.connect(server_ip, server_port)
            result = True
        except Exception as msg:
            print(msg)
            print("\nPlease try again. \n")
      # creates a connection with the server
