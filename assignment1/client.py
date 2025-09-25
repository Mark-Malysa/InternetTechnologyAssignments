import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 30069  # Using assigned port 30069
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Receive data from the server
    data_from_server=cs.recv(100)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # Read lines from input file and send to server
    try:
        with open('in-proj.txt', 'r') as file:
            for line in file:
                line = line.strip()  # Remove newline characters
                if line:  # Skip empty lines
                    print("[C]: Sending to server: {}".format(line))
                    cs.send(line.encode('utf-8'))
                    
                    # Receive processed string from server
                    processed_data = cs.recv(200)
                    processed_string = processed_data.decode('utf-8')
                    print("[C]: Processed data received from server: {}".format(processed_string))
    except FileNotFoundError:
        print("[C]: Error: in-proj.txt file not found")
    except Exception as e:
        print("[C]: Error reading file: {}".format(e))

    # close the client socket
    cs.close()
    exit()

if __name__ == "__main__":
    client()
