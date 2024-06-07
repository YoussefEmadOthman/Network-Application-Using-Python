import socket
import threading
import os

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

# Define a dictionary to store cart items for each client
client_carts = {}
# Define a dictionary to store deposit amounts for each client
client_balances = {}
# Define a dictionary to store phone numbers for each client
client_phonenumbers = {}

# Electronic products data 
electronic_products = [
    {"name": "Laptop", "price": 1200},
    {"name": "Smartphone", "price": 800},
    {"name": "Tablet", "price": 400},
    {"name": "Headphones", "price": 150},
    {"name": "Smartwatch", "price": 300}
]

# Function to handle each client connection
def handle_client(client_socket, client_address):
    try:
        # Ask client for name
        client_socket.sendall("Enter your name: ".encode())
        client_name = client_socket.recv(1024).decode().strip()

        # Ask client for deposit amount
        client_socket.sendall("Enter deposit amount: ".encode())
        deposit_amount = float(client_socket.recv(1024).decode().strip())
        client_balances[client_name] = deposit_amount  # Store deposit amount for the client

        # Ask client for phone number
        client_socket.sendall("Please enter your phone number: ".encode())
        phonenum = client_socket.recv(1024).decode().strip()
        client_phonenumbers[client_name] = phonenum  # Store phone number for the client

        # Initialize an empty cart for the client
        client_carts[client_name] = []

        while True:
            # Show menu options to the client
            menu_message = (
                "Select an option:\n"
                "1. Preview Products\n"
                "2. Add to Cart\n"
                "3. Remove from Cart\n"
                "4. Checkout\n"
                "Enter option number (1-4): "
            )
            client_socket.sendall(menu_message.encode())

            # Receive client's choice
            choice = client_socket.recv(1024).decode().strip()

            if not choice:
                # Client disconnected unexpectedly
                print(f"Client {client_name} disconnected unexpectedly.")
                break

            if choice == '1':
                # Preview electronic products
                preview_message = "Available electronic products:\n"
                for index, product in enumerate(electronic_products, start=1):
                    preview_message += f"{index}. {product['name']} - ${product['price']}\n"

                client_socket.sendall(preview_message.encode())

            elif choice == '2':
                # Add item to cart
                if electronic_products:
                    add_message = "Select a product to add (enter product number): "
                    client_socket.sendall(add_message.encode())
                    product_index = int(client_socket.recv(1024).decode().strip())

                    if 1 <= product_index <= len(electronic_products):
                        selected_product = electronic_products[product_index - 1]
                        client_carts[client_name].append(selected_product)
                        client_socket.sendall(f"Item '{selected_product['name']}' added to cart.".encode())
                    else:
                        client_socket.sendall("Invalid product number. Please try again.".encode())
                else:
                    client_socket.sendall("No products available to add.".encode())

            elif choice == '3':
                # Remove item from cart
                if client_carts[client_name]:
                    # Display cart contents first
                    cart_contents_message = "Your cart contains:\n"
                    for index, item in enumerate(client_carts[client_name], start=1):
                        cart_contents_message += f"{index}. {item['name']} - ${item['price']}\n"
                    client_socket.sendall(cart_contents_message.encode())

                    # Prompt user to enter item number to remove
                   

                    # Receive item number to remove
                    item_index = int(client_socket.recv(1024).decode().strip())

                    if 1 <= item_index <= len(client_carts[client_name]):
                        removed_item = client_carts[client_name].pop(item_index - 1)
                        client_socket.sendall(f"Item '{removed_item['name']}' removed from cart.".encode())
                    else:
                        client_socket.sendall("Invalid item number. Please try again.".encode())
                else:
                    client_socket.sendall("Your cart is empty.".encode())

            elif choice == '4':
                # Checkout
                if client_carts[client_name]:
                    # Calculate total cost of items in the cart
                    total_cost = sum(item['price'] for item in client_carts[client_name])

                    # Check if the client's balance is sufficient
                    if total_cost <= client_balances[client_name]:
                        # Reduce client's balance by total cost
                        client_balances[client_name] -= total_cost

                        # Calculate remaining balance
                        remaining_balance = client_balances[client_name]

                        cart_contents = "\n".join([f"{item['name']} - ${item['price']}" for item in client_carts[client_name]])
                        checkout_message = f"Checkout successful!\nItems purchased:\n{cart_contents}\nRemaining balance: ${remaining_balance:.2f}"

                        # Log successful checkout to a file
                        log_data = f"Client: {client_name}\nItems Purchased:\n{cart_contents}\nRemaining Balance: ${remaining_balance:.2f}\n"
                        log_file_path = r"C:\Users\CPMPUMARTS\Desktop\Testinnng\checkout_logs.txt"

                        with open(log_file_path, "a") as log_file:
                            log_file.write(log_data)

                        # Send checkout success message to client
                        client_socket.sendall(checkout_message.encode())

                    else:
                        client_socket.sendall("Insufficient funds. Please add more deposit or remove items from your cart.".encode())
                else:
                    client_socket.sendall("Your cart is empty. Nothing to checkout.".encode())

    except ValueError:
        error_message = "Invalid input. Please try again."
        client_socket.sendall(error_message.encode())

    except ConnectionResetError:
        # Handle connection reset gracefully (no server-side output)
        pass

    finally:
        # Close the client socket
        client_socket.close()
        print(f"Connection closed with client at {client_address}")

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}...")

try:
    while True:
        # Accept connections from clients
        client_socket, client_address = server_socket.accept()
        print(f"Connected to client at {client_address}")

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

except KeyboardInterrupt:
    print("Server interrupted. Closing...")
finally:
    # Close the server socket upon termination
    server_socket.close()
