import socket
import threading
from Vigenere import VigenereCipher
from Thermostat import SmartThermostat

# Initialization of global objects for the thermostat and the cipher.
thermostat = SmartThermostat()
cipher = VigenereCipher("YOURKEY")  # Replace 'YOURKEY' with your actual key

users = {
    "user1": "password1",
    "user2": "password2",
}

def handle_client(conn, address):
    """
    Handles incoming client connections. Each client connection is managed in a separate thread.
    Args:
        conn: The socket object for the client.
        address: The address of the client.
    """
    print(f"New connection from {address[0]}:{address[1]}", flush=True)
    with conn:
        # Handle login
        encrypted_data = conn.recv(1024).decode()
        decrypted_data = cipher.decrypt(encrypted_data)
        if not decrypted_data.startswith("LOGIN") or not validate_login(decrypted_data):
            conn.sendall(cipher.encrypt("Login failed").encode())
            return

        conn.sendall(cipher.encrypt("Login successful").encode())
        while True:
            try:
                # Receiving encrypted data from client
                encrypted_data = conn.recv(1024).decode()
                if not encrypted_data:
                    break

                # Print the received encrypted command for debugging
                print(f"Received encrypted command: {encrypted_data}")

                # Decrypt the received data
                decrypted_data = cipher.decrypt(encrypted_data)

                # Process the decrypted command and prepare a response
                response = process_command(decrypted_data)
                encrypted_response = cipher.encrypt(response)

                # Send the encrypted response back to the client
                conn.sendall(encrypted_response.encode())
            except Exception as e:
                # Handle any exceptions during client handling
                print(f"Error with client {address}: {e}")
                break

def validate_login(login_data):
    parts = login_data.split()
    if len(parts) != 3:
        return False
    username, password = parts[1], parts[2]
    return users.get(username) == password

def process_command(command):
    """
    Processes the command received from the client.
    Args:
        command: The decrypted command string from the client.
    Returns:
        A response string based on the command processing result.
    """
    parts = command.split()
    if not parts:
        return "Invalid command format"

    # Processing different commands based on the keyword
    keyword = parts[0].upper()
    if keyword == "SET_TEMP":
        # Handle SET_TEMP command
        if len(parts) == 2 and parts[1].isdigit():
            temperature = int(parts[1])
            return thermostat.set_temperature(temperature)
        else:
            return "Invalid SET_TEMP command format. Usage: SET_TEMP [temperature]"

    elif keyword == "SET_MODE":
        # Handle SET_MODE command
        if len(parts) == 2 and parts[1] in ["HEATING", "COOLING", "OFF"]:
            mode = parts[1]
            return thermostat.set_mode(mode)
        else:
            return "Invalid SET_MODE command format. Usage: SET_MODE [HEATING/COOLING/OFF]"

    elif keyword == "GET_STATUS":
        # Handle GET_STATUS command
        return thermostat.get_status()

    else:
        # Response for unknown command
        return "Unknown command"
        
def start_server():
    """
    Starts the server, listens for incoming connections and handles them using threads.
    """
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Binding the server socket to the host and port
        server_socket.bind((host, port))
        # Start listening for incoming connections
        server_socket.listen()
        print(f"Server is listening on {host}: {port}")

        # Infinite loop to accept and handle client connections
        while True:
            conn, addr = server_socket.accept()
            # Create a new thread for each client connection
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    # Entry point of the script
    start_server()
