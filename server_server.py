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
        self.itens = {} # Key: item ID. Value: [[item_Name], [WarehouseID, Qtt], [WarehouseID, Qtt] ]
        self.itens_list = []

        # # # # # COMMUNICATION # # # # #
        # # UDP
        # Server joins multicast group
        self.server_multicast_socket = self.join_multicast_server()
        thread_listen_group = Thread(target = self.listen_messages, args=())
        thread_listen_group.start()

        # # # # # SERVER LOG # # # # # 
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

    def listen_messages(self, sock):
        """
        Listen for incoming messages to the sock in arguments.
        """
        message = "@"
        while ('' != message):
            print("Waiting msgs...")
            message, addr = listen_socket(sock)

            if ('' == message): # Empty string '' means that the other contact closed the socket
                break; # Doesn't really applies to UDP but could be used by TCP
            else: 
                print("Reading message... ")
                print(message)

                # If it's a valid message, pass to handle_message so it can be, well... handled.
                # If its UDP, its a server action. If it's TCP, must respond
                # If it's an UDP socket, it received (msg,addr). If it's TCP, only:                
                if (None == addr):
                    self.handle_message(message, sock)
                else:
                    self.handle_message(message)

        sock.close()

    def listen_client(self):
        """
        Listen to messages that came from a client
        """
        

    def handle_message(self, message, sock=None):
        """
        Receives a message and treats it accordingly to the application protocol defined in util_app_protocol.py
        """
        if ('0' == message[0]):
            self.update_server(message[1:])
        elif ('1' == message[0]):
            self.update_self(message[1:])
        elif ('2' == message[0]):
            self.warehouse_update(message[1:])
        elif ('3' == message[0]):
            self.send_info_client(message[1:], sock)

    def read_logfile(self, logfile):
        while ('' != logfile):
            # Read line
            # Line format: ProductID;[ [WarehouseID,Qtt], [WarehouseID, Qtt] ]. Remember "[]" doesnt exists on file.
            line = logfile.readline().split(space_char)
            item_ID = line[0]            

            # Adds item ID to item list
            self.itens_list.append(item_ID)

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

    def warehouse_update(self, message):
        """
        Updates the server with message from warehouse.
        Messages from warehouse have the following format, defined in util_app_protocol.py:
            #Message: WarehouseID;ItemID;ItemName;Qtt. If Qtt > 0, adding item. If qtt < 0, removing item.
        """
        # Separate data
        message = message.split(space_char)

        # Gets data from msg
        warehouse_ID = message[0]
        item_ID = message[1]
        item_name = message[2]
        qtt = message[3]
        value = [warehouse_ID, qtt]

        # If item is on server, checks if there's data about that warehouse already.
        # If there is, update qtt.
        # If not, create list containing warehouse.
        # If item isn't on server, create item.

        #Checks if item is in the server
        if (item_ID in self.itens):
            index = -1
            # Checks if warehouse is present and find its index.
            for warehouse in self.itens[item_ID]:
                if (warehouse[0] == warehouse_ID):
                    index = self.itens[item_ID].index(warehouse)
                    break;
            
            # If warehouse is present    
            if (index != -1):
                # Updates qtt. If qtt*-1 > actual qtt, means remove all items.
                if (qtt*-1 >= self.itens[item_ID][index][1]):
                    self.itens[item_ID][index][1] = 0
                # If not to remove all, update qtt:
                else:
                    self.itens[item_ID][index][1] += qtt
            # If warehouse is not present, adds warehouse
            else:
                self.itens[item_ID].append(value)
        # If item isn't on server
        else:
            # Adds item to dictionary
            self.itens[itemID] = [[item_name], [value]]

    def send_info_client(self, sock):
        """
        Sends info to the client upon request
        # Answer: [ [itemID, itemName, qtt], [itemID, itemName, qtt] ] "itemID;itemName;Qtt|itemID..."
        """
        answer = ''
        # # Mounts answer
        # Go through all itens in the server
        for item in self.itens_list:
            answer.append(item + space_char + self.itens[item][0] + space_char) # ItemID;Item_name

            # Find out how many items in total counting all warehouses
            total_qtt = 0
            for warehouses in self.itens[item][1:]:
                total_qtt += warehouses[1]
             
            # Add total qtt for item
            answer.append( str(total_qtt) + list_itens )

        # # Sends answer
        sock.send(answer.encode('utf-8'))
        print("Enviado: " + answer)
        return


server = Server()
print("ID classe:" + str(Server.server_ID))
print("ID instancia:" + str(server.serverID))

