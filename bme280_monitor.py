import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from datetime import datetime

# --- Configuration ---
PORT = "/dev/ttyAMA0"  # RPi 5 GPIO UART
BAUD = 115200
MAX_POINTS = 50

# --- Data Storage ---
timestamps = deque(maxlen=MAX_POINTS)
temps      = deque(maxlen=MAX_POINTS)
humidities = deque(maxlen=MAX_POINTS)
pressures  = deque(maxlen=MAX_POINTS)

# --- Serial Connection ---
ser = serial.Serial(PORT, BAUD, timeout=20)
time.sleep(2)

# --- Graph Setup ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle('BME280 Environmental Monitor', fontsize=14, fontweight='bold')

def read_serial():
    try:
        line = ser.readline().decode("utf-8").strip()
        if line.startswith("DATA,"):
            values = line.split(",")
            return float(values[1]), float(values[2]), float(values[3])
    except:
        pass
    return None

def update(frame):
    data = read_serial()
    if data:
        temp, humidity, pressure = data
        now = datetime.now().strftime("%H:%M:%S")

        timestamps.append(now)
        temps.append(temp)
        humidities.append(humidity)
        pressures.append(pressure)

        ax1.clear()
        ax1.plot(list(timestamps), list(temps), 'r-o', linewidth=2)
        ax1.set_ylabel('Temperature (°C)', color='red')
        ax1.set_title(f'Temperature: {temp:.1f} °C')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)

        ax2.clear()
        ax2.plot(list(timestamps), list(humidities), 'b-o', linewidth=2)
        ax2.set_ylabel('Humidity (%)', color='blue')
        ax2.set_title(f'Humidity: {humidity:.1f} %')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)

        ax3.clear()
        ax3.plot(list(timestamps), list(pressures), 'g-o', linewidth=2)
        ax3.set_ylabel('Pressure (hPa)', color='green')
        ax3.set_title(f'Pressure: {pressure:.1f} hPa')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)

        plt.tight_layout()
        print(f"[{now}] Temp: {temp}C | Humidity: {humidity}% | Pressure: {pressure}hPa")

ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
plt.tight_layout()
plt.show()
