#!/usr/bin/python
# TCP client example
import socket,os,pickle
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5005))
k = ' '
size = 1024

while(1):
    print("Do you want to transfer a \n1.Text File\n2.Image\n3.Video\n")
    k = input()
    client_socket.send(pickle.dumps(k))
    k = int (k)
    if(k == 1):
        print("Enter file name\n")
        strng = input()
        client_socket.send(strng)
        size = client_socket.recv(1024)
        size = int(size)
        print("The file size is - ",size," bytes")
        size = size*2
        strng = client_socket.recv(size)
        print("\nThe contents of that file - ")
        print(strng)

    if (k==2 or k==3):
        print("Enter file name of the image with extentsion (example: filename.jpg,filename.png or if a video file then filename.mpg etc) - ")
        fname = input()
        client_socket.send(pickle.dumps(fname))
        fname = fname
        fp = open(fname,'w')
        while True:
            strng = client_socket.recv(512)
            if not strng:
                break
            fp.write(strng)
        fp.close()
        print("Data Received successfully")
        exit()
        #data = 'viewnior '+fname
        #os.system(data)