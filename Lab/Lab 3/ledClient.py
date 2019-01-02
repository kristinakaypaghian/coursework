# LED Client
#
# This code runs on your VM and sends requests to the Raspberry Pi to turn on 
# and off the Grove LED using TCP packets.

import socket

def Main():
    host = '192.168.1.83' # destination: Pi IP address
    port = 5001 # destination: should match the Pi port

    s = socket.socket()
    s.connect((host,port))

    while True:
        message = input("light status-> ")
        if message == 'q':
            break
        elif message != 'q':
            s.send(message.encode('utf-8'))
        
            data= s.recv(1024).decode('utf-8')
            if not data:
                    break
            print(data)
    s.close()



if __name__ == '__main__':
    Main()