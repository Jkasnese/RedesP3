from util_com import *
import uuid
import Thread

class Server:
    """
    The server contains info about the set of itens;
    Connects the client to the website;
    Keeps consistency;
    """
    
    def __init__(self):
        # # # # # DATA # # # # # 
        # Defines server ID
        self.serverID = str(uuid.uuid4())

        # Opens log file. 
        # Appends to file in case it exists, meaning the server lost connection, and attempts to recover lost messages during disconnect time
        # If it doesn't exists means that it's a new server with consistent DB. Creates log file with server ID on the first line
        try:
            with open('server_log.txt', 'a') as self.log_file:
                self.reconnect()
        except IOError:
            with open ('server_log.txt', 'w') as self.log_file:
                self.log_file.write("# LOG FILE FOR SERVER " + self.serverID + "\n")

        # # # # # COMMUNICATION # # # # #
        # # UDP
        # Server joins multicast group
        self.server_multicast_socket = join_multicast_server()
        thread_listen_group = Thread(target = self.listen_messages, args=(self.server_multicast_socket,), daemon=True)
        thread_listen_group.start()
        
    def join_multicast_server(self):
        """
        Asks for a multicast address and connects to it.
        """
        group = input("Digite o endereco do grupo multicast: ")
        port = input("Digite a porta p se conectar ao grupo multicast: ")
        return create_multicast_socket(group, port)

    def listen_messages(self, sock):
        """
        Listen for incoming messages to the sock in arguments.
        """
        message = "@"
        while ('' != message):
            message, addr = listen_socket(sock)
            # If it's an UDP socket, it received (msg,addr). If it's TCP, only (msg). Hence:
            if ('' == message): # Empty string '' means that the other contact closed the socket
                break; # Doesn't really applies to UDP but could be used by TCP
            else: 
                # If it's a valid message, pass to handle_message so it can be, well... handled.
                print("Reading message... ")
                self.handle_message(message)
                                
        sock.close()

    def handle_message(self, message):
        """
        Receives a message and treats it accordingly to the application protocol defined in util_app_protocol.py
        """
        if ('0' == message[0]):
            self.update_server(message[1:])
        else if ('1' == message[0]):
            self.update_self(message[1:])

    def reconnect(self):
        """
        Once the server reconnects it asks the other servers for lost messages
        """     
        message = "0" + "Ultimo log etc"
        send_msg(message, self.server_multicast_socket)
        print("Sent: " + message)
        return

    def update_server(self, message):
        """
        Sends info the server attempting to reconnect
        """   
        print(message)

    def update_self(self, message):
        """
        Updates self with info received from other servers        
        """
        print("Updating self")



        

