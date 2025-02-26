import random
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class EquipmentSensor:
    def __init__(self):
        self.temperature = 25  
        self.vibration = 0.5  

    def update_data(self):
        
        self.temperature += random.uniform(-0.5, 0.5)  
        self.vibration += random.uniform(-0.05, 0.05)  

        
        return self.temperature, self.vibration


class RealTimeMonitor:
    def __init__(self):
        self.sensor = EquipmentSensor()
        self.temperature_data = []
        self.vibration_data = []

    def update_plot(self, frame):
        temp, vib = self.sensor.update_data()

        self.temperature_data.append(temp)
        self.vibration_data.append(vib)

        
        if len(self.temperature_data) > 100:
            self.temperature_data.pop(0)
            self.vibration_data.pop(0)

        ax1.clear()
        ax2.clear()

        ax1.plot(self.temperature_data, label="Temperature (°C)", color="tab:red")
        ax2.plot(self.vibration_data, label="Vibration (m/s²)", color="tab:blue")

        ax1.set_title("Real-Time Temperature Monitoring")
        ax2.set_title("Real-Time Vibration Monitoring")

        ax1.set_ylabel("Temperature (°C)")
        ax2.set_ylabel("Vibration (m/s²)")

        ax1.legend(loc="upper right")
        ax2.legend(loc="upper right")

        ax1.set_ylim([20, 30])
        ax2.set_ylim([0, 1])


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
real_time_monitor = RealTimeMonitor()

ani = FuncAnimation(fig, real_time_monitor.update_plot, interval=1000)
plt.tight_layout()
plt.show()
