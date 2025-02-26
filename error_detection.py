import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

normal_data = np.random.normal(0, 1, (100, 2))  

anomalous_data = np.random.normal(5, 1, (10, 2)) 

data = np.vstack([normal_data, anomalous_data])

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(data_scaled)

predictions = model.predict(data_scaled)

plt.figure(figsize=(10, 6))

plt.scatter(data_scaled[predictions == 1, 0], data_scaled[predictions == 1, 1], color="blue", label="Normal")

plt.scatter(data_scaled[predictions == -1, 0], data_scaled[predictions == -1, 1], color="red", label="Anomaly")

plt.title("Anomaly Detection: Equipment Sensor Data")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.show()

anomalies = np.where(predictions == -1)[0]
print(f"Anomalous data points: {anomalies}")
