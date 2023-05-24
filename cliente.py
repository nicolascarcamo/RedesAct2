import socket
import sys 
import tcp_class

HEADER_SIZE = 18
BYTES_TO_RECEIVE = 16
TOTAL_BYTES = HEADER_SIZE + BYTES_TO_RECEIVE

SERVER_ADDRESS = ('localhost', 8000)
NEW_SERVER_ADDRESS = (sys.argv[1], int(sys.argv[2]))

#Create a client that communicates through an UDP socket with "server.py" file in the same directory
#Client will recieve an adress, port as its first two arguments and a file through standard input
#Client will send the file to the server in chunks of 16 bytes
#The server will receive the file and print it to standard output

#Create a TCP object
tcp = tcp_class.SocketTCP()

#Set the address and port
tcp.set_address(sys.argv[1])
tcp.set_port(sys.argv[2])

#Initialize the socket
tcp.init_socket()

#Use connect function to connect to the server using the address and port
#Connect function will start the three-way handshake
new_address = tcp.connect(SERVER_ADDRESS)
print("Connected to server at " + str(new_address))

#Send the file to the server in chunks of 16 bytes, until the file is empty
#The client will wait for an ACK from the server before sending the next chunk
#If the client doesn't receive an ACK, it will resend the chunk
#If the client doesn't receive an ACK after 3 tries, it will close the socket
#If the client receives an empty message, it will close the socket
try:
    #Open the file received from standard input using stdin
    file = sys.stdin
    #Read the file
    file_data = file.read(16)
    #Send the file
    while file_data:

        #Create a segment with SYN and SEQ headers with the sequence number of the chunk using the "create_segment" function
        #SEQ format is "001" for the first chunk, "002" for the second, etc.
        segment = tcp.create_segment([1, 0, 0], tcp.seq, file_data)
        
        #Send the segment to the server
        tcp.sock.sendto(segment.encode(), NEW_SERVER_ADDRESS)
        print('sent {} bytes to {}'.format(len(segment), (tcp.address, tcp.port)))

        #Parse server response and get check if it is an ACK
        server_data, address = tcp.recieve(HEADER_SIZE)
        print('+')
        header, seq, text_data = tcp.parse_segment(server_data.decode())
        if header[1] == "1":
            print("ACK")
        else:
            print("NACK")
        #If the server response is not an ACK, resend the segment
        #If the server response is an ACK, read the next chunk
        #If the client doesn't receive an ACK after 3 tries, it will close the socket
        tries = 1
        while header[1] != "1":
            if tries == 3:
                print("Closing socket")
                tcp.close_socket()
                break
            tcp.sock.sendto(segment.encode(), NEW_SERVER_ADDRESS)
            print('sent {} bytes to {}'.format(len(segment), (tcp.address, tcp.port)))
            server_data, address = tcp.receive(HEADER_SIZE)
            header, seq, text_data = tcp.parse_segment(server_data.decode())
            if header[1] == "1":
                print("ACK")
            else:
                print("NACK")
            tries += 1
        
        #Read the next chunk
        file_data = file.read(16)

        #Iterate the sequence number
        tcp.seq 
finally:
    #Close the file
    file.close()

    #Close the socket
    print('closing socket')
    tcp.close_socket()