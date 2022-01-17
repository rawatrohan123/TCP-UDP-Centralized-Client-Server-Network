# don't modify this imports.
import socket
from threading import Thread
from client_handler import ClientHandler


class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10  # keeps 10 clients in queue

    def __init__(self, host="0.0.0.0", port=12000):
        """
        TODO: copy and paste your implementation from lab 3 for self.server socket property
        """
        self.host = host
        self.port = port
        self.handlers = {}  # initializes client_handlers list
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _bind(self):
        """
        TODO: copy and paste your implementation from lab 3
        :return: VOID
        """
        self.server.bind((self.host, self.port))

    def _listen(self):
        """
        TODO: copy and paste your implementation from lab 3
        :return: VOID
        """
        try:
            self.server.listen(self.MAX_NUM_CONN)
            print("Server is running without issues")
            print("Listening at " + str(self.host) + "/" + str(self.port))
        except Exception as msg:
            print(msg)

    def _accept_clients(self):
        """
        #TODO: Modify your implementation from lab 3, so now the
               server can support multiple clients pipelined.
               HINT: you must thread the handler(...) method
        :return: VOID
        """
        while True:
            clientsocket, addr = self.server.accept()
            Thread(target=self._handler, args=(clientsocket, addr)).start()  # client thread started

    def _handler(self, clienthandler, addr):
        """
        TODO: create an object of the ClientHandler.
              see the clienthandler.py file to see
              the parameters that must be passed into
              the ClientHandler's constructor to create
              the object.
              Once the ClientHandler object is created,
              add it to the dictionary of client handlers initialized
              on the Server constructor (self.handlers)
        :clienthandler: the clienthandler child process that the server creates when a client is accepted
        :addr: the addr list of server parameters created by the server when a client is accepted.
        """
        client_handler = ClientHandler(self, clienthandler, addr)
        self.handlers[addr[1]] = client_handler
        client_handler.run()

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._bind()
        self._listen()
        self._accept_clients()


# main execution
if __name__ == '__main__':
    server = Server()
    server.run()
