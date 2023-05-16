import socket
import sys 

#Create a client that communicates through an UDP socket with "server.py" file in the same directory
#Client will recieve an adress, port as its first two arguments and a file through standard input
#Client will send the file to the server in chunks of 16 bytes
#The server will receive the file and print it to standard output

#Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Get the server address and port from the command line
server_address = (sys.argv[1], int(sys.argv[2]))

#Send the file to the server in chunks of 16 bytes, until the file is empty
#The client will wait for an ACK from the server before sending the next chunk
#If the client doesn't receive an ACK, it will resend the chunk
#If the client doesn't receive an ACK after 3 tries, it will close the socket
#If the client receives an empty message, it will close the socket
try:
    #Open the file received from standard input using stdin
    file = sys.stdin
    #Read the file
    data = file.read(16)
    #Send the file
    while data:
        #Send the data
        sent = sock.sendto(data.encode(), server_address)
        print('sent {} bytes to {}'.format(sent, server_address))
        #Wait for an ACK
        ackn, address = sock.recvfrom(4096)
        print('received {} bytes from {}'.format(len(ackn), address))
        print(ackn.decode())
        #If the ACK is empty, close the socket
        if not ackn:
            print('closing socket')
            sock.close()
            break
        #If the ACK is not empty, read the next chunk
        data = file.read(16)
    #Close the file
    file.close()
finally:
    print('closing socket')
    sock.close()