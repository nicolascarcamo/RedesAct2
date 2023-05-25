
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