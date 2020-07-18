import curses
import threading
import time
import socket
from Renderer import *
from Constants import *
import pickle


def resurrect(edges):  # edges): ONLY TEMPORARILY IN THE SNAKE CLASS. IS INTEDED TO BE TRANSFERED TO THE CLIENT FILE
    newList = []

    constant = 0
    varriableAxis = 1


    for i in range(len(edges) - 1):

        thisEdge = edges[i]
        nextEdge = edges[i + 1]

        if thisEdge[0] == nextEdge[0]:
            constant = thisEdge[0]
            varriableAxis = 1
            
        elif thisEdge[1] == nextEdge[1]:
            constant = thisEdge[1]
            varriableAxis = 0

        step = 1 

        if thisEdge[varriableAxis] > nextEdge[varriableAxis]:
            step = -1

        for varriableVal in range(thisEdge[varriableAxis],nextEdge[varriableAxis], step):
            if varriableAxis == 0:
                newList.append([varriableVal, constant])
            else:
                newList.append([constant, varriableVal])

    newList.append(edges[len(edges) - 1])

    return newList


def main():  # For now, the client has no concept of its id or its color, will fix that later
    
    c_socket = socket.socket()
    try:
        c_socket.connect(SERVER)
        starting_info = pickle.loads(c_socket.recv(100))
    except Exception as e:
        raise e
        print ("Couldn't connect to server.")
        c_socket.close()
        quit()

    id = starting_info["id"]
    height = starting_info["height"]
    width = starting_info["width"]


    key = curses.KEY_RIGHT
    dir = VEC_RIGHT

    r = Renderer(height, width)

    # id = pickle.loads(c_socket.recv(100))
    while True:
        try:
            to_be_recv = c_socket.recv(1024)
            all_ids_edges = pickle.loads(to_be_recv)
        except Exception as e:
            r.destroy()
            print("YOU LOST!")
            break

        r.refresh_window()

        for id_edges in all_ids_edges:
            thisID = id_edges["id"]
            edges = id_edges["edges"]
            win = id_edges["win"]
            color = 2

            if win and thisID == id:
                r.destroy()
                print("YOU WONNNN!!!!")
                c_socket.close()
                quit()

            if thisID == id:
                color = 1

            r.draw_items(resurrect(edges))

        key = r.take_input()

        if key == curses.KEY_DOWN:
            dir = VEC_DOWN
        if key == curses.KEY_UP:
            dir = VEC_UP
        if key == curses.KEY_LEFT:
            dir = VEC_LEFT
        if key == curses.KEY_RIGHT:
            dir = VEC_RIGHT
        
        to_be_sent = pickle.dumps(dir)

        c_socket.sendall(to_be_sent)

main()




