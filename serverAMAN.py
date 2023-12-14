#AMANDEEP SINGH (100893335)

import socket
import json
import tkinter as tk

# Function to create the GUI
def create_gui():
    gui = tk.Tk()
    gui.title("Server GUI")

    # Label to display LED status
    led_label = tk.Label(gui, text="LED: OFF", fg="red", font=("Arial", 20, "bold"))
    led_label.grid(row=0, column=0, columnspan=2)

    # Button to exit the GUI
    exit_button = tk.Button(gui, text="Exit", command=gui.destroy)
    exit_button.grid(row=1, column=0, columnspan=2)

    return gui, led_label

# Function to update the LED status on the GUI
def update_led_status(label, status):
    color = "green" if status else "red"
    label.config(text=f"LED: {'ON' if status else 'OFF'}", fg=color)

# Main function
def main():
    # Define server host and port
    host = '127.0.0.1'  # Listen on all available interfaces
    port = 5555

    # Create GUI
    gui, led_label = create_gui()

    try:
        # Set up server socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5)

            print(f"Server listening on port {port}")

            # Accept connection from a client
            connection, addr = server_socket.accept()
            print('Got connection from', addr)

            # Update LED status on GUI to ON
            update_led_status(led_label, True)

            # Receive and process data in a loop
            while True:
                data = connection.recv(1024)
                if not data:
                    break

                # Decode received JSON data
                decoded_data = json.loads(data.decode())
                print(f"Received data: {decoded_data}")

            # Update LED status on GUI to OFF when the loop breaks
            update_led_status(led_label, False)

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
    finally:
        # Run the GUI main loop and print a message when the process ends
        gui.mainloop()
        print("Process ended with exit code 0.")

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
