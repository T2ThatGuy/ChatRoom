from styles import Colours
import threading
import socket
import os

os.system("")

print("[" + Colours.GREEN + "Start Up" + Colours.RESET + "] Server is starting up...")

HOST = '127.0.0.1' # localhost
PORT = 25570

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            nicknames.remove(nickname)

            print('[' + Colours.GOLD + f'{nickname}' + Colours.RESET + '] has left the chat room!' )
            broadcast(f'[{nickname}] has left the chat!'.encode('ascii'))

            break

def receive():
    while True:
        client, address = server.accept()
        print("[" + Colours.CYAN + "New Connection" + Colours.RESET + "]" + f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)

        print("[" + Colours.GOLD + "Nickname" + Colours.RESET + "]" + f"Nickname of client is {nickname}")
        broadcast((f"[{nickname}] has joined the chat!".encode('ascii')))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("[" + Colours.LIME + "Complete" + Colours.RESET + "]" + "Chat Room is now listening for new connections...")
receive()