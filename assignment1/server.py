import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 30069)  # Using Mark Malysa's port 30069
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.  
    msg = "Welcome to CS 352!"
    csockid.send(msg.encode('utf-8'))

    # Open output file for writing
    output_file = open('out-proj.txt', 'w')
    
    # Receive data from client, process it, and send back
    while True:
        data_from_client = csockid.recv(200)  # Max 200 characters as specified
        if not data_from_client:
            break
            
        # Decode the received data
        client_string = data_from_client.decode('utf-8')
        print("[S]: Received from client: {}".format(client_string))
        
        # Reverse string and swap case
        processed_string = client_string[::-1].swapcase()
        print("[S]: Sending to client: {}".format(processed_string))
        
        # Write processed string to output file
        output_file.write(processed_string + '\n')
        output_file.flush()  # Ensure data is written immediately
        
        # Send the processed string back to client
        csockid.send(processed_string.encode('utf-8'))
    
    # Close the output file
    output_file.close()

    # Close the server socket
    ss.close()
    exit()

if __name__ == "__main__":
    server()
