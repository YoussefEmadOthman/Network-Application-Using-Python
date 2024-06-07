import socket
import threading
import datetime

def handle_client(client_socket, client_address):
    print('Accepted connection from', client_address)

    # Specify the file path to be transferred
    file_path = r'C:\Users\CPMPUMARTS\Desktop\Happy Face.jpg'  # Replace with your file path

    # Log client information
    log_entry = f"At {datetime.datetime.now()} - Client {client_address} downloaded file: {file_path}\n"
    with open('server_log.txt', 'a') as log_file:
        log_file.write(log_entry)

    # Open the specified file for reading
    with open(file_path, 'rb') as file:
        # Send file name and size to the client
        client_socket.send(file_path.encode())
        file_size = len(file.read())
        client_socket.send(str(file_size).encode())

        # Move the file cursor back to the beginning of the file
        file.seek(0)

        # Send file data in chunks
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    print(f'File sent successfully to {client_address}.')

    # Close the client socket
    client_socket.close()

def server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('localhost', 12344))

    # Listen for incoming connections
    server_socket.listen(5)  # Allow up to 5 queued connections

    print('Server listening on port 12344...')

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

        # Check for user input to close the server
        user_input = input("Type 'yes' to close the server: ")
        if user_input.lower() == 'yes':
            print('Closing the server...')
            # Close the server socket
            server_socket.close()
            break

# Run the server
server()
