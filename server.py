import socket

ADDRESS = 'localhost'
PORT = 8000

#Create an UDP socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Bind the socket to the port
server_address = (ADDRESS, PORT)

print('starting up on {} port {}'.format(*server_address))

sock.bind(server_address)

#Client will send a file to the server in chunks of 16 bytes
#The server will receive the file and print it to standard output
while True:
    print('waiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(len(data), address))
    print(data.decode())

    if data:
        #Acknowledge the client
        ackn = 'ACK'
        sent = sock.sendto(ackn.encode(), address)
        print('sent {} bytes back to {}'.format(sent, address))
    
    #If the client sends an empty message, the server will close the socket
    if not data:
        print('closing socket')
        sock.close()
        break