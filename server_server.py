from util_com import *
import uuid
from threading import Thread

class Server:
    """
    The server contains info about the set of itens;
    Connects the client to the website;
    Keeps consistency;
    """

    server_ID = 0
    
    def __init__(self):
        # # # # # SERVER DATA # # # # # 
        # Defines server ID
        self.serverID = str(Server.server_ID)
        self.increase_ID()
        self.itens = {}
        self.all_itens_id = []

        # # # # # COMMUNICATION # # # # #
        # # UDP
        # Server joins multicast group
        self.server_multicast_socket = self.join_multicast_server()
        thread_listen_group = Thread(target = self.listen_messages, args=())
        thread_listen_group.start()

        # # # # # SERVER DATA # # # # # 
        # Log file.
        # Appends new logs to file in case it exists, meaning the server lost connection, and attempts to recover lost messages during disconnect time
        # If it doesn't exists means that it's a new server with consistent DB. Creates log file with server ID on the first line
        try:
            with open('server_' + self.serverID + '_log.txt', 'r') as self.log_file:
                self.reconnect()
        except IOError:
            with open ('server_' + self.serverID + '_log.txt', 'w') as self.log_file:
                self.log_file.write("# LOG FILE FOR SERVER " + self.serverID + "\n")

        # Memory data
        
s    @classmethod
    def increase_ID(klass):
        Server.server_ID += 1
        
    def join_multicast_server(self):
        """
        Asks for a multicast address and connects to it.
        """
        self.group = input("Digite o endereco do grupo multicast: ")
        self.port = int(input("Digite a porta p se conectar ao grupo multicast: "))
        self.my_ip_addr = input("Digite seu IP: ")
        return create_multicast_socket(self.group, self.port, self.my_ip_addr)

    def listen_messages(self):
        """
        Listen for incoming messages to the sock in arguments.
        """
        message = "@"
        while ('' != message):
            print("Waiting msgs...")
            message, addr = listen_socket(self.server_multicast_socket)
            # If it's an UDP socket, it received (msg,addr). If it's TCP, only (msg). Hence:
            #if ('' == message): # Empty string '' means that the other contact closed the socket
             #   break; # Doesn't really applies to UDP but could be used by TCP
            #else: 
                # If it's a valid message, pass to handle_message so it can be, well... handled.
            print("Reading message... ")
            print(message)
            self.handle_message(message)
                            
        sock.close()

    def handle_message(self, message):
        """
        Receives a message and treats it accordingly to the application protocol defined in util_app_protocol.py
        """
        if ('0' == message[0]):
            self.update_server(message[1:])
        elif ('1' == message[0]):
            self.update_self(message[1:])

    def read_logfile(self, logfile):
        while ('' != logfile):
            # Read line
            # Line format: ProductID;[ [WarehouseID,Qtt], [WarehouseID, Qtt] ]. Remember "[]" doesnt exists on file.
            line = logfile.readline().split(space_char)
            item_ID = line[0]            

            # Adds item ID to item list
            self.all_itens_ID.append(item_ID)

            # Gets warehouses lists
            # Line[1] = [ [WarehouseID|Qtt], [WarehouseID, Qtt] ]
            # Warehouse_lists separates 
            warehouses_list_from_file = line[1].split(list_divisor)

            # Gets warehouses qtts
            warehouses_list = []
            for i in warehouses_list_from_file:
                # WarehouseID, ItemQtt
                warehouse_info = i.split(list_itens)

                # Append list to permanent list
                warehouses_list.append([warehouse_info[0],warehouse_info[1]])
                
            # Add item to dictionary
            self.itens{item_ID} = warehouse_list

    def reconnect(self):
        """
        Once the server reconnects it asks the other servers for lost messages
        """     
        message = "0" + "Ultimo log etc"
        port = int(input("Digite a porta pra mandar msg"))
        send_msg(message, self.group, port)
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


server = Server()
print("ID classe:" + str(Server.server_ID))
print("ID instancia:" + str(server.serverID))

