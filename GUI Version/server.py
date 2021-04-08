import threading, socket, os, pickle
from styles import Colours

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
    tempDict = {
            'Message': 'NICK',
            'Data': None
        }

    client.send(pickle.dumps(tempDict))
    data = client.recv(4096)

    decompiled_data = pickle.loads(data)

    if decompiled_data['Message'] == 'Set Username':
        nickname = decompiled_data['Data']

        nicknames.append(nickname)
        clients.append(client)

        print("[" + Colours.GOLD + "Nickname" + Colours.RESET + "]" + f" Nickname of client is {nickname} ({client})")


    while True:
        try:
            data = client.recv(4096)
            decompiled_data = pickle.loads(data)

            if decompiled_data['Message'] == 'New Message':
                compiled_data = pickle.dumps(decompiled_data)
                broadcast(compiled_data)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            nicknames.remove(nickname)

            print('[' + Colours.GOLD + f'{nickname}' + Colours.RESET + '] has left the chat room!' )
            break

def receive():
    while True:
        client, address = server.accept()
        print("[" + Colours.CYAN + "New Connection" + Colours.RESET + "]" + f"Connected with {str(address)}")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("[" + Colours.LIME + "Complete" + Colours.RESET + "]" + "Chat Room is now listening for new connections...")
receive()