import socket

class SocketTCP:
    def __init__(self):
        self.address = None
        self.port = None
        self.sock = None
        
    def set_address(self, address):
        self.address = address

    def set_port(self, port):
        self.port = port

    def init_socket(self):
        if self.address is None or self.port is None:
            raise Exception("Address or port not set")
        #Create an UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind_socket(self):
        if self.sock is None:
            raise Exception("Socket not initialized")
        self.sock.bind((self.address, self.port))

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

    #Connect function will be used by the client to connect to the server
    def connect(self):
        if self.sock is None:
            raise Exception("Socket not initialized")
        self.sock.connect((self.address, self.port))
    #Info sent through TCP class will include TCP-type headers such as "ACK", "SYN", "FIN" or "SEQ"
    #We'll create "parse_segment" function to parse these headers into a data structure
    #We'll also create "create_segment" function to create a segment from a data structure

    #Parse a segment into a data structure
    #Segment is a string which contains the header, the sequence number and the data
    #Headers are signaled through binary numbers
    #These is an example of how headers will be included 
    #[SYN]|||[ACK]|||[FIN]|||[SEQ]|||[DATA]
    #Where 1 signals the header is included and 0 signals the header is not included
    #For example, if we want to send a segment with SYN and SEQ headers, we'll have to send a segment like this:
    #1|||0|||0|||0|||001|||Hello
    #Where 1|||0|||0|||001|||Hello is the segment
    #1 is the SYN header
    #0 is the ACK header
    #0 is the FIN header
    #001 is the sequence number
    #Hello is the data
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
    
    #iterate_seq function will iterate the sequence number
    #The sequence number will be a string of 3 digits
    #The sequence should start at 001 and end at 100
    #Create a function that receives a sequence number and returns the next sequence number
    def iterate_seq(self, seq):
        #Convert the sequence number to an integer
        seq = int(seq)
        #Add 1 to the sequence number
        seq += 1
        #Convert the sequence number to a string
        seq = str(seq)
        #Add zeros to the sequence number until it has 3 digits
        while len(seq) < 3:
            seq = "0" + seq
        #Return the sequence number
        return seq

    #La idea es que el cliente envie un mensaje al servidor, donde la primera parte del mensaje sea el header, la segunda parte sea el numero de secuencia y la tercera parte sea el mensaje
    #El servidor recibe el mensaje y lo imprime en pantalla
    #Para hacer esto, tenemos que añadirle a cada mensaje sus headers respectivos, y utilizar parse y create segment para enviar y recibir los mensajes
    #El cliente envia un mensaje con el header "SYN", el numero de secuencia "000" y el mensaje "Hello"
    #El servidor recibe el mensaje y lo imprime en pantalla
    #El servidor envia un mensaje con el header "ACK", el numero de secuencia "001" y el mensaje "Hello"
    #El cliente recibe el mensaje y lo imprime en pantalla
