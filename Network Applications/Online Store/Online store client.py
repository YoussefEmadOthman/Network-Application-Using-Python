import socket

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))

        # Receive name request from server and send client's name
        name_request = client_socket.recv(1024).decode()
        client_name = input(name_request)
        client_socket.sendall(client_name.encode())

        # Receive deposit amount request from server and send client's deposit amount
        deposit_request = client_socket.recv(1024).decode()
        deposit_amount = input(deposit_request)
        client_socket.sendall(deposit_amount.encode())

        # Receive Phone number request from server and send client's phone number
        phonenumber_request = client_socket.recv(1024).decode()
        phonenum = input(phonenumber_request)
        client_socket.sendall(phonenum.encode())

        # Receive and process server responses and menu options
        while True:
            response = client_socket.recv(1024).decode()
            print("Server response:", response)

            if "Select an option" in response:
                option = input()
                client_socket.sendall(option.encode())

                # Handle user's choice
                if option == '1':
                    # Display electronic products preview
                    products_preview = client_socket.recv(1024).decode()
                    print(products_preview)

                elif option == '2':
                    # Add product to cart
                    add_message = client_socket.recv(1024).decode()
                    print(add_message)
                    product_number = input()
                    client_socket.sendall(product_number.encode())
                    add_response = client_socket.recv(1024).decode()
                    print(add_response)

                elif option == '3':
                    # Remove item from cart
                    remove_message = client_socket.recv(1024).decode()
                    print(remove_message)
                    item_number = input()
                    client_socket.sendall(item_number.encode())
                    remove_response = client_socket.recv(1024).decode()
                    print(remove_response)

                elif option == '4':
                    # Checkout
                    client_socket.sendall(option.encode())
                    checkout_response = client_socket.recv(1024).decode()
                    print(checkout_response)

                    # Extract client name from the initial interaction
                    if "Checkout successful!" in checkout_response:
                        # Get client's name (assuming the name was sent in the initial interaction)
                        message_parts = checkout_response.split('\n')
                        client_name = message_parts[0].split(' ')[-1]

                        # Display personalized thank you message
                        print(f"Thank you for shopping with us, a confirmation message is sent to your phone : {phonenum }!")

                    # Automatically disconnect after checkout
                    break  # Exit the loop and disconnect from server

            else:
                break  # Exit the loop if no more actions needed

    except ConnectionRefusedError:
        print("Error: Connection refused. Please ensure the server is running.")
    except ConnectionResetError:
        print("Connection to the server was forcibly closed.")
