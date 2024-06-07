import socket
import threading
import time
import os

# Define the file path to save client scores
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
scores_file_path = os.path.join(desktop_path, "client_scores.txt")

# Quiz questions and answers
quiz_data = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Which planet is known as the Red Planet?", "answer": "Mars"},
    {"question": "What is the capital city of Japan?", "answer": "Tokyo"},
    {"question": "Who is known as the father of modern physics?", "answer": "Albert Einstein"},
    {"question": "In which year did the Titanic sink?", "answer": "1912"},
]

# Function to handle each connected client
def handle_client(client_socket):
    # Prompt the client to enter their name
    client_socket.send("Please enter your name: ".encode())
    client_name = client_socket.recv(1024).decode().strip()
    welcome_message = f"Welcome, {client_name}, to the Online General Information Quiz Game!\n"
    client_socket.send(welcome_message.encode())

    # Send quiz start message
    client_socket.send("You have 60 seconds to answer all the questions.\n".encode())

    # Initialize score
    score = 0

    # Set the overall quiz timer duration (in seconds)
    overall_timer_duration = 60

    # Start the overall timer for the entire quiz
    start_time = time.time()

    # Loop through quiz questions
    for idx, question_data in enumerate(quiz_data, start=1):
        question = question_data["question"]
        answer = question_data["answer"]

        # Send the question to the client
        client_socket.send(f"Question {idx}: {question}\n".encode())

        # Receive the client's answer
        client_answer = ""
        while time.time() - start_time < overall_timer_duration:
            try:
                client_answer = client_socket.recv(1024).decode().strip()
                if client_answer:
                    break
            except socket.error as e:
                pass  # Ignore socket errors during the wait

        # Check if the time is up
        if time.time() - start_time >= overall_timer_duration:
            response = "Time's up! Your answer won't be taken into consideration.\n"
        elif client_answer.lower() == answer.lower():
            response = f"Correct! Time taken: {time.time() - start_time:.2f} seconds\n"
            score += 1  # Increment the score for each correct answer
        else:
            response = f"Wrong! The correct answer is {answer}\n"

        # Send the response to the client
        client_socket.send(response.encode())

    # Stop the overall timer for the entire quiz
    overall_elapsed_time = time.time() - start_time

    # Save the client's name and score to a file
    with open(scores_file_path, "a") as scores_file:
        scores_file.write(f"{client_name} scored {score}/{len(quiz_data)}\n")

    # Send the final score to the client along with the total number of questions
    final_score_message = f"Quiz complete, {client_name}. Your final score is {score}/{len(quiz_data)}\n"
    client_socket.send(final_score_message.encode())

    # Send the overall time taken for the entire quiz
    time_up_message = f"Overall time taken for the entire quiz: {overall_elapsed_time:.2f} seconds\n"
    client_socket.send(time_up_message.encode())

    # Close the client socket
    client_socket.close()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind(("127.0.0.1", 8888))

# Listen for incoming connections (max 5 connections)
server_socket.listen(5)
print("Server listening on port 8888")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
