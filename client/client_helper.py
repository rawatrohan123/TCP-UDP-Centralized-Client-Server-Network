import socket
import threading

from udp_socket import UDPSocket
from cdma import CDMA
import ast
from threading import Thread


class ClientHelper:

    channel_ids = {}

    def __init__(self, client):
        self.client = client
        self.username = input("Enter a username: ")
        self.udp_socket = UDPSocket()
        self.print_lock = threading.Lock()  # creates the print lock


    def send_request(self, request):
        """
        Sends a request to the server.
        """
        self.client.send(request)

    def get_cdma_data(self):
        """
        Processes the cdma data which are the freq and codes to decode the messages.
        """
        data = ""
        packet = ""
        while True:
            packet = self.client.receive()
            if packet == "finished":
                break
            if type(packet) != dict:
                data += packet      # Getting chunks of data and appending it together
            elif type(packet) == dict:
                break
        message = ast.literal_eval(data)
        cdma = CDMA()
        freq = message[0]
        for i in range(len(message[1])):
            bits = cdma.decode(freq, message[1][i])         # decoding messages
            text = cdma.text_from_bits(bits)
            print(text)
        self.send_request(1)
        self.process_response()

    def process_response(self):
        """
        Processes responses from the server. Server will send a dictionary containing
        headers such as "udp" or "cdma". The client_helper here will then know how to properly
        process this response.
        """
        disconnect = False
        while True:
            data = self.client.receive()
            if data:
                if type(data) == str:
                    #continue
                    print(data)
                elif "disconnect" in data.keys():
                    print(data["message"])
                    #self.udp_socket.udp_socket.close()
                    disconnect = True
                    break
                    self.client.client.shutdown(socket.SHUT_RDWR)
                    #self.client.client.close()
                elif "print" in data.keys():
                    print(data["message"])
                elif "pgpadmin" in data.keys():
                    ClientHelper.channel_ids[data["message"]] = True  #channel is active
                    self.run_input_message()
                elif "map" in data.keys():
                    print(data["message"])
                elif "cdma" in data.keys():
                    print(data["message"])
                    break
                elif "udp" in data.keys():
                    try:
                        ipaddress = input(data["message"])
                        self.client.send(ipaddress)
                        port = input(data["message2"])
                        self.client.send(port)
                        port = int(port)
                        address = (ipaddress, port)
                        message = input(data["message3"])
                        message = message + " (message from " + self.username + ")"
                        self.udp_socket.send(message, address)
                    except Exception as error:
                        print(error)
                        print("Failed to send message. Please try again")
                elif data["input"] == 1:
                    user_input = input(data["message"])
                    self.client.send(user_input)
                else:
                    print(data["message"])
        if disconnect is True:
            self.client.client.shutdown(socket.SHUT_RDWR)
            return
        self.get_cdma_data()

    def input_message(self):
        while True:
            data = input("")
            self.client.send(data)
            if "#exit" in data:
                break

    def run_input_message(self):
        Thread(target=self.input_message, args=()).start()

    def log(self, message):
        """
        TODO: log a message on the server windows.
              note that before calling the print statement you must acquire a print lock
              the print lock must be released after the print statement.
        """
        self.print_lock.acquire()
        print(message)
        self.print_lock.release()

    def start(self):
        """
        Starts the client helper.
        """
        self.send_request(self.username)
        self.process_response()




