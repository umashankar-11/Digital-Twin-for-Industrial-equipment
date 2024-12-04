import random
import time
import numpy as np

class Motor:
    def __init__(self, id, max_speed, efficiency):
        self.id = id
        self.max_speed = max_speed  # in RPM
        self.efficiency = efficiency  # percentage
        self.current_speed = 0
        self.temperature = 25  # in Celsius

    def run(self, speed):
        if speed > self.max_speed:
            raise ValueError("Speed exceeds maximum limit.")
        self.current_speed = speed
        self.temperature += self.simulate_temperature_increase(speed)

    def simulate_temperature_increase(self, speed):
        return speed * 0.1  # simplistic model for temperature increase

    def report_status(self):
        return {
            "id": self.id,
            "current_speed": self.current_speed,
            "temperature": self.temperature,
            "efficiency": self.efficiency
        }

class DigitalTwin:
    def __init__(self, motor):
        self.motor = motor
        self.history = []

    def update(self):
        status = self.motor.report_status()
        self.history.append(status)
        self.monitor_health()

    def monitor_health(self):
        if self.motor.temperature > 80:  # threshold for warning
            print(f"Warning: Motor {self.motor.id} temperature is too high!")

    def simulate_operation(self, duration, speed_range):
        for _ in range(duration):
            speed = random.randint(*speed_range)
            self.motor.run(speed)
            self.update()
            time.sleep(1)  # Simulate time delay for each operation

if __name__ == "__main__":
    # Create a motor and its digital twin
    motor = Motor(id="M1", max_speed=3000, efficiency=90)
    digital_twin = DigitalTwin(motor)

    # Simulate the motor operation for 10 seconds with speed between 500 and 2500 RPM
    digital_twin.simulate_operation(duration=2, speed_range=(500, 2500))

    # Print the history of the digital twin
    print("\nDigital Twin History:")
    for record in digital_twin.history:
        print(record)
