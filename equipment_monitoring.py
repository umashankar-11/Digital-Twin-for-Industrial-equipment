import random
import numpy as np
import matplotlib.pyplot as plt

class EquipmentHealthMonitor:
    def __init__(self):
        self.temperature = 25  
        self.vibration = 0.3
        self.usage_hours = 0   

    def update_data(self):
        
        self.temperature += random.uniform(-0.5, 0.5)
        self.vibration += random.uniform(-0.05, 0.05)
        self.usage_hours += random.uniform(0.5, 1.5)

        
        health_status = "Healthy"
        if self.temperature > 35 or self.vibration > 0.8:
            health_status = "Warning"
        return self.temperature, self.vibration, self.usage_hours, health_status


monitor = EquipmentHealthMonitor()


temps = []
vibs = []
usage = []
status = []

for _ in range(100):
    temp, vib, use, stat = monitor.update_data()
    temps.append(temp)
    vibs.append(vib)
    usage.append(use)
    status.append(stat)

plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(temps, label="Temperature")
plt.title("Temperature Monitoring")
plt.subplot(3, 1, 2)
plt.plot(vibs, label="Vibration")
plt.title("Vibration Monitoring")
plt.subplot(3, 1, 3)
plt.plot(usage, label="Usage Hours")
plt.title("Usage Hours Monitoring")
plt.tight_layout()
plt.show()


print(f"Last Health Status: {status[-1]}")
