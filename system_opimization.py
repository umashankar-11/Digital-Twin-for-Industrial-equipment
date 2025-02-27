import random

class GeneticAlgorithmOptimization:
    def __init__(self, population_size, generations, mutation_rate):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def fitness_function(self, settings):

        rpm, temperature, pressure = settings
        efficiency = (rpm * 0.5) + (100 - temperature) + (30 - abs(pressure - 20))
        return efficiency

    def generate_population(self):
      
        population = []
        for _ in range(self.population_size):
            rpm = random.randint(1000, 4000)
            temperature = random.randint(60, 120)
            pressure = random.randint(10, 30)
            population.append((rpm, temperature, pressure))
        return population

    def mutate(self, settings):
        
        mutated = list(settings)
        if random.random() < self.mutation_rate:
            mutated[random.randint(0, 2)] += random.randint(-10, 10)
        return tuple(mutated)

    def run(self):
        
        population = self.generate_population()
        for generation in range(self.generations):
            population = sorted(population, key=lambda x: self.fitness_function(x), reverse=True)
            print(f"Generation {generation}: Best Fitness = {self.fitness_function(population[0])}")
            next_population = population[:self.population_size // 2]
            next_population = next_population + [self.mutate(x) for x in next_population]
            population = next_population
        return population[0]

ga_optimizer = GeneticAlgorithmOptimization(population_size=10, generations=5, mutation_rate=0.1)
best_settings = ga_optimizer.run()
print("Best Equipment Settings (RPM, Temp, Pressure):", best_settings)
