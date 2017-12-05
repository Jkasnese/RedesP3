import util_com

class Client():
    
    def __init__():

        # Gets server IP
        self.server_ip = input("Digite o IP do servidor: ") # DNS role
        
        # Stablishes connection with loadbalancer
        self.tcp_socket = open_TCP_socket()
        self.tcp_socket.connect((self.server_ip, 8080))

        # Load balancer accepts connection and sends back the server IP.
        addr = listen_TCP(self.tcp_socket)

        # Redirected to server
        self.tcp_socket.close()
        self.tcp_socket.connect((addr, 8080))

        # Sends msg requesting information
        send_msg("3", addr, 8080, self.tcp_socket)

        
        
