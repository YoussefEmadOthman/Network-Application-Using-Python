import socket
import threading

class GameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sessions = {}
        self.players = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))

    def start(self):
        print(f"Server started on {self.host}:{self.port}")

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            command = input("Enter command (EXIT to stop): ")
            if command == "EXIT":
                break

    def receive_messages(self):
        while True:
            data, client_address = self.server_socket.recvfrom(1024)
            data = data.decode('utf-8')
            message = data.split(":")
            command = message[0]

            if command == "CONNECT":
                self.handle_connection(client_address, message[1])
            elif command == "JOIN":
                self.handle_join_session(client_address, message[1])
            elif command == "LEAVE":
                self.handle_leave_session(client_address)
            elif command == "MESSAGE":
                self.handle_chat_message(client_address, message[1])

    def handle_connection(self, client_address, player_name):
        self.players[client_address] = player_name
        print(f"{player_name} connected from {client_address}")

    def handle_join_session(self, client_address, session_id):
        if client_address in self.players:
            if session_id not in self.sessions:
                self.sessions[session_id] = {"players": set(), "chat": []}

            self.sessions[session_id]["players"].add(client_address)
            self.broadcast_session_info(session_id)

    def handle_leave_session(self, client_address):
        for session_id, session_data in self.sessions.items():
            if client_address in session_data["players"]:
                session_data["players"].remove(client_address)
                self.broadcast_session_info(session_id)

    def handle_chat_message(self, client_address, message):
        player_name = self.players.get(client_address, "Unknown")
        chat_message = f"{player_name}: {message}"

        for session_id, session_data in self.sessions.items():
            session_data["chat"].append(chat_message)
            self.broadcast_session_info(session_id)

    def broadcast_session_info(self, session_id):
        players = ', '.join(self.players.get(player, "Unknown") for player in self.sessions[session_id]["players"])
        chat_history = self.sessions[session_id]["chat"][-5:]  # Show the last 5 messages

        session_info = f"PLAYERS:{players}|CHAT:{'|'.join(chat_history)}"
        for player_address in self.sessions[session_id]["players"]:
            self.send_message(player_address, session_info)

    def send_message(self, client_address, message):
        self.server_socket.sendto(message.encode('utf-8'), client_address)

if __name__ == "__main__":
    server = GameServer("localhost", 12345)
    server.start()
