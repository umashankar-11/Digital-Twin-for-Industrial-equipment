import random
import time
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
import logging
import threading

class IndustrialEquipment:
    def __init__(self, id, name, max_capacity, efficiency, failure_rate, failure_types, location="Factory Floor", operating_temp_range=(0, 100)):
        self.id = id
        self.name = name
        self.max_capacity = max_capacity
        self.efficiency = efficiency
        self.failure_rate = failure_rate
        self.failure_types = failure_types
        self.location = location
        self.operating_temp_range = operating_temp_range
        self.current_capacity = 0
        self.status = "operational" 
        self.logs = []  
        self.operational_time = 0  
        self.downtime = 0  
        self.failure_count = 0  
        self.temperature = 20 

    def simulate_operation(self):
        
        if self.status == "operational":
            self.efficiency -= random.uniform(0, 0.05)
            self.efficiency = max(0, self.efficiency)
            self.current_capacity = self.max_capacity * self.efficiency
      
            self.temperature += random.uniform(-2, 2)  
            if self.temperature < self.operating_temp_range[0] or self.temperature > self.operating_temp_range[1]:
                self.status = "failed"
                self.logs.append(f"{datetime.now()}: Equipment {self.name} failed due to temperature out of range!")
                self.failure_count += 1
                print(f"Equipment {self.name} has failed due to temperature out of range!")
            
            failure_type = random.choice(self.failure_types)
            if random.random() < self.failure_rate:
                self.status = "failed"
                self.failure_count += 1
                self.logs.append(f"{datetime.now()}: Equipment {self.name} failed due to {failure_type}.")
                print(f"Equipment {self.name} has failed due to {failure_type}!")
            else:
                print(f"Equipment {self.name} is operating at {self.efficiency * 100:.2f}% efficiency.")
                self.operational_time += 1 
                
        return self.status, self.current_capacity, self.temperature

    def perform_maintenance(self):
        
        self.status = "operational"
        self.efficiency = 1.0  
        self.logs.append(f"{datetime.now()}: Equipment {self.name} has been restored to operational state.")
        print(f"Equipment {self.name} is now operational after maintenance.")

    def get_efficiency(self):
        
        return self.efficiency * 100  

    def get_performance_parameters(self):
    
        if self.operational_time + self.downtime == 0:
            uptime_percentage = 0  
        else:
            uptime_percentage = (self.operational_time / (self.operational_time + self.downtime)) * 100
        return {
            "Uptime Percentage": uptime_percentage,
            "Failure Count": self.failure_count,
            "Downtime (hrs)": self.downtime,
            "Current Efficiency (%)": self.get_efficiency(),
            "Temperature (°C)": self.temperature
        }

class Sensor:
    def __init__(self, sensor_id, equipment_id, sensor_type, unit, min_value, max_value, failure_type=None, drift_rate=0.01):
        self.sensor_id = sensor_id
        self.equipment_id = equipment_id
        self.sensor_type = sensor_type
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.value = self.generate_random_value()
        self.failure_type = failure_type  
        self.drift_rate = drift_rate  

    def generate_random_value(self):
        
        return random.uniform(self.min_value, self.max_value)

    def read_sensor(self):
       
        if self.failure_type == "stuck":
            return self.value  
        elif self.failure_type == "overload":
            return random.uniform(self.max_value - 10, self.max_value)  
        elif self.failure_type == "drift":
            self.value += random.uniform(-self.drift_rate, self.drift_rate) 
            self.value = max(self.min_value, min(self.max_value, self.value))  
            return self.value
        else:
            self.value = self.generate_random_value()
            return self.value

    def __repr__(self):
        return f"Sensor {self.sensor_id}: {self.sensor_type} ({self.unit}), Reading: {self.value}"


class Database:
    def __init__(self, db_name="digital_twin.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            equipment_id TEXT,
            value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id TEXT,
            status TEXT,
            efficiency REAL,
            temperature REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.connection.commit()

    def store_data(self, sensor_id, equipment_id, value):
       
        self.cursor.execute('''
        INSERT INTO sensor_data (sensor_id, equipment_id, value) 
        VALUES (?, ?, ?)''', (sensor_id, equipment_id, value))
        self.connection.commit()

    def store_equipment_data(self, equipment_id, status, efficiency, temperature):
        
        self.cursor.execute('''
        INSERT INTO equipment_data (equipment_id, status, efficiency, temperature)
        VALUES (?, ?, ?, ?)''', (equipment_id, status, efficiency, temperature))
        self.connection.commit()

    def retrieve_data(self, sensor_id, limit=10):
        
        self.cursor.execute('''
        SELECT * FROM sensor_data WHERE sensor_id = ? ORDER BY timestamp DESC LIMIT ?''', (sensor_id, limit))
        return self.cursor.fetchall()

    def retrieve_equipment_data(self, equipment_id, limit=10):
        
        self.cursor.execute('''
        SELECT * FROM equipment_data WHERE equipment_id = ? ORDER BY timestamp DESC LIMIT ?''', (equipment_id, limit))
        return self.cursor.fetchall()

    def close(self):
       
        self.connection.close()

class PredictiveMaintenance:
    def __init__(self, historical_data):
        self.model = LinearRegression()
        self.train_model(historical_data)

    def train_model(self, data):
        
        X = np.array([d[0] for d in data]).reshape(-1, 1)  # Assume 1 feature (e.g., time)
        y = np.array([d[1] for d in data])  
        self.model.fit(X, y)

    def predict_failure(self, current_time):
        
        prediction = self.model.predict([[current_time]])
        return prediction[0]

    def check_for_failure(self, current_time, threshold=0.1):
       
        prediction = self.predict_failure(current_time)
        if prediction < threshold:
            print(f"Prediction indicates failure risk at time {current_time}")
            return True
        return False

class ReportGenerator:
    def __init__(self, equipment, db):
        self.equipment = equipment
        self.db = db
        self.logger = logging.getLogger("ReportLogger")
        logging.basicConfig(filename="equipment_report.log", level=logging.INFO)

    def log_equipment_status(self):
       
        performance = self.equipment.get_performance_parameters()
        self.logger.info(f"Equipment {self.equipment.id} Status Report")
        self.logger.info(f"Status: {self.equipment.status}")
        self.logger.info(f"Efficiency: {self.equipment.get_efficiency():.2f}%")
        self.logger.info(f"Temperature: {self.equipment.temperature} °C")
        self.logger.info(f"Uptime Percentage: {performance['Uptime Percentage']}%")
        self.logger.info(f"Failure Count: {performance['Failure Count']}")
        self.logger.info(f"Downtime: {performance['Downtime (hrs)']} hours")

    def generate_report(self):
        
        self.log_equipment_status()
        print(f"\n--- Report for Equipment {self.equipment.id} ---")
        print(f"Status: {self.equipment.status}")
        for sensor in self.equipment.logs:
            print(sensor)
            
class DigitalTwinControl:
    def __init__(self, equipment_list, sensors, database, predictive_maintenance, report_generator):
        self.equipment_list = equipment_list
        self.sensors = sensors
        self.db = database
        self.predictive_maintenance = predictive_maintenance
        self.report_generator = report_generator

    def start_simulation(self):
        
        while True:
            for equipment in self.equipment_list:
                status, capacity, temperature = equipment.simulate_operation()

                for sensor in self.sensors:
                    if sensor.equipment_id == equipment.id:
                        value = sensor.read_sensor()
                        self.db.store_data(sensor.sensor_id, equipment.id, value)

                self.db.store_equipment_data(equipment.id, equipment.status, equipment.get_efficiency(), equipment.temperature)

                current_time = time.time()
                if self.predictive_maintenance.check_for_failure(current_time):
                    print("Initiating maintenance process...")
                    equipment.perform_maintenance()

                self.report_generator.generate_report()

            time.sleep(5)

equipment_1 = IndustrialEquipment("001", "Pump A", max_capacity=1000, efficiency=0.9, failure_rate=0.1, failure_types=["overload", "temperature"], location="Factory Floor")
equipment_2 = IndustrialEquipment("002", "Fan B", max_capacity=800, efficiency=0.85, failure_rate=0.08, failure_types=["bearing failure", "temperature"], location="Assembly Line")
sensor_1 = Sensor("S1", "001", "Temperature", "°C", 10, 100, failure_type="drift")
sensor_2 = Sensor("S2", "001", "Pressure", "bar", 0, 20)
sensor_3 = Sensor("S3", "002", "Temperature", "°C", 10, 100)
sensor_4 = Sensor("S4", "002", "Vibration", "m/s", 0, 10)
db = Database()
predictive_maintenance = PredictiveMaintenance(historical_data=[(1, 95), (2, 92), (3, 90)])
report_generator = ReportGenerator(equipment_1, db)

digital_twin_control = DigitalTwinControl([equipment_1, equipment_2], [sensor_1, sensor_2, sensor_3, sensor_4], db, predictive_maintenance, report_generator)
digital_twin_control.start_simulation()
