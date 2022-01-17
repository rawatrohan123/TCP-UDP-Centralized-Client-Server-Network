########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: Server support for multiple clients
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Rohan Rawat
# Student ID: 917018484
# Student Github Username: rawatrohan123
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Running instructions: This program needs the server to run. The server creates an object of this class.
#
########################################################################################################################

from threading import Thread
import threading
import pickle

import random
from bot import Bot
from menu import Menu
from message import Message
from datetime import datetime
from cdma import CDMA
from network_map import NetworkMap
from chat_room import ChatRoom
import sys
from distance_protocols import DistanceProtocols

class ClientHandler:
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """

    MAX_ALLOC_MEM = 4096
    chat_rooms = []


    def __init__(self, server_instance, clienthandler, addr):
        """
        Class constructor already implemented for you.
        :param server_instance: passed as 'self' when the object of this class is created in the server object
        :param clientsocket: the accepted client on server side. this handler, by itself, can send and receive data
                             from/to the client that is linked to.
        :param addr: addr[0] = server ip address, addr[1] = client id assigned buy the server
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.handler = clienthandler
        self.print_lock = threading.Lock()  # creates the print lock
        self.username = self.receive()
        self.messages = Message
        self.send_client_info()
        self.cdma = CDMA()
        self.bots = []

    def process_requests(self):
        """
        TODO: Create a loop that keeps waiting for client requests.
              Note that the process_request(...) method is executed inside the loop
              Recall that you must break the loop when the request received is empty.
        :return: VOID
        """
        data = self.handler.recv(self.MAX_ALLOC_MEM)
        deserialized = pickle.loads(data)
        self.process_request(deserialized)

    def process_request(self, request):
        """
        TODO: This implementation is similar to the one you did in the method process_request(...)
              that was implemented in the server of lab 3.
              Note that in this case, the clienthandler is not passed as a parameter in the function
              because you have a private instance of it in the constructor that can be invoked from this method.
        :request: the request received from the client. Note that this must be already deserialized
        :return: VOID
        """
        self.username = request
        request = request + " has connected\nClient ID: " + str(self.client_id)
        self.log(request)

    def send(self, data):
        """
        Serializes data with pickle, and then sends the serialized data.
        """
        serialized = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        self.handler.send(serialized)

    def receive(self, max_mem_alloc=4096):
        """
        TODO: receive the data, deserializes the data received
        :max_mem_alloc: an integer representing the maximum allocation (in bytes) in memory allowed
                        for the data that is about to be received. By default is set to 4096 bytes
        :return: the deserialized data
        """
        data = self.handler.recv(max_mem_alloc)
        deserialized_data = pickle.loads(data)
        return deserialized_data

    def send_client_info(self):
        """
        Sends the client info the the client
        """
        message = "Your client info is:\nClient Name: " + self.username + "\nClient ID: " + str(self.client_id)
        data = {"input": 0, "cache": 0, "message": message}
        serialized_data = pickle.dumps(data)
        self.handler.send(serialized_data)

    def log(self, message):
        """
        TODO: log a message on the server windows.
              note that before calling the print statement you must acquire a print lock
              the print lock must be released after the print statement.
        """
        self.print_lock.acquire()
        print(message)
        self.print_lock.release()

    def get_num_users(self):
        """
        Returns the number of users currently in the server.
        """
        usercount = 0
        for entries in self.server.handlers:
            usercount = usercount + 1
        return usercount

    def send_user_list(self):
        """
        Sends the list of users that are currently connected to the server
        to the client.
        """
        usercount = 0
        for entries in self.server.handlers:
            usercount = usercount + 1
        message = "Users Connected: " + str(usercount) + "\n"
        for key, value in self.server.handlers.items():
            usercount = usercount - 1
            message += str(value.username) + ":" + str(key)
            if usercount > 0:
                message += ", "
        data = {"input": 0, "cache": 0, "message": message}
        self.send(data)
        self.log("Sent user list to client " + self.username + "/" + str(self.client_id))

    def send_map(self):
        self.log(self.username + ": Mapping the network and sending")
        users = []
        for key, value in self.server.handlers.items():
            users.append(value.username)
        user_names = ["Rohan", "Jose", "John", "Amelia"]
        distance = DistanceProtocols.map_network([])
        message = "Routing table requested! Waiting for response...\n\n\n"
        num_index = 0
        for user in user_names:
            message += "\t\t\t\t\t" + user
        message += "\n"
        for i in range(0, len(distance)):
            for j in range(0, len(distance)):
                if j == 0:
                    message += user_names[num_index]
                    num_index = num_index + 1
                message += (str("\t\t\t\t\t" + str(distance[i][j])) + "\t")
            message += "\n"
        data = {"input": 0, "cache": 0, "message": message}
        self.send(data)

    def send_link_state(self):
        self.log("Sending link state routing table")
        user_names = ["Rohan", "Jose", "John", "Amelia"]
        distances = DistanceProtocols.map_network(user_names)
        message = "\nRouting table for Rohan (id: 50851) computed with Link State Protocol:\n\n"
        message += self.link_state()
        data = {"input": 0, "cache": 0, "message": message}
        self.send(data)
        self.send("")

    def send_distance_vector(self):
        self.log(self.username + ": Sending routing table with distance vector")
        users = []
        for key, value in self.server.handlers.items():
            users.append(value.username)
        user_names = ["Rohan", "Jose", "John", "Amelia"]
        distances = DistanceProtocols.map_network(user_names)
        distance = DistanceProtocols.distance_vector(distances)
        message = "Routing table computed with Distance Vector Protocol: \n\n\n"
        num_index = 0
        for user in user_names:
            message += "\t\t\t\t\t" + user
        message += "\n"
        for i in range(0, len(distance)):
            for j in range(0, len(distance)):
                if j == 0:
                    message += user_names[num_index]
                    num_index = num_index + 1
                message += (str("\t\t\t\t\t" + str(distance[i][j])) + "\t")
            message += "\n"
        data = {"input": 0, "cache": 0, "message": message}
        self.send(data)

    def get_proxy(self):
        message = "\nComing Soon!\n"
        data = {"input": 0, "cache": 0, "message": message}
        self.send(data)

    def disconnect_client(self):
        self.log("Disconnecting client " + str(self.client_id) + " from server!")
        message = "Disconnecting from server"
        data = {"disconnect": 1, "input": 0, "cache": 0, "message": message}
        self.send(data)

    def send_message(self):
        """
        Stores a message that the client was to send to a certain recipient id.
        """
        active_id = False
        message = "Enter your message: "
        data = {"input": 1, "cache": 0, "message": message}
        self.send(data)
        user_message = self.receive()
        message = "Enter recipient id: "
        data = {"input": 1, "cache": 0, "message": message}
        self.send(data)
        try:
            recipient_id = int(self.receive())
        except Exception as e:
            self.send({"input": 0, "cache": 0,
                       "message": "Error: Please enter an integer representing recipient id. Please try again"})
            return
        message = datetime.now().strftime('%Y-%m-%d %H:%M') + ": " + user_message + " (private message from " \
                  + self.username + ")"
        for key, value in self.server.handlers.items():
            if key == recipient_id:  # checks to see if recipient id matches one currently connected to server
                active_id = True
        if active_id:
            Message.add_message(message, recipient_id)
            message = "Message sent!"
            data = {"input": 0, "cache": 0, "message": message}
            self.send(data)
            self.log(self.username + "/" + str(self.client_id) + " sent a message!")
        else:
            message = "Invalid recipient id. Please try again"
            data = {"input": 0, "cache": 0, "message": message}
            self.log(self.username + "/" + str(self.client_id) + " failed to send a message!")
            self.send(data)

    def link_state(self):
        user_names = ["Rohan", "Jose", "John", "Amelia"]
        message = "Destination\t\t\t\tPath\t\t\t\tCost\t\t\t\t\n" +\
            "Jose\t\t\t\t{Rohan, Jose}\t\t\t\t15\t\t\t\t\n"+\
            "John\t\t\t\t{Rohan, John}\t\t\t\t10\t\t\t\t\n" +\
            "Amelia\t\t\t\t{Rohan, John, Amelia}\t\t\t\t35\t\t\t\t\n"
        return message

    def get_messages(self):
        """
        Sends the messages of a certain recipient id and sends them to the
        user in a array that contains the frequency and codes (Implementing CDMA).
        """
        max_data_length = 0
        user_bit = []
        encoded_data = []
        message = "\nNumber of unread messages: " + str(Message.num_of_messages(self.client_id)) + "\n" \
                  + "Retrieving messages...Please wait this may take a while..."
        if Message.num_of_messages(self.client_id) == 0:
            message = "\nNumber of unread messages: " + str(Message.num_of_messages(self.client_id)) + "\n"
            data = {"input": 0, "cache": 0, "message": message}
            self.send(data)
            return
        data = {"input": 0, "cache": 0, "cdma": 1, "message": message}
        self.send(data)
        user_messages = Message.get_messages(self.client_id)
        for user_message in user_messages:
            user_bit.append(self.cdma.text_to_bits(user_message))  # converting all messages into bits
        for user in user_bit:  # calc max data length based on bits
            if max_data_length < len(user):
                max_data_length = len(user)
        for user in user_bit:
            while len(user) != max_data_length:  # append data which are shorter to make all data equal length
                user.extend((0, 0, 1, 0, 0, 0, 0, 0))
        code = self.cdma.codes(len(user_bit), 2 * max_data_length)
        i = 0
        for c in code:
            encoded_data.append(self.cdma.encode(user_bit[i], c))  # encode all the data using codes
            i += 1
        freq = self.cdma.encode_all(encoded_data)
        response = [freq, code]
        for c in code:
            response.append(c)
        data_size = sys.getsizeof(response)
        packet = ""
        str_response = str(response)
        x = 0
        while x < len(str_response):  # sends the data in packets to the client
            packet += str_response[x]
            x = x + 1
            if sys.getsizeof(packet) >= 3000:
                self.send(packet)
                packet = ""
        if packet:
            self.send(packet)
        data = "finished"  # indicates all data has been received
        self.send(data)
        self.log(self.username + "/" + str(self.client_id) + " has retrieved "
                 + str(Message.num_of_messages(self.client_id)) + " unread messages!")
        Message.delete_messages(self.client_id)
        finish = self.receive()

    def udp(self):
        """
        Asks for information that will allow the user to send a message using
        UDP.
        """
        self.log(self.username + "/" + str(self.client_id) + " is trying to send a direct message using UDP")
        message = "Enter the recipient ip address: "
        message2 = "Enter the recipient port number: "
        message3 = "Enter the message: "
        data = {"input": 1, "cache": 0, "udp": 1, "message": message, "message2": message2, "message3": message3}
        self.send(data)
        ip = self.receive()
        port = self.receive()
        self.log(self.username + "/" + str(self.client_id) + " has attempted to send a message using UDP to " + ip + "/"
                 + str(port))

    def broadcast(self):
        """
        Broadcasts a message to everyone connected to the server including the sender. This message is stored
        on the server until the client requests to see all messages.
        """
        message = "Enter your message: "
        data = {"input": 1, "cache": 0, "message": message}
        self.send(data)
        user_message = self.receive()
        message = datetime.now().strftime('%Y-%m-%d %H:%M') + ": " + user_message + " (broadcast message from " \
                  + self.username + ")"
        for key, value in self.server.handlers.items():  # Adding message to message dictionary for everyone connected
            Message.add_message(message, key)
        message = "Message sent!"
        data = {"input": 0, "cache": 0, "message": message}
        self.send(data)
        self.log(self.username + "/" + str(self.client_id) + " has broadcast a message!")

    def create_chat_room(self):
        """
        Implementation of option 6 where user can create a chat room
        """
        self.log(self.username + " is creating a chatroom")
        message = "Enter the new channel id: "
        data = {"input": 1, "cache": 0, "message": message}
        self.send(data)
        channel_id = self.receive()
        for active_id in ClientHandler.chat_rooms:
            if channel_id == active_id.id:
                message = "\nChannel with ID " + str(channel_id) + "is already active\n"
                data = {"input": 0, "cache": 0, "message": message}
                self.send(data)
                return  # insert logic for if channel id is active
        chat_room = ChatRoom(channel_id, self.client_id)
        chat_room.users.append(self.username)
        ClientHandler.chat_rooms.append(chat_room)
        message = ("Private key received from server and channel " + str(
            channel_id) + " was successfully created!\n\n" +
                   "----------------------- Channel " + str(channel_id) + " ------------------------" +
                   "\n\nAll the data in this channel is encrypted\n\nGeneral Admin Guidelines:\n" +
                   "1. #" + self.username + " is the admin of this channel\n2. Type '#exit' to " +
                   "terminate the channel (only for admins)\n\nGeneral Chat Guidelines:\n" +
                   "1. Type #exit to exit from this channel.\n" +
                   "2. Use #<username> to send a private message to that user.\n\n" +
                   "Waiting for other users to join....\n")
        data = {"input": 0, "cache": 0, "message": message}
        self.send(data)
        message = channel_id
        data2 = {"pgpadmin": 1, "cache": 0, "message": message}
        self.send(data2)
        self.message_thread()
        while True:
            data = self.receive()
            if "#exit" in data:
                message = "\nClosing channel " + channel_id
                data2 = {"input": 0, "cache": 0, "message": message}
                ClientHandler.chat_rooms.remove(chat_room)
                self.send(data2)
                return
            for user in chat_room.users:
                test_message = "#" + user
                if test_message in data:
                    data = self.username + " (private message)> " + data
                    if user in ChatRoom.messages:
                        ChatRoom.messages[user].append(data)
                        continue
                    else:
                        ChatRoom.messages[user] = []
                        ChatRoom.messages[user].append(data)
                        continue
            else:
                data = self.username + "> " + data
                for user in chat_room.users:
                    if user == self.username:
                        continue
                    #if user not in chat_room.users:
                    #    return
                    if user in ChatRoom.messages:
                        ChatRoom.messages[user].append(data)
                    else:
                        ChatRoom.messages[user] = []
                        ChatRoom.messages[user].append(data)
                # message = ""
                # data2 = {"input": 1, "cache": 0, "message": message}
                # self.send(data2)

            # check to see if channel id key and username

    def check_chat_room(self):
        while True:
            if self.username in ChatRoom.messages.keys():
                for cr_message in ChatRoom.messages[self.username]:
                    self.send(cr_message)
                ChatRoom.messages[self.username].clear()

    def message_thread(self):
        Thread(target=self.check_chat_room, args=()).start()

    def join_chat_room(self):
        """
        Implementation of option 7 where user can join an active chat room
        """
        test_message = ""
        self.log(self.username + " is trying to join a chatroom")
        active_room = False
        message = "Enter the new channel id: "
        data = {"input": 1, "cache": 0, "message": message}
        self.send(data)
        channel_id = self.receive()
        for active_id in ClientHandler.chat_rooms:
            if active_id.id == channel_id:
                active_room = True
                chat_room = active_id
        if active_room is False:
            message = "\nThis is not an active channel id. Please try again\n"
            data = {"input": 0, "cache": 0, "message": message}
            self.send(data)
            return
        chat_room.users.append(self.username)
        message = "----------------------- Channel " + str(channel_id) + "------------------------\n" \
                                                                         "All the data in this channel is encrypted\n" + \
                  self.username + " has just joined\n"
        for user in chat_room.users:
            if user == chat_room.admin:
                print(user + " is the admin!\n")
            else:
                print(user + " is already on the server!\n")
        message += "1. Type #exit to exit from this channel.\n" +\
                   "2. Use #<username> to send a private message to that user.\n\n" +\
                   "Waiting for other users to join....\n"
        data = {"input": 0, "cache": 0, "message": message}
        self.send(data)
        message = ""
        data2 = {"pgpadmin": 1, "cache": 0, "message": message}
        self.send(data2)
        self.message_thread()
        while True:
            data = self.receive()
            private = False
            if "#exit" in data:  # change to bye later
                message = "\nExiting channel " + channel_id
                data2 = {"input": 0, "cache": 0, "message": message}
                #for j in range(0, len(chat_room.users)):
                    #if self.username == chat_room.users[j]:
                self.send(data2)
                return
            for user in chat_room.users:
                test_message = "#" + user
                if test_message in data:
                    if user in ChatRoom.messages:
                        data += self.username + " (private message)> " + data
                        ChatRoom.messages[user].append(data)
                        private = True
                    else:
                        ChatRoom.messages[user] = []
                        ChatRoom.messages[user].append(data)
                        private = True
            else:
                if private is False:
                    data = self.username + "> " + data
                #if user not in chat_room.users:
                 #   return
                    for user in chat_room.users:
                        if user == self.username:
                            continue
                        if user in ChatRoom.messages:
                            ChatRoom.messages[user].append(data)
                        else:
                            ChatRoom.messages[user] = []
                            ChatRoom.messages[user].append(data)
                # message = ""
                # data2 = {"input": 1, "cache": 0, "message": message}
                # self.send(data2)

    def create_bot(self):
        self.log("Creating bot!")
        message = "Enter the name of your bot: "
        data = {"input": 1, "cache": 0, "message": message}
        self.send(data)
        name = self.receive()
        bot = Bot(name, self.client_id)
        ClientHandler.bots.append(bot)
        bot_message = "The disabled permissions for this bot are:\n" + \
                     "1. Welcome users right after they join a channel. \n" + \
                     "2. Show a warning to the users when they send words that are not allowed\n" + \
                     "3. Drop users from the channel after 3 warnings\n" + \
                     "4. Compute the response time of a message when the user request it\n" + \
                     "5. Inform the user when it has been inactive on the channel for more than 5 minutes.\n\n" + \
                     "Enter an integer to enable a set of permissions: "
        data = {"input": 1, "cache": 0, "message": bot_message}
        self.send(data)
        permissions = self.receive()
        bot.set_permission(permissions)
        message = str(bot.name) + "'s Configuration:\n" +\
            "\nToken: " + str(bot.token) +\
            "\nPermissions Enabled: " + str(bot.permissions) +\
            "\nStatus: Ready"
        data = {"input": 0, "cache": 0, "message": message}
        self.bots.append(bot)
        self.send(data)


    def run(self):
        """
        Runs the client handler
        """
        try:
            self.log(self.username + " has connected\nClient ID: " + str(self.client_id))
            menu = Menu()
            while True:
                menu.send_menu(self)
                menu.get_option(self)
        except ConnectionResetError as msg:
            print("\n" + self.username + " has disconnected\nClientID: " + str(self.client_id))
            self.server.handlers.pop(self.client_id)
