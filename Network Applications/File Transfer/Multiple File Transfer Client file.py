import socket
import datetime

def client():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(('localhost', 12344))

    # Receive file path and size from the server
    file_name = client_socket.recv(1024).decode()
    file_size = int(client_socket.recv(1024).decode())
    print(f"Receiving file: {file_name}, Size: {file_size} bytes")

    # Specify the destination path to save the received file
    destination_path = r'C:\Users\CPMPUMARTS\Downloads\received_file.jpg'  # Replace with your file path

    # Log client information
    log_entry = f"At {datetime.datetime.now()} - Downloaded file: {file_name} from server {client_socket.getpeername()}\n"
    with open('client_log.txt', 'a') as log_file:
        log_file.write(log_entry)

    # Open a new file for writing in the specified destination path
    with open(destination_path, 'wb') as file:
        # Receive and write file data in chunks
        data = client_socket.recv(1024)
        while data:
            file.write(data)
            data = client_socket.recv(1024)

    print('File received successfully and saved at:', destination_path)

    # Close the socket
    client_socket.close()

# Run the client
client()
