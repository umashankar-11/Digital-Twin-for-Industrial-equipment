import numpy as np
import matplotlib.pyplot as plt
import random

class ScenarioPlanning:
    def __init__(self, num_scenarios, time_horizon, growth_rate_range, uncertainty_factor):
        self.num_scenarios = num_scenarios
        self.time_horizon = time_horizon
        self.growth_rate_range = growth_rate_range
        self.uncertainty_factor = uncertainty_factor
        self.scenarios = []

    def generate_scenarios(self):
        for _ in range(self.num_scenarios):
            initial_value = random.uniform(100, 200)
            growth_rate = random.uniform(*self.growth_rate_range)
            uncertainty = random.uniform(-self.uncertainty_factor, self.uncertainty_factor)
            scenario = self.simulate_scenario(initial_value, growth_rate, uncertainty)
            self.scenarios.append(scenario)

    def simulate_scenario(self, initial_value, growth_rate, uncertainty):
        values = []
        for t in range(self.time_horizon):
            growth = initial_value * (1 + growth_rate + random.uniform(-uncertainty, uncertainty))
            values.append(growth)
            initial_value = growth
        return values

    def plot_scenarios(self):
        plt.figure(figsize=(10, 6))
        for i, scenario in enumerate(self.scenarios):
            plt.plot(range(self.time_horizon), scenario, label=f"Scenario {i+1}")
        plt.title("Scenario Planning Simulation")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_summary_statistics(self):
        summaries = []
        for scenario in self.scenarios:
            mean_value = np.mean(scenario)
            std_dev = np.std(scenario)
            min_value = np.min(scenario)
            max_value = np.max(scenario)
            summaries.append((mean_value, std_dev, min_value, max_value))
        return summaries

    def display_summary(self):
        summaries = self.get_summary_statistics()
        for i, (mean, std, min_val, max_val) in enumerate(summaries):
            print(f"Scenario {i+1}: Mean: {mean:.2f}, Std Dev: {std:.2f}, Min: {min_val:.2f}, Max: {max_val:.2f}")

    def generate_best_case_worst_case(self):
        best_case = max(self.scenarios, key=lambda x: np.mean(x))
        worst_case = min(self.scenarios, key=lambda x: np.mean(x))
        return best_case, worst_case

    def display_best_worst_case(self):
        best_case, worst_case = self.generate_best_case_worst_case()
        plt.figure(figsize=(10, 6))
        plt.plot(range(self.time_horizon), best_case, label="Best Case", color='g')
        plt.plot(range(self.time_horizon), worst_case, label="Worst Case", color='r')
        plt.title("Best and Worst Case Scenarios")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()

    def calculate_risk(self):
        risks = []
        for scenario in self.scenarios:
            risk = np.std(scenario) / np.mean(scenario)
            risks.append(risk)
        return risks

    def display_risk(self):
        risks = self.calculate_risk()
        plt.figure(figsize=(10, 6))
        plt.bar(range(1, self.num_scenarios + 1), risks)
        plt.title("Scenario Risk Analysis")
        plt.xlabel("Scenario")
        plt.ylabel("Risk (Std Dev / Mean)")
        plt.grid(True)
        plt.show()

    def perform_sensitivity_analysis(self, growth_rate_range, uncertainty_factor_range):
        sensitivity_results = []
        for growth_rate in growth_rate_range:
            for uncertainty in uncertainty_factor_range:
                self.growth_rate_range = (growth_rate, growth_rate)
                self.uncertainty_factor = uncertainty
                self.generate_scenarios()
                risk = self.calculate_risk()
                sensitivity_results.append((growth_rate, uncertainty, np.mean(risk)))
        return sensitivity_results

    def plot_sensitivity_analysis(self, results):
        growth_rates = [result[0] for result in results]
        uncertainties = [result[1] for result in results]
        risks = [result[2] for result in results]

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(growth_rates, uncertainties, risks, c=risks, cmap='viridis')
        ax.set_xlabel('Growth Rate')
        ax.set_ylabel('Uncertainty')
        ax.set_zlabel('Risk')
        ax.set_title('Sensitivity Analysis')
        plt.show()

if __name__ == "__main__":
    num_scenarios = 5
    time_horizon = 20
    growth_rate_range = (0.01, 0.05)
    uncertainty_factor = 0.02

    scenario_planner = ScenarioPlanning(num_scenarios, time_horizon, growth_rate_range, uncertainty_factor)
    scenario_planner.generate_scenarios()
    scenario_planner.plot_scenarios()
    scenario_planner.display_summary()
    scenario_planner.display_best_worst_case()
    scenario_planner.display_risk()

    sensitivity_results = scenario_planner.perform_sensitivity_analysis([0.01, 0.02, 0.03], [0.01, 0.02, 0.03])
    scenario_planner.plot_sensitivity_analysis(sensitivity_results)
