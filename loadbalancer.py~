import util_com
from queue import Queue
from threading import Thread

class Load_Balancer():
    """
    Receives connections and distributes the connection to the servers
    """

    def __init__():

        # Create server list
        self.servers = []
        self.index = 0
        number_of_servers = int(input("Digite a quantidade de servidores: "))
        for i in range(number_of_servers):
            server = input("Digite o endereco do servidor: ") # Server addrs
            self.servers.append(server)
        
        # # # # Create TCP connection # # # # 
        # Open socket
        self.sock = open_TCP_socket()

        # Listen to 10 simultaneos connections
        self.sock.listen(10) 

        # Acepts connections and puts new socket (the connection socket) into the thread safe queue
        connections_list = Queue()
        open_connections_thread = Thread(target = accept_connections, args=(self.sock, connections_list))
        open_connections_thread.start()

        # Socket é retirado da fila e passado para função de ouvir, p/ que servidor registre as mensagens do socket.
        # Recebe tupla contendo socket e endereço
        handle_messages_thread = Thread(target = self.handle_connections, args=(connections_list,))
        handle_messages_thread.start()

    def handle_connections(self, connections_list):
        while True:
            sock = connections_list.get()
            addr = bocal[1]
            sock = bocal[0]
            
            # Sends to the client the server address
            send_msg(self.servers[self.index], addr[0], addr[1], sock)
            # Changes next server to be sent
            if (self.index == len(self.servers)-1):
                self.index = 0
            else:
                self.index += 1

load = Load_Balancer()
