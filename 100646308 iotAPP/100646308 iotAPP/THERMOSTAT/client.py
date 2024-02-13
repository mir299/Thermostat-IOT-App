import socket
from Vigenere import VigenereCipher

def main():
    # Define server address and port
    server_info = ('localhost', 12345)

    # Initialize the Vigenere Cipher with a key
    cipher = VigenereCipher("YOURKEY")
    
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect(server_info)
        print("Connected to server")

        if not login(client_socket, cipher):
            print("Login failed.")
            return

        # Infinite loop to send commands to the server
        while True:
            # Prompt user to enter a command or 'exit' to quit
            command = input("Enter command (SET_TEMP, SET_MODE, GET_STATUS) or 'exit' to quit: ")
            if command.lower() == 'exit':
                break

            # Encrypt and send the command to the server
            send_command(client_socket, cipher, command)

def login(client_socket, cipher):
    username = input("Enter username: ")
    password = input("Enter password: ")
    credentials = f"LOGIN {username} {password}"
    encrypted_credentials = cipher.encrypt(credentials)
    client_socket.sendall(encrypted_credentials.encode())

    encrypted_response = client_socket.recv(1024).decode()
    if encrypted_response:
        response = cipher.decrypt(encrypted_response)
        print("Server response: " + response)
        return response == "Login successful"
    else:
        return False

def send_command(client_socket, cipher, command):
    # Encrypt the command using Vigenere Cipher
    encrypted_message = cipher.encrypt(command)

    # Send the encrypted command to the server
    client_socket.sendall(encrypted_message.encode())

    # Receive and decrypt the server's response
    encrypted_response = client_socket.recv(1024).decode()
    if encrypted_response:
        # Decrypt the response from the server
        decrypted_response = cipher.decrypt(encrypted_response)
        print("Server response: " + decrypted_response)
    else:
        print("No response received from server.")

if __name__ == "__main__":
    # Entry point of the script
    main()

