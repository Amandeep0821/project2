#AMANDEEP SINGH (100893335)

import json
import socket
import time
import subprocess
import tkinter as tk

# Function to collect system data
def collate_data(iteration):
    # Try to get system information and handle exceptions
    try:
        core_temp = float(subprocess.check_output(["vcgencmd", "measure_temp"]).decode()[5:-3])
    except ValueError:
        core_temp = 0.0

    try:
        cpu_clock_freq = float(subprocess.check_output(["vcgencmd", "measure_clock", "arm"]).decode()[14:])
    except ValueError:
        cpu_clock_freq = 0.0

    try:
        gpu_clock_freq = float(subprocess.check_output(["vcgencmd", "measure_clock", "core"]).decode()[14:])
    except ValueError:
        gpu_clock_freq = 0.0

    try:
        memory_usage = float(subprocess.check_output(["vcgencmd", "get_mem", "arm"]).decode()[10:])
    except ValueError:
        memory_usage = 0.0

    try:
        core_voltage = float(subprocess.check_output(["vcgencmd", "measure_volts", "core"]).decode()[5:])
    except ValueError:
        core_voltage = 0.0

    # Create a dictionary with collected data
    data = {
        'core_temperature': core_temp,
        'cpu_clock_frequency': cpu_clock_freq,
        'gpu_clock_frequency': gpu_clock_freq,
        'memory_usage': memory_usage,
        'core_voltage': core_voltage,
        'iteration': iteration
    }
    return data

# Function to create the GUI
def create_gui():
    gui = tk.Tk()
    gui.title("Client GUI")

    # Labels to display various system information
    connection_label = tk.Label(gui, text="Connection: OFF", fg="red")
    connection_label.grid(row=0, column=0, columnspan=2)

    core_temp_label = tk.Label(gui, text="Core Temperature: N/A")
    core_temp_label.grid(row=1, column=0, columnspan=2)

    cpu_freq_label = tk.Label(gui, text="CPU Clock Frequency: N/A")
    cpu_freq_label.grid(row=2, column=0, columnspan=2)

    gpu_freq_label = tk.Label(gui, text="GPU Clock Frequency: N/A")
    gpu_freq_label.grid(row=3, column=0, columnspan=2)

    mem_label = tk.Label(gui, text="Memory Usage: N/A")
    mem_label.grid(row=4, column=0, columnspan=2)

    voltage_label = tk.Label(gui, text="Core Voltage: N/A")
    voltage_label.grid(row=5, column=0, columnspan=2)

    led_label = tk.Label(gui, text="LED: OFF", fg="red", font=("Arial", 20, "bold"))
    led_label.grid(row=6, column=0, columnspan=2)

    # Button to exit the GUI
    exit_button = tk.Button(gui, text="Exit", command=gui.destroy)
    exit_button.grid(row=7, column=0, columnspan=2)

    return gui, connection_label, core_temp_label, cpu_freq_label, gpu_freq_label, mem_label, voltage_label, led_label

# Function to update the connection status on the GUI
def update_connection_status(label, status):
    color = "green" if status else "red"
    label.config(text=f"Connection: {'ON' if status else 'OFF'}", fg=color)

# Function to update the LED status on the GUI
def update_led_status(label, status):
    color = "green" if status else "red"
    label.config(text=f"LED: {'ON' if status else 'OFF'}", fg=color)

# Function to update the displayed system information on the GUI
def update_values(core_temp_label, cpu_freq_label, gpu_freq_label, mem_label, voltage_label, data):
    core_temp_label.config(text=f"Core Temperature: {data['core_temperature']} °C")
    cpu_freq_label.config(text=f"CPU Clock Frequency: {data['cpu_clock_frequency']} Hz")
    gpu_freq_label.config(text=f"GPU Clock Frequency: {data['gpu_clock_frequency']} Hz")
    mem_label.config(text=f"Memory Usage: {data['memory_usage']} MB")
    voltage_label.config(text=f"Core Voltage: {data['core_voltage']} V")

# Main function
def main():
    # Set server host and port
    host = ''  # Assuming server runs on the same machine
    port = 5555

    # Create GUI
    gui, connection_label, core_temp_label, cpu_freq_label, gpu_freq_label, mem_label, voltage_label, led_label = create_gui()

    try:
        # Set up client socket and connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            update_connection_status(connection_label, True)

            # Send 50 iterations of system data to the server
            for iteration in range(50):
                data = collate_data(iteration)
                json_data = json.dumps(data)
                client_socket.sendall(json_data.encode())
                update_values(core_temp_label, cpu_freq_label, gpu_freq_label, mem_label, voltage_label, data)
                update_led_status(led_label, True)
                time.sleep(2)  # Sending data every 2 seconds

            # Update connection status to OFF after sending data
            update_connection_status(connection_label, False)

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

