from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import pickle
import json
HEADERSIZE = 10
FORMAT = 'utf-8'
def revMenu(client):
    try:
        client.sendall(bytes("Menu",FORMAT))
    except:
        print("Connection error")

    flag = True
    full_msg = b''
    new_msg = True
    counter = 1
    while counter != 8:
        fname = 'img' + str(counter) + '.png'
        print(counter)
        while flag:
            msg = client.recv(2048)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
            full_msg += msg

            if len(full_msg)-HEADERSIZE == msglen:
                if(counter == 7):
                    open("menu.json","wb").write(pickle.loads(full_msg[HEADERSIZE:]))
                    with open('menu.json') as f:    
                        data = json.load(f)   
                    for food in data:
                        print("{}: {} VND {}" .format(food['food'], food['price'],food['note']))
                    f.close()
                    break

                open(fname,"wb").write(pickle.loads(full_msg[HEADERSIZE:]))
                new_msg = True
                full_msg = b""
                flag = False
        counter += 1
        flag = True
  
def Order(client):
    try:
        client.sendall(bytes("Order",FORMAT))
    except:
        print("Connection error")
    while True:
        resquest = input("Mon an muon Order:(Pizza, Pasta, Salad, Spaghetti, Bierre, Pudding)")
        if resquest == "Pizza":
            client.sendall(resquest.encode(FORMAT)) 
            amount = input("So luong: ")
            client.sendall(amount.encode(FORMAT))
        elif resquest == "Pasta":
            client.sendall(resquest.encode(FORMAT)) 
            amount = input("So luong: ")
            client.sendall(amount.encode(FORMAT))
        elif resquest == "Spaghetti":
            client.sendall(resquest.encode(FORMAT)) 
            amount = input("So luong: ")
            client.sendall(amount.encode(FORMAT))
        elif resquest == "Bierre":
            client.sendall(resquest.encode(FORMAT)) 
            amount = input("So luong: ")
            client.sendall(amount.encode(FORMAT))
        elif resquest == "Pudding":
            client.sendall(resquest.encode(FORMAT)) 
            amount = input("So luong: ")
            client.sendall(amount.encode(FORMAT))
        elif resquest == "Salad":
            client.sendall(resquest.encode(FORMAT)) 
            amount = input("So luong: ")
            client.sendall(amount.encode(FORMAT))
        elif resquest == "no":
            client.sendall(bytes("Thanh toan",FORMAT))
            break

    sum = client.recv(1024).decode(FORMAT)
    print("So tien can thanh toan:", sum)   

def Pay(client):
    try:
        client.sendall(bytes("Pay",FORMAT))
    except:
        print("Connection error")
    method = input("Type of payments(VISA, CASH): ")
    client.sendall(str(method).encode(FORMAT))
    if method == "VISA":
        account_number = input("Enter the account number: ")
        client.sendall(str(account_number).encode(FORMAT))
        msg = client.recv(1024).decode(FORMAT)
    elif method == "CASH":
        msg = client.recv(1024).decode(FORMAT)

    if msg == "Re-enter the account number":
        while True:
            account_number = input("Re-enter the account number: ")
            client.sendall(str(account_number).encode(FORMAT))
            msg = client.recv(1024).decode(FORMAT)
            if msg == "Payment success":
                break
    print(msg)
def control(client, temp):
    temp = int(temp)
    # Pay(client)
    if (temp == 1):
        revMenu(client)
    elif (temp == 2):
        Order(client)
    elif (temp == 3):
        Pay(client)
    
def receive(client):
    print("Connect to server successfully")
    while True:
        try:
            temp = input("1: Menu \n2: Order \n3: Pay \nOption: ")
            temp = int(temp)
            rcv = Thread(target=control(client,temp))
            rcv.start()
        except:
            print("ERROR!")
            client.close()
            break

def connectServer(HOST):
    global Host
    Host = HOST
    client = socket(AF_INET,SOCK_STREAM)
    try: 
        client.connect((HOST, 5656))
        client.send(bytes("Success", 'utf-8'))
        rcv = Thread(target=receive(client))
        rcv.start()
    except:
        print("Warning!!!", "Connection error ")

connectServer("192.168.28.79")