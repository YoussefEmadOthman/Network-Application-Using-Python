import socket
import time

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(("127.0.0.1", 8888))

# Prompt the client to enter their name
name_prompt = client_socket.recv(1024).decode()
client_name = input(name_prompt)

# Send the client's name to the server
client_socket.send(client_name.encode())

# Receive and print the welcome message and quiz start message
welcome_message = client_socket.recv(1024).decode()
print(welcome_message)

# Initialize score
score = 0

# Set the overall quiz timer duration on the client side (in seconds)
overall_timer_duration = 60

# Start the overall timer on the client side
start_time = time.time()

# Loop to receive and answer quiz questions
while True:
    # Receive and print the question
    question = client_socket.recv(1024).decode()
    if "Quiz complete" in question or "Time's up" in question:
        print(question)
        break  # Exit the loop when the quiz is complete or time is up
    print(question)

    # Get the user's answer within the specified time
    try:
        answer = input(f"Your answer (within {overall_timer_duration} seconds): ")
    except EOFError:
        answer = ""

    # Stop the timer for the current question
    elapsed_time = time.time() - start_time

    # Send the answer to the server
    client_socket.send(answer.encode())

    # Receive and print the server's response
    response = client_socket.recv(1024).decode()
    
    # Check if the response indicates a correct answer
    if "Correct" in response:
        # Check if the answer was entered after the time limit
        if "won't be taken into consideration" in response:
            print(response)
        else:
            score += 1
    else:
        print(response)

    # Print the time taken for the current question
    print(f"Time taken for this question: {elapsed_time:.2f} seconds\n")

# Stop the overall timer on the client side
overall_elapsed_time = time.time() - start_time

# Print the final score
final_score_message = client_socket.recv(1024).decode()
print(final_score_message)

# Print the overall time taken for the entire quiz
print(f"Overall time taken for the entire quiz: {overall_elapsed_time:.2f} seconds")

# Close the client socket
client_socket.close()
