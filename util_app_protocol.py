# THIS FILE CONTAINS THE APPLICATION PROTOCOL FOR REDESP3

space_char = ';'
list_divisor = ','
list_itens = '|'

# 0 = Server asks for updates upon reconnecting
# 1 = Response from the others servers to the update message
# 2 = Update item.
    #Message: 2WarehouseID;ItemID;ItemName;Qtt. If Qtt > 0, adding item. If qtt < 0, removing item.
# 3 = Client requests info
    # Message: 3
    # Answer: [ [itemID, itemName, qtt], [itemID, itemName, qtt] ] "itemID;itemName;Qtt|itemID..."
# 4 = Client requests buying item
    #Message: 4itemID;qtt


#  = Redirect client to server
    # From loadbalancer to client, message:"ServerIP"

