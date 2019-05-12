from route import Route
import random
import math
import copy


class SimulatedAnnealing:
    def __init__(self, states, initial_temperature, cooling_coefficient, minimal_temperature, inc_support, dec_support):
        self.states = states
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.temperature = initial_temperature
        self.initial_temperature = initial_temperature
        self.cooling_coefficient = cooling_coefficient
        self.minimal_temperature = minimal_temperature
        self.best_solution = self.Solution(self.inc_support, self.dec_support)
        self.best_solution.calculate_value()
        self.tabu_list = []

    class Solution(Route):
        def __init__(self, inc_support, dec_support):
            super().__init__(inc_support, dec_support)

        def random_swap(self):
            index_a, index_b = tuple(random.sample(range(len(self.states)), 2))
            self.states[index_b], self.states[index_a] = self.states[index_a], self.states[index_b]

    def probability(self, new_val, old_val):
        return math.e ** (-1 * (((old_val - new_val)/old_val) / (self.temperature/self.initial_temperature)))

    def run(self):
        # Generate random route
        solution = self.Solution(self.inc_support, self.dec_support)
        solution.generate_random(self.states)
        solution.calculate_value()

        # Save this route as best route
        self.best_solution = solution

        while self.temperature > self.minimal_temperature:
            # Copy solution and random swap two states
            new_solution = copy.deepcopy(solution)
            new_solution.random_swap()
            new_solution.calculate_value()

            # Evaluate route value and save it as current route if it is more valuable or rand < probability()
            solution.calculate_value()
            if solution.value > self.best_solution.value \
                    or (random.randint(0, 999) / 1000) < self.probability(new_solution.value, solution.value):
                solution = new_solution

                # Evaluate new route value and save it as best route if it is more valuable
                if solution.value > self.best_solution.value:
                    self.best_solution = solution

            # Lower the temperature value
            self.temperature *= self.cooling_coefficient
