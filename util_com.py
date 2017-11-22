import socket
import struct

group = '224.1.1.1'
port = 5007

def create_multicast_socket(group, port):
    """ Receives a multicast group address and sets it to port.
    Return the created socket """

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # # CONFIGURING SOCKET # #
    # UDP to reuse same address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Configuring TTL number (number of routers msg is allowed to pass through)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2) 

    # Configuring LOOPBACK (receive the msg sent to the multicast group). 1 enabled 0 disabled
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

    # Bind group,port tuple to socket
    sock.bind((group, port))  # use MCAST_GRP instead of '' to listen only
                                 # to MCAST_GRP, not all groups on MCAST_PORT

    # Defines a struct contaning multicast addres group and local interface group (INADDR_ANY)
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)

    # Adds previous struct to the multicast listening group
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock


def listen_socket(sock):
    """ From the received socket return data and address of sender s"""
    while True:
        data, addr = sock.recvfrom(1024) # Buffer size 1024
        return bytes.decode(data), addr

def send_msg(message, sock):
    """ Sends a received message to the socket multicast """
    sock.sendto(message.encode('utf-8'))
    return

def open_TCP_socket(port=8080, host=''):
    #   - - -   Criando socket - - - 
    try:
        # Retorna descrição do socket
        # Cria um socket da familia de endereços INET, usado pra protocolos ipv4.
        #   A familia de endereços diz que tipos de endereços podem se acoplar a esse socket. Pra internet, INET. Tem tb INET6 pra ipv6.
        bocal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print ('Nao foi possivel criar o socket. Erro: ' + str(msg[0]) + ' , Mensagem: ' + msg[1])
        sys.exit();

    #   - - - Atribuindo dados ao socket - - - 
    try:
        # Atribuindo ao meu socket atual o nome HOST e a porta do socket.
        bocal.bind((host, porta))
    except socket.error as msg:
        print ('Erro na atribuicao. Codigo: ' + str(msg[0]) + ' Mensagem: ' + msg[1])
        sys.exit()

    return bocal

""" Pede um socket e retorna a string de resposta"""
def listen_TCP(bocal):
    # Deixar a thread pra sempre recebendo dados
    while True:
        # data recebe os dados de no maximo 1024 bytes, neste caso.
        mensagem = (bocal.recv(1024)).decode('utf-8')
        # Seja educado e responda
        return mensagem        

def acept_connections(bocal, lista_conexoes):
    # Ouvindo
    while True:
        # Coloca na lista uma tupla contendo bocal de conexão e endereço
        conexao = bocal.accept()
        lista_conexoes.put(conexao)
        lista_conexoes.task_done()
        print ("Nova conexão TCP! " + conexao[1][0] + ':' + str(conexao[1][1]))





