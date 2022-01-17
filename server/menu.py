#######################################################################################
# File:             menu.py
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# IMPORTANT:        This file can only resides on the server side.
# Usage :           menu = Menu() # creates object
#
########################################################################################

class Menu:
    """
    IMPORTANT MUST READ: The Menu class is the user interface that acts as a communication bridge between the user
    and the Client-Server architecture of this application. The Menu is always located on the Server side (machine running the server).
    However, it must be printed on the Client console by the ClientHelper object. In order to accomplish this, students
    must create a
    """

    @staticmethod
    def send_menu(server):
        """
        Shows the following menu on the client side
        ****** TCP/UDP Network ******
        ------------------------------------
        Options Available:
        1.  Get users list
        2.  Send a message
        3.  Get my messages
        4.  Send a direct message with UDP protocol
        5.  Broadcast a message with CDMA protocol
        6.  Create a secure channel to chat with your friends using PGP protocol
        7.  Join an existing channel
        8.  Create a Bot to manage a future channel
        9.  Map the network
        10.  Get the Routing Table of this client with Link State Protocol
        11. Get the Routing Table of this network with Distance Vector Protocol
        12. Turn web proxy server on (extra-credit)
        13. Disconnect from server

        Your option <enter a number>:
        """
        menu = "\n\n****** TCP/UDP Network ******\n------------------------------------\nOptions Available:\n1.  Get users list\n2.  Send a message\n3.  Get my messages\n4.  Send a direct message with UDP protocol\n5.  Broadcast a message with CDMA protocol\n6.  Create a secure channel to chat with your friends using PGP protocol\n7.  Join an existing channel\n8.  Create a Bot to manage a future channel\n9.  Map the network\n10. Get the Routing Table of this client with Link State Protocol\n11. Get the Routing Table of this network with Distance Vector Protocol\n12. Turn web proxy server on (extra-credit)\n13. Disconnect from server\n\nYour option <enter a number>: "
        data = {"input": 1, "cache": 0, "message": menu}
        server.send(data)

    @staticmethod
    def get_option(server):
        """
        TODO: Ask the user to select an option from the menu
              Note. you must handle exceptions for options chosen that are not in the allowed range
        :return: an integer representing the option chosen by the user from the menu
        """
        option = server.receive()
        if option == "1":
            server.send_user_list()
        elif option == "2":
            server.send_message()
        elif option == "3":
            server.get_messages()
        elif option == "4":
            server.udp()
        elif option == "5":
            server.broadcast()
        elif option == "6":
            server.create_chat_room()
        elif option == "7":
            server.join_chat_room()
        elif option == "8":
            server.create_bot()
        elif option == "9":
            server.send_map()
        elif option == "10":
            server.send_map()
            server.send_link_state()
        elif option == "11":
            server.send_map()
            server.send_distance_vector()
        elif option == "12":
            server.get_proxy()
        elif option == "13":
            server.disconnect_client()
        else:
            return


menu = Menu

