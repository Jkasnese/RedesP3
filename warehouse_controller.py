import uuid

class Warehouse:
    warehouse_id =  # How do I generate sequential warehouse ids?
    itens = [] # Itens list. Each item is a list. 0 ID, 1 Name, 2 Qtt, 3 Warehouses that has the item

    def register_itens (self, name, qtt):
        identification = str(uuid.uuid4())
        self.itens.append([identification, name, qtt])
    
    def remove_itens (self, identification, qtt):
        index = search_item(identification)
        if (self.itens[index][2] =< qtt): # If remove all itens
            self.itens.pop(index)
        else:
            self.itens[index][2] -= qtt


    """ 
    Receives item ID
    Returns item index on itens list"""
    def search_item (self, identification):
        for i in self.itens:
            if (identification == i[0]):
                return i


    """
    Overwrites the current database on a file called warehouse_id"""
    def persist(self):

        # Open file to write
        database = open('warehouse_' + warehouse_id, 'w')

        # Write header
        database.write(warehouse_id + "\n")

        # Write database
        for i in self.itens:
            database.write(i[0] + " " + i[1] + ' ' + i[2] + '\n')
