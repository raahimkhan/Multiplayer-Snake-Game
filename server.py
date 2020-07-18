import threading
import socket
import time
from Snake import *
from Constants import *
import pickle 
import copy

clients = []
lock = threading.Lock()

class client:
    def __init__(self, id, c_socket):
        self.c_socket = c_socket
        self.id = id
        self.snk = snake(id, HEIGHT, WIDTH)
        self.is_active = True

def game_thread(client):
    dir = VEC_RIGHT
    while True:
        
        all_ids_edges = []
        allSnakes = []
        win = False

        if len(clients) == 1:
            win = True

        lock.acquire()

        
        for eachClient in clients:
            allSnakes.append(eachClient.snk)
            thisDict = {"id":eachClient.id, "edges":eachClient.snk.edges, "win":win}
            all_ids_edges.append(thisDict)

            
        lock.release()

        to_be_sent = pickle.dumps(all_ids_edges)

        client.c_socket.sendall(to_be_sent)

        if win:     ###IF THE CLIENT WON, CLOSE ITS SOCKET AND REMOVE FROM CLIENTS LIST
            client.c_socket.close()
            clients.remove(client)
            break
        
        lock.acquire()
            
        try:
            to_be_recv = client.c_socket.recv(100)
            dir = pickle.loads(to_be_recv)
            client.snk.updateSnake(dir)
            client.is_active = client.snk.isAlive(allSnakes, HEIGHT, WIDTH)
        except Exception as e:
            client.is_active = False
            print(e, ' ', client.id)

        lock.release()

        if(client.is_active == False):
            client.c_socket.close()
            clients.remove(client)
            break



def clients_connecting(s_socket):
    s_socket.listen(5)
    c_socket, addr = s_socket.accept()
    clientId = len(clients) + 1
    thisClient = client(clientId, c_socket)
    clients.append(thisClient)

    starting_info = {"id":clientId, "height":HEIGHT, "width":WIDTH}
    c_socket.sendall(pickle.dumps(starting_info))


def main():

    s_socket = socket.socket()
    s_socket.bind(SERVER)

    s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    threads = []

    while len(clients) < MAX_CONNECTIONS:  # CAN CHANGE FROM CONSTANTS FILE
        clients_connecting(s_socket)

    time.sleep(0.1)  # wait for all clients to have received their info

    for client in clients:
        t = threading.Thread(target = game_thread, args = [client])
        t.daemon = True
        t.start()
        threads.append(t)
   
    for t in threads:  # WAIT FOR ALL THREADS TO FINISH
        t.join()


main()
