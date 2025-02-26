import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def generate_data(num_samples=1000):
    np.random.seed(42)
    temperature = np.random.normal(25, 5, num_samples)  
    vibration = np.random.normal(0.5, 0.1, num_samples)  
    failure = (temperature > 30) | (vibration > 0.7)  
    return pd.DataFrame({"Temperature": temperature, "Vibration": vibration, "Failure": failure})


data = generate_data()


X = data[["Temperature", "Vibration"]]
y = data["Failure"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
y_pred_binary = (y_pred > 0.5).astype(int)


mse = mean_squared_error(y_test, y_pred_binary)
accuracy = np.mean(y_pred_binary == y_test)

print(f"Mean Squared Error: {mse}")
print(f"Accuracy: {accuracy * 100:.2f}%")


plt.figure(figsize=(10, 6))
plt.scatter(X_test["Temperature"], y_test, color="blue", label="Actual Failure")
plt.scatter(X_test["Temperature"], y_pred_binary, color="red", label="Predicted Failure")
plt.xlabel("Temperature")
plt.ylabel("Failure (0 = No, 1 = Yes)")
plt.title("Predictive Maintenance: Failure Prediction")
plt.legend()
plt.show()
