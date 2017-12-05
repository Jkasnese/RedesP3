import util_com
import util_app_protocol

class Client():
    
    def __init__(self):

        # Client itens info
        self.itens = []

        # Gets server IP
        self.server_ip = input("Digite o IP do servidor: ") # DNS role
        
        # Stablishes connection with loadbalancer
        self.tcp_socket = open_TCP_socket()
        self.tcp_socket.connect((self.server_ip, 8080))

        # Load balancer accepts connection and sends back the server IP.
        self.server_addr = listen_TCP(self.tcp_socket)

        # Redirected to server
        self.tcp_socket.close()
        self.tcp_socket.connect((self.server_addr, 8080))

        # Sends msg requesting information
        send_msg("3", self.server_addr, 8080, self.tcp_socket)

        # Receives msg and loads page with info
        server_info = listen_TCP(self.tcp_socket)
        self.retrieve_info(server_info)

    def retrieve_info(self, server_info):
        """
        Retrieves answer from server and organizes it in a logical way on the client side
        """
        itens = server_info.split(list_itens)

        print("Lista de itens: ")
        for i in itens:
            # Print to client
            print(i + '\n')
            
            # Organize in lists
            info = i.split(space_char)
            item = []
            for j in info:
                # [itemID, itemName, qtt]
                item.append(j)
            self.itens.append(item)
        
        
    def buy_item(self, item_ID, qtt):
        
        # Sends msgs to server requesting buying that item
        send_msg("4" + item_ID + space_char + str(qtt), self.server_addr, 8080, self.tcp_socket)

        # Waits for answer
        answer = listen_TCP(self.tcp_socket)
    
        if (0 == answer):
            print("Proceed to payment methods")
        else:
            print("O item que voce requisitou nao pode ser comprado, pois ja acabou o estoque: " + item_ID)

    def pick_item(self):
        return (input("Digite o ID do produto: "), int(input("Digite a quantidade: ")) )

client = Client()
buy = client.pick_item()
client.buy_item(buy[0], buy[1])
        

        
