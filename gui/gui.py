import serial
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

# --- Configuration ---
PORT = "/dev/ttyAMA0"
BAUD = 115200
RESULTS_FOLDER = "results"
CSV_FILENAME = "bme280_log.csv"

# --- Setup Data Logging ---
# Create the results folder if it doesn't exist yet
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

filepath = os.path.join(RESULTS_FOLDER, CSV_FILENAME)

# If the file is brand new, create it and write the column headers
if not os.path.exists(filepath):
    with open(filepath, "w") as f:
        f.write("Timestamp,Temperature(C),Humidity(%),Pressure(hPa)\n")

# --- Open Serial Port ---
try:
    ser = serial.Serial(PORT, BAUD, timeout=2)
except Exception as e:
    print(f"Failed to open port: {e}")
    exit()

def fetch_data():
    """Triggered when the button is clicked"""
    try:
        # 1. Clear any old junk out of the pipeline
        ser.reset_input_buffer()
        
        # 2. Ask the STM32 for data
        ser.write(b"GET\n")
        
        # 3. Read the reply
        line = ser.readline().decode("utf-8").strip()
        
        # 4. Process and Save the data
        if line.startswith("DATA,"):
            values = line.split(",")
            temp_val = float(values[1])
            hum_val = float(values[2])
            press_val = float(values[3])
            
            # Update the screen labels
            temp_label.config(text=f"{temp_val:.1f} °C")
            hum_label.config(text=f"{hum_val:.1f} %")
            press_label.config(text=f"{press_val:.1f} hPa")
            
            # Get the current time
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save the new row to the CSV file
            with open(filepath, "a") as f:
                f.write(f"{now},{temp_val},{hum_val},{press_val}\n")
                
            print(f"[{now}] Saved to {filepath}")
            
        else:
            messagebox.showwarning("Timeout", "Did not receive data from STM32.")
            
    except Exception as e:
        messagebox.showerror("Error", f"Communication failed: {e}")

# --- Build the GUI Window ---
root = tk.Tk()
root.title("BME280 Monitor & Logger")
root.geometry("300x350")
root.configure(padx=20, pady=20)

# Temperature Display
tk.Label(root, text="Temperature", font=("Arial", 12)).pack()
temp_label = tk.Label(root, text="-- °C", font=("Arial", 24, "bold"), fg="red")
temp_label.pack(pady=(0, 10))

# Humidity Display
tk.Label(root, text="Humidity", font=("Arial", 12)).pack()
hum_label = tk.Label(root, text="-- %", font=("Arial", 24, "bold"), fg="blue")
hum_label.pack(pady=(0, 10))

# Pressure Display
tk.Label(root, text="Pressure", font=("Arial", 12)).pack()
press_label = tk.Label(root, text="-- hPa", font=("Arial", 24, "bold"), fg="green")
press_label.pack(pady=(0, 20))

# The Clickable Button
btn = tk.Button(root, text="Get & Save Data", font=("Arial", 14), command=fetch_data, bg="#e0e0e0")
btn.pack(fill="x")

# Start the application
root.mainloop()
