import socket
import tcp_class

HEADER_SIZE = 18
BYTES_TO_RECEIVE = 16
TOTAL_BYTES = HEADER_SIZE + BYTES_TO_RECEIVE
ADDRESS = 'localhost'
PORT = 8009

#Create a TCP object
tcp = tcp_class.SocketTCP()

#Set the address and port
tcp.set_address(ADDRESS)
tcp.set_port(PORT)

#Initialize the socket
tcp.init_socket()

#Bind the socket
tcp.bind_socket()


#Client will send a file to the server in chunks of 16 bytes
#The server will receive the file and print it to standard output
while True:

    #Wait for a connection
    print('waiting for packet...')

    #Receive data from the client
    whole_data, address = tcp.recieve(TOTAL_BYTES)

    #Parse the segment
    header, seq, data = tcp.parse_segment(whole_data.decode())
    print(header, seq, data)
    print('------------------')
    if data:
        print('received {} bytes from {}'.format(len(whole_data), (tcp.address, tcp.port)))
        #Create a segment with ACK header with the sequence number of the received segment using the "create_segment" function
        segment = tcp.create_segment([0, 1, 0], seq, "")

        #Acknowledge the client
        tcp.sock.sendto(segment.encode(), address)
        print('sent {} bytes back to {}'.format(len(segment), ADDRESS))
        
    
    #If the client sends an empty message, the server will close the socket
    if not data:
        print('closing socket')
        tcp.close_socket()
        break