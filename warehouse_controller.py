import uuid
import util_com

class Warehouse:

    def __init__():
        # Warehouse atributes
        self.warehouse_id = 0 # How do I generate sequential warehouse ids?
        self.itens = [] # Itens list. Each item is a list. 0 ID, 1 Name, 2 Qtt, 3 Warehouses that has the item
        
        # Asks servers multicast address for future msgs
        self.servers_multicast_address = input("Digite o endereco de multicast dos servidores: ")
        self.mcast_port = input("Digite a porta de destino multicast: ")

    def register_itens (self, name, qtt):
        # Stablishes new item ID
        identification = str(uuid.uuid4())

        # Appends item to the list of itens
        self.itens.append([identification, name, qtt])

        # Persist on file
        self.persist()

        # Updates servers
        #Message: 2WarehouseID;ItemID;ItemName;Qtt. If Qtt > 0, adding item. If qtt < 0, removing item.
        send_msg('2' + str(self.warehouse_id) + space_char + identification + space_char + name + space_char + str(qtt), self.servers_multicast_address, self.mcast_port)

    
    def remove_itens (self, identification, qtt):
        index = search_item(identification)
        if (self.itens[index][2] =< qtt): # If qtt to remove is greater than available qtt, remove item from list.
            self.itens.pop(index)
        else: # If not, remove the necessary quantity.
            self.itens[index][2] -= qtt

        # Persist on file
        self.persist()

        # Updates servers
        #Message: 2WarehouseID;ItemID;ItemName;Qtt. If Qtt > 0, adding item. If qtt < 0, removing item.
        send_msg('2' + str(self.warehouse_id) + space_char + identification + space_char + name + space_char + str(qtt), self.servers_multicast_address, self.mcast_port)


    """ 
    Receives item ID
    Returns item index on itens list
    """
    def search_item (self, identification):
        for i in self.itens:
            if (identification == i[0]):
                return i


    """
    Overwrites the current database on a file called warehouse_id
    """
    def persist(self):

        # Open file to write
        database = open('warehouse_' + warehouse_id, 'w')

        # Write header
        database.write(warehouse_id + "\n")

        # Write database
        for i in self.itens:
            # Writes: ID NAME QTT\n
            database.write(i[0] + space_char + i[1] + space_char + i[2] + '\n')
