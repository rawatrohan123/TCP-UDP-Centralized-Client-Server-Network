import socket
import threading
from threading import Thread
import pickle


class UDPSocket:
    """
    Implementation of the UDP socket
    """

    def __init__(self):
        self.port = None
        self.ipv4 = socket.AF_INET
        self.ip = None
        self.transmission_protocol = socket.SOCK_DGRAM
        self.udp_socket = socket.socket(self.ipv4, self.transmission_protocol)
        self.print_lock = threading.Lock()  # creates the print lock
        self.listen()
        self.run()

    def listen(self):
        try:
            self.bind()
            print(f'UDP socket successfully bind to port {self.port} and ip {self.ip}')
        except ConnectionError as err:
            print("An error occurred: ", err.args[1])

    def bind(self):
        result = 0
        while result == 0:
            try:
                self.ip = input("Enter the ip address to bind your UDP client: ")
                self.port = input("Enter the port to bind your UDP client: ")
                self.port = int(self.port)
                address = (self.ip, self.port)
                self.udp_socket.bind(address)
                result = 1
            except Exception as error:
                print(error)

    def send(self, message, to=None, broadcast=False, toItself=False):
        """
        Sends message using UDP.
        """
        if broadcast:
            self.broadcast(message, toItself)
        else:
            serialized = pickle.dumps(message)
            self.udp_socket.sendto(serialized, to)

    def broadcast(self, message, toItself=False):
        """
        Broadcasts message using UDP.
        """
        socket_option = socket.SOL_SOCKET
        transmission_method = socket.SO_BROADCAST
        active = 1
        self.udp_socket.setsockopt(socket_option, transmission_method, active)
        address = ('<broadcast>', self.port)
        self.udp_socket.sendto(message, address)
        if toItself:
            self.print_response(is_broadcast=True)

    def log(self, message):
        """
        Prints a message using print lock thread.
        """
        self.print_lock.acquire()
        message = "\n" + message
        print(message)
        self.print_lock.release()

    def print_response(self, is_broadcast=False, mem_alloc=4096):
        """
        Print any messages received.
        """
        while True:
            try:
                data, addr = self.udp_socket.recvfrom(mem_alloc)
                if is_broadcast:
                    self.log(f'Message broadcast: {data}  from {addr}')
                else:
                    deserialized = pickle.loads(data)
                    self.log(f'{deserialized} from {addr}')
            except ConnectionError as e:
                print("\n" + str(e))
                print("Message not sent. Please try again")

    def run(self):
        """
        Run UDP socket
        """
        Thread(target=self.handler, args=()).start()

    def handler(self):
        self.print_response()


