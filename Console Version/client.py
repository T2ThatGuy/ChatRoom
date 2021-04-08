import socket
import threading
import os

MESSAGES = []

print('[Connection] Connecting to the server!') 

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 25570))
except ConnectionRefusedError:
    print('[ERROR] An error occured while trying to connect to the server!')
    quit()

print('[Connection] Successfully connected to the chatroom!')

nick = input('[Nickname] What is your nickname: ')

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def addMessage(message):
    MESSAGES.append(message)

def printMessages():
    cls()
    for msg in MESSAGES:
        print(msg)

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nick.encode('ascii'))
            else:
                addMessage(message)
                printMessages()
        except:
            print('[ERROR] An Error occurred whilst receiving data from the server')
            client.close()
            quit()

def write():
    while True:
        message = f'{nick}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()