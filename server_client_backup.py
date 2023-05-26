
#Create a TCP object to establish a connection with the client
initial_tcp = SocketTCP.SocketTCP()

#Bind the socket
initial_tcp.bind(FULL_ADDRESS)

print('starting up on {} port {}'.format(initial_tcp.address, initial_tcp.port))

#Use the accept function to accept a connection from the client from the three-way handshake
tcp, new_address = initial_tcp.accept()
print('accepted connection and listening at {} port {}'.format(new_address[0], new_address[1]))


#Receive the file from the client using recv function
message_received = tcp.recv(TOTAL_BYTES)
print("Message received: " + str(message_received))



##############################

#Create a TCP object
tcp = SocketTCP.SocketTCP()

#Set the address and port
tcp.set_address(sys.argv[1])
tcp.set_port(sys.argv[2])

#Use connect function to connect to the server using the address and port
#Connect function will start the three-way handshake
new_address = tcp.connect(SERVER_ADDRESS)
print("Connected to server at " + str(new_address))

#open the file received from standard input using stdin
file = sys.stdin
#Read the whole file
file_data = file.read(4096)
#Send the file to the server using send function
tcp.send(file_data)

#############################

        #Begin timeout
        self.sock.settimeout(5)
        #Since we'll call recv function multiple times, we'll use an if statement to check if the message has been fully received
        try:
            if len(self.whole_message) < self.message_size:
                #Receive a segment from the sender
                whole_data, client_address = self.recieve(HEADER_SIZE + 16)
                #Parse the segment
                header, seq, data = self.parse_segment(whole_data.decode())

                print("Data segment received from server")

                #Check if the segment is a data segment and if the sequence number is one more than the previous sequence number
                if header[0] == "0" and header[1] == "0" and header[2] == "0" and seq == "{:03d}".format(int(self.seq) + 1):
                    #If we have data in the auxillary variable, it means that we have received more data than the size of the message
                    #So we'll append the data to the auxillary variable

                    self.whole_message += data

                    if self.aux_message != "":
                        self.aux_message += data
                        if len(self.aux_message) > size:
                            self.message = self.aux_message[:self.message_size]
                            self.aux_message = self.aux_message[self.message_size:]
                    #If we don't have data in the auxillary variable, it means that we have received less data than the size of the message
                    #So we'll append the data to the message
                    else:
                        #Append the data to the message
                        self.message = data[:size]
                        if(len(data) > size):
                            self.aux_message = data[size:]
                    #Send an ACK segment to the sender
                    #Increment the sequence number by 1
                    self.seq = "{:03d}".format(int(seq) + 1)
                    #Create an ACK segment
                    ack_segment = self.create_segment([0, 1, 0], self.seq, "")
                    #Send the ACK segment to the sender
                    self.send_to(client_address, ack_segment)
                #elif we already have the whole message

        except socket.timeout:
            print("Timeout occured, resending ACK segment")
            #Send an ACK segment to the sender
            #Create an ACK segment
            ack_segment = self.create_segment([0, 1, 0], self.seq, "")
            #Send the ACK segment to the sender
            self.send_to(client_address, ack_segment)
        #End timeout
        self.sock.settimeout(None)
        #Return the message
        return self.message

#############################
    def recv(self, size):

        print("recv starting with variables: ", self.message_length, self.message, self.whole_message, self.aux_message)
        #If self.message_length is 0, then we'll receive the size of the message
        if self.message_length == 0:
            #Receive the size of the message from the sender
            #No timeout is needed here
            whole_data, client_address = self.recieve(HEADER_SIZE + 16)
            #Parse the segment
            print("whole_data: ", whole_data)
            print("client_address: ", client_address)
            header, seq, data = self.parse_segment(whole_data.decode())
            print("message size: ", data)
            #Get the size of the message 
            self.message_length = int(data)
            self.message = ""
            self.whole_message = ""
            #Since we're recieving 16 bytes of data, but we can only send back size of message, we'll create an auxillary variable to store the rest of the data
            self.aux_message = ""
            #Send an ACK segment to the sender
            #Increment the sequence number by 1
            self.seq = "{:03d}".format(int(seq) + 1)
            #Create an ACK segment
            ack_segment = self.create_segment([0, 1, 0], self.seq, "")
            #Send the ACK segment to the sender
            self.send_to(client_address, ack_segment)
        #Receive the message from the sender
        #If we haven't received the whole message, we'll receive the message
        print("self.message_length: ", self.message_length)

        #We'll use a while loop to receive the message in case size is bigger than len(message)
        if len(self.whole_message) < self.message_length:
            #Receive the message from the sender
            #Begin timeout
            print("begin if!")
            self.sock.settimeout(5)
            try:
                #Receive a segment from the sender
                whole_data, client_address = self.recieve(HEADER_SIZE + 16)
                #Parse the segment
                header, seq, data = self.parse_segment(whole_data.decode())
                print("data: ", data)
                #Check if the segment is a data segment and if the sequence number is correct
                if header[0] == "0" and header[1] == "0" and header[2] == "0" and seq == "{:03d}".format(int(self.seq) + 1):
                    print("begin second if!")
                    self.whole_message += data
                    #Now check if we have leftovers from the previous segment
                    if len(self.aux_message) > 0:
                        #If we do, then we'll add the data from the current segment to the leftovers
                        self.aux_message += data
                        #Then we'll add the leftovers to the message
                        #If the length of the message is greater than the size, then we'll add the first size bytes of the message to the message
                        if len(self.aux_message) > size:
                            self.message = self.aux_message[:size]
                            self.aux_message = self.aux_message[size:]
                        else:
                            self.message += self.aux_message
                            self.aux_message = ""
                    else:
                        #If we don't have leftovers from the previous segment, then we'll check if the length of the message is greater than the size
                        #If it is, then we'll add the first size bytes of the message to the message
                        if len(data) > size:
                            self.message = data[:size]
                            self.aux_message = data[size:]
                        else:
                            self.message = data
                            print("we are heeeeere")
                            print("whole_message: ", self.whole_message)
                    #Increment the sequence number by 1
                    self.seq = "{:03d}".format(int(seq) + 1)
                    #Create an ACK segment
                    ack_segment = self.create_segment([0, 1, 0], self.seq, "")
                    #Send the ACK segment to the sender
                    self.send_to(client_address, ack_segment)
                else:
                    raise Exception("Connection failed")
            except socket.timeout:
                print("Timeout occured, resending segment")
        else:
            #If we have received the whole message, we'll check if we have leftovers from the previous segment
            if len(self.aux_message) > 0:
                #If we do, then we'll add the leftovers to the message
                #If the length of the message is greater than the size, then we'll add the first size bytes of the message to the message
                if len(self.aux_message) > size:
                    self.message = self.aux_message[:size]
                    self.aux_message = self.aux_message[size:]
                else:
                    self.message += self.aux_message
                    self.aux_message = ""


        #End timeout
        self.sock.settimeout(None)

        print("self.whole_message: ", self.whole_message, "self.aux_message: ", self.aux_message)
        #If we have received the whole message, and we have no leftovers from the previous segment, then we'll reset the message_length variable
        if len(self.whole_message) == self.message_length and len(self.aux_message) == 0:
            print("we are here again")
            self.message_length = 0
            self.whole_message = ""
        #Return the message
        return self.message