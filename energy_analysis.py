import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

days = np.arange(1, 31)
normal_consumption = np.random.normal(50, 10, 30)  
peak_consumption = np.random.normal(70, 15, 30)    

peak_days = np.random.choice(days, size=5, replace=False)
peak_consumption[peak_days] += 20  

plt.figure(figsize=(10, 6))
plt.plot(days, normal_consumption, label="Normal Consumption", color="blue")
plt.plot(days, peak_consumption, label="Peak Consumption", color="red", linestyle="--")
plt.fill_between(days, normal_consumption, peak_consumption, color="gray", alpha=0.3)
plt.title("Energy Consumption Analysis")
plt.xlabel("Day")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.show()

avg_consumption = np.mean(normal_consumption)
peak_avg = np.mean(peak_consumption)

print(f"Average Normal Consumption: {avg_consumption:.2f} kWh")
print(f"Average Peak Consumption: {peak_avg:.2f} kWh")

if peak_avg > avg_consumption + 15:
    print("Energy optimization suggested: Peak consumption is higher than expected.")
