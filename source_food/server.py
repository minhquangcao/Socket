import socket
from threading import Thread
import time
import pickle
import json
import re
HEADERSIZE = 10
FORMAT = 'utf-8'

def Menu(client):
    try:
        counter = 1
        while counter != 7:
            fname = 'Resources/img' + str(counter) + '.png'
            img = open(fname,"rb").read()
            msg = pickle.dumps(img)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", FORMAT)+msg
            client.sendall(msg)
            counter += 1
            time.sleep(0.1)
            # img.close()
        d = open("Resources/data.json","rb").read()
        msg = pickle.dumps(d)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", FORMAT)+msg
        client.sendall(msg)
    except:
        print("Can't send")
    

def Order(client):
    try:
        dict = '''
        {
            "order":[
            {
                "Pizza": 0,
                "Pasta": 0,
                "Salad": 0,
                "Spaghetti": 0,
                "Bierre": 0,
                "Pudding": 0,
                "status": false
            }
            ]
        }
        '''
        data = json.loads(dict)
        while True:
            amount = 0
            request = client.recv(1024).decode(FORMAT)
            if request == "Pizza": amount = client.recv(1024).decode(FORMAT)
            elif request == "Pasta": amount = client.recv(1024).decode(FORMAT)
            elif request == "Spaghetti": amount = client.recv(1024).decode(FORMAT)
            elif request == "Bierre": amount = client.recv(1024).decode(FORMAT)
            elif request == "Salad": amount = client.recv(1024).decode(FORMAT)
            elif request == "Pudding": amount = client.recv(1024).decode(FORMAT)
            elif request == "Thanh toan":
                with open("order.json", "w") as f:
                    json.dump(data,f, indent = 2)
                    break   
            for items in data['order']:
                items[request] = int(amount)
                print(items[request])

        for money in data['order']:
            sum = money["Pizza"] * 250000 + money["Pasta"] * 135000 + money["Spaghetti"] * 230000 +  money["Salad"] * 100000 + money["Pudding"] * 35000 + money["Bierre"] * 35000
        sum = str(sum)
        client.sendall(bytes(sum,FORMAT))
        
        with open("order.json", "w") as f:
            json.dump(data,f, indent = 2)
    
    except:
        print("Can't order")

def checkString(str):
    pattern = re.compile("[0-9]+")
    if ((pattern.fullmatch(str) is None) or (len(str) < 10)):
        return False
    return True

def Pay(client):
    try:
        method = client.recv(1024).decode(FORMAT)
       
        method = str(method)
        pattern = re.compile("[0-9]+")
        while True:

            # if found match (entire string matches pattern)
            if method == "VISA":

                account_number = client.recv(1024).decode(FORMAT)
                if checkString(account_number) is True:
                    client.sendall(bytes("Payment success", FORMAT))
                    with open("order.json") as f:
                        source = json.load(f)

                    for item in source['order']:
                        item['status'] = True

                    with open("order.json", "w") as f:
                        json.dump(source,f, indent = 2)
                    break
                else:
                    print("hello")
                    # if not found match
                    client.sendall(bytes("Re-enter the account number", FORMAT))
                    # Pay(client)
            elif method == "CASH":
                client.sendall(bytes("Payment success", FORMAT))
                break
    except:
        print("can't recv")
# Receive request from client
def readRequest(client):
    request = ""
    try:
        request = client.recv(1024).decode('utf-8')
    finally:
        return request


# Choose option from request
def takeRequest(client):
    while True:
        Request = readRequest(client)
        print(Request)
        if not Request:
            client.close()
            break
        print("Request from client: \n")
        #take a picture
        if "Menu" == Request:
            Menu(client)
        if "Order" == Request:
            Order(client)
        if "Pay" == Request:
            Pay(client)
def Serveur():
    try:
        SERVER.listen()
        ACCEPT_THREAD = Thread(target = waitingConnection())
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except: 
        print("ERROR!")
    finally:
        SERVER.close()
#wait to connect for client 
def waitingConnection():

    print("Waiting for Client")

    while True:
        client, Address = SERVER.accept()
        print("Client", Address, "connected!")
        Thread(target = takeRequest(client)).start()

print("Server IP Address Now ", (socket.gethostbyname(socket.gethostname())))
SERVER =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind((socket.gethostbyname(socket.gethostname()), 5656))
Serveur()