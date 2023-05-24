import random
import socket

HEADER_SIZE = 18
NEW_SERVER_ADDRESS = ('localhost', 8001)

class SocketTCP:
    def __init__(self):
        self.address = None
        self.port = None
        self.sock = None
        self.seq = "000"
        
    def set_address(self, address):
        self.address = address

    def set_port(self, port):
        self.port = port

    def init_socket(self):
        if self.address is None or self.port is None:
            raise Exception("Address or port not set")
        #Create an UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #bind_socket function will be used by the server to bind the socket to the given address
    def bind_socket(self, address=None):
        if self.sock is None:
            raise Exception("Socket not initialized")
        if address is None:
            address = (self.address, self.port)
        self.sock.bind(address)

    def listen_socket(self):
        if self.sock is None:
            raise Exception("Socket not initialized")
        self.sock.listen(1)

    def close_socket(self):
        if self.sock is None:
            raise Exception("Socket not initialized")
        self.sock.close()

    def recieve(self, bytes_to_receive):
        if self.sock is None:
            raise Exception("Socket not initialized")
        return self.sock.recvfrom(bytes_to_receive)
    
    def send_to(self, address, message):
        if self.sock is None:
            raise Exception("Socket not initialized")
        self.sock.sendto(message.encode(), address)

    #Connect function will be used by the client to connect to the server to implement the three-way handshake
    #The client will send a SYN segment to the server
    #The server will respond with a SYN-ACK segment
    #The client will respond with an ACK segment
    def connect(self, address):
        print("Connecting to server using three-way handshake")
        #Generate a random sequence number between 0    and 100, using string format to pad the number with zeros
        self.seq = "{:03d}".format(random.randint(0, 100))
        #Create a segment with SYN header and the sequence number
        segment = self.create_segment([1, 0, 0], self.seq, "")
        #Send the segment to the server
        self.send_to(address, segment)
        #Wait for a response from the server (SYN-ACK segment), with HEADER_SIZE bytes, since the segment will not contain any data
        whole_data, response_address = self.recieve(HEADER_SIZE)
        #Parse the segment
        header, server_seq, data = self.parse_segment(whole_data.decode())
        #If the segment is a SYN-ACK segment, and check if the sequence number is one more than the client sequence number
        if header[0] == "1" and header[1] == "1" and header[2] == "0" and server_seq == "{:03d}".format(int(self.seq) + 1):
            print("Received SYN-ACK segment from server")
            #Increment the sequence number by 1
            self.seq = "{:03d}".format(int(server_seq) + 1)
            #Create a segment with ACK header and the sequence number
            segment = self.create_segment([0, 1, 0], self.seq, "")
            #Send the segment to the server
            self.send_to(response_address, segment)
            #Return address
            return response_address
        else:
            raise Exception("Connection failed")
    #accept function will be used by the server to accept a connection from the client
    #The server will wait for a SYN segment from the client
    #The server will respond with a SYN-ACK segment
    #The client will respond with an ACK segment
    def accept(self):
        #Wait for a SYN segment from the client, with HEADER_SIZE bytes, since the segment will not contain any data
        whole_data, client_address = self.recieve(HEADER_SIZE)
        #Parse the segment
        header, client_seq, data = self.parse_segment(whole_data.decode())
        #Update the sequence number
        self.seq = client_seq
        #If the segment is a SYN segment, send a SYN-ACK segment
        if header[0] == "1" and header[1] == "0" and header[2] == "0":
            print("Accepting connection from client")
            #Increment the sequence number by 1
            self.seq = "{:03d}".format(int(client_seq) + 1)
            #Create a segment with SYN-ACK header and the sequence number
            segment = self.create_segment([1, 1, 0], self.seq, "")
            #Create a new TCP object to communicate with the client
            new_tcp = SocketTCP()
            #Set the address and port of the new TCP object using SERVER_ADDRESS
            new_tcp.set_address(NEW_SERVER_ADDRESS[0])
            new_tcp.set_port(NEW_SERVER_ADDRESS[1])
            new_tcp.seq = self.seq
            new_tcp.init_socket()
            #Bind the socket to the client address
            new_tcp.bind_socket(NEW_SERVER_ADDRESS)
            #Send the segment to the client
            new_tcp.send_to(client_address, segment)
            #Wait for a response from the client (ACK segment)
            whole_data, new_address = new_tcp.recieve(HEADER_SIZE)
            #Parse the segment
            last_header, new_client_seq, data = self.parse_segment(whole_data.decode())
            #If the segment is an ACK segment, and check if the sequence number is one more than the server sequence number
            #If the sequence number is correct, return the TCP object
            if last_header[0] == "0" and last_header[1] == "1" and last_header[2] == "0" and new_client_seq == "{:03d}".format(int(self.seq) + 1):
                print("ACK segment received from client")
                #Update the sequence number 
                new_tcp.seq = new_client_seq
                return new_tcp, (new_tcp.address, new_tcp.port)
            else:
                raise Exception("Connection failed at last step")
        else:
            raise Exception("Connection failed")
            
    '''
    Resume what we've done so far:
    - We've created a SocketTCP class which will be used to communicate through TCP
    - We've created a connect function which will be used by the client to connect to the server to implement the three-way handshake
    - We've created an accept function which will be used by the server to accept a connection from the client
    - We've created a send_to function which will be used to send data to a given address
    - We've created a recieve function which will be used to recieve data from a given address
    - We've created a bind_socket function which will be used to bind the socket to a given address
    - We've created a listen_socket function which will be used to listen for connections
    - We've created a close_socket function which will be used to close the socket
    - We've created a set_address function which will be used to set the address
    - We've created a set_port function which will be used to set the port
    - We've created a init_socket function which will be used to initialize the socket
    - We've created a parse_segment function which will be used to parse a segment into a data structure
    - We've created a create_segment function which will be used to create a segment from a data structure

    We still need to test the code to see if it works

    Next up, we'll implement Stop-and-Wait ARQ using a timeout mechanism, using settimeout and setblocking functions

    '''       

    #Info sent through TCP class will include TCP-type headers such as "ACK", "SYN", "FIN" or "SEQ"
    #We'll create "parse_segment" function to parse these headers into a data structure
    #We'll also create "create_segment" function to create a segment from a data structure

    #Parse a segment into a data structure

    def parse_segment(self, segment):
        #Get the header
        split_segment = segment.split("|||")
        header = split_segment[0:3]
        #Get the sequence number
        seq = split_segment[3]
        #Get the data
        data = split_segment[4]
        #Return the data structure
        return header, seq, data



    #Create a segment from a data structure
    def create_segment(self, header, seq, data):
        #Create the segment
        #The segment will be a string which contains the header, the sequence number and the data
        #Headers are signaled through binary numbers
        #These is an example of how the function will be used
        #create_segment([1, 0, 0], "001", "Hello")

        #Create the segment
        segment = ""
        #Add the header
        for i in header:
            segment += str(i) + "|||"
        #Add the sequence number
        segment += seq + "|||"
        #Add the data
        segment += data

        #Return the segment
        return segment
