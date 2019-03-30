from classes import Route
from data import states
import random


class GeneticAlgorithm:
    class Solution:
        def __init__(self, route, value):
            self.route = route
            self.value = value

    def __init__(self, states, no_of_iterations, population_size, inc_support, dec_support):
        self.states = states
        self.no_of_iterations = no_of_iterations
        self.population_size = population_size
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.best_route = None
        self.best_route_value = 0

    def run(self):
        # Generate random population
        population = []
        for i in range(self.population_size):
            route = Route(self.inc_support, self.dec_support)
            route.generate_random(self.states)
            value = route.calculate_value()

            population.append(self.Solution(route, value))

        for i in range(self.no_of_iterations):
            # Choice best solutions
            def my_sort(solution):
                return -solution.value

            population.sort(key=my_sort)
            population = population[:int(self.population_size / 2)]

            # If current best solution is better than global, switch it
            if population[0].value > self.best_route_value:
                self.best_route = population[0].route
                self.best_route_value = population[0].value

            # Crossover and mutate new population
            new_population = []
            while len(new_population) < self.population_size:
                parent_a = random.choice(population)
                parent_b = random.choice(population)

                if parent_a == parent_b:
                    continue

                child_a, child_b = Route.pmx(parent_a.route, parent_b.route)

                # Mutate child A
                child_a.random_swap()

                # Mutate child B
                child_b.random_swap()

                new_population.append(self.Solution(child_a, child_a.calculate_value()))
                new_population.append(self.Solution(child_b, child_b.calculate_value()))

            # Switch populations
            population = new_population
