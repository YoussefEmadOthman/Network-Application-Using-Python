import socket
import threading

class GameClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(2)
        self.player_name = None
        self.in_chat_session = False  # Track if the client is in a chat session

    def start(self):
        self.player_name = input("Enter your player name: ")
        self.send_message(f"CONNECT:{self.player_name}")

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            self.print_menu()
            choice = input("Enter your choice: ").upper()

            if choice == "1":
                self.join_session()
            elif choice == "2":
                self.leave_session()
            elif choice == "3":
                self.in_chat_session = True  # Set to True when entering chat session
                self.send_chat_message()
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def receive_messages(self):
        while True:
            try:
                data, server_address = self.client_socket.recvfrom(1024)
                message = data.decode('utf-8')

                if not self.in_chat_session:
                    print(message)
                else:
                    print("CHAT:", message)

            except socket.timeout:
                pass

    def send_message(self, message):
        self.client_socket.sendto(message.encode('utf-8'), (self.server_host, self.server_port))

    def print_menu(self):
        print("\n=== Menu ===")
        print("1. Join a session")
        print("2. Leave the current session")
        print("3. Send a chat message")
        print("4. Exit")

    def join_session(self):
        self.print_active_sessions()
        session_id = input("Enter session ID to join: ")
        self.send_message(f"JOIN:{session_id}")

    def leave_session(self):
        self.in_chat_session = False  # Reset to False when leaving the chat session
        self.send_message("LEAVE")

    def send_chat_message(self):
        message = input("Enter chat message: ")
        self.send_message(f"MESSAGE:{message}")

    def print_active_sessions(self):
        print("\n=== Active Sessions ===")
        self.send_message("LIST")
        print("=======================\n")

if __name__ == "__main__":
    client = GameClient("localhost", 12345)
    client.start()
