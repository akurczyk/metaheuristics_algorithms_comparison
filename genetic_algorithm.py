from route import Route
import random
import datetime


class GeneticAlgorithm:
    def __init__(self, states, seconds, population_size, crossover, mutate, inc_support, dec_support):
        self.states = states
        self.seconds = seconds
        self.population_size = population_size
        self.crossover = crossover
        self.mutate = mutate
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.best_solution = self.Solution(self.inc_support, self.dec_support)
        self.best_solution.calculate_value()

    class Solution(Route):
        def __init__(self, inc_support, dec_support):
            super().__init__(inc_support, dec_support)

        @staticmethod
        def crossover(solution_a, solution_b, kind):
            parent_a = solution_a.states
            parent_b = solution_b.states

            random_a = random.randint(0, len(parent_a))
            random_b = random.randint(0, len(parent_a))

            begin = min(random_a, random_b)
            end = max(random_a, random_b)

            child_a = []
            child_b = []

            # PMX
            if kind == 'pmx':
                child_a = parent_a[:begin] + parent_b[begin:end] + parent_a[end:]
                child_b = parent_b[:begin] + parent_a[begin:end] + parent_b[end:]

                for i in range(len(parent_a)):
                    if i < begin or i >= end:
                        while child_a[i] in child_a[begin:end]:
                            pos = child_a[begin:end].index(child_a[i]) + begin
                            child_a[i] = child_b[pos]

                for i in range(len(parent_a)):
                    if i < begin or i >= end:
                        while child_b[i] in child_b[begin:end]:
                            pos = child_b[begin:end].index(child_b[i]) + begin
                            child_b[i] = child_a[pos]

            # OX
            elif kind == 'ox':
                child_a = [element for element in parent_b if element not in parent_a[begin:end]][:begin]\
                          + parent_a[begin:end]\
                          + [element for element in parent_b if element not in parent_a[begin:end]][begin:]

                child_b = [element for element in parent_a if element not in parent_b[begin:end]][:begin]\
                          + parent_b[begin:end]\
                          + [element for element in parent_a if element not in parent_b[begin:end]][begin:]

            solution_c = GeneticAlgorithm.Solution(solution_a.inc_support, solution_a.dec_support)
            solution_c.states = child_a

            solution_d = GeneticAlgorithm.Solution(solution_a.inc_support, solution_a.dec_support)
            solution_d.states = child_b

            return solution_c, solution_d

        def mutate(self, kind):
            index_a, index_b = tuple(random.sample(range(len(self.states)), 2))
            if index_b < index_a:
                index_a, index_b = index_b, index_a

            if kind == 'transposition':
                self.states[index_b], self.states[index_a] = self.states[index_a], self.states[index_b]

            elif kind == 'insertion':
                self.states = self.states[:index_a]\
                              + self.states[index_a+1:index_b]\
                              + [self.states[index_a]]\
                              + self.states[index_b:]

            elif kind == 'inversion':
                self.states = self.states[:index_a]\
                              + self.states[index_a:index_b][::-1]\
                              + self.states[index_b:]

    def run(self):
        # Generate random population
        population = []
        for i in range(self.population_size):
            solution = self.Solution(self.inc_support, self.dec_support)
            solution.generate_random(self.states)
            solution.calculate_value()

            population.append(solution)

        finish = datetime.datetime.now() + datetime.timedelta(seconds=self.seconds)
        while datetime.datetime.now() < finish:
            # Choice best solutions
            def my_sort(solution):
                return -solution.value

            population.sort(key=my_sort)
            population = population[:int(self.population_size / 2)]

            # If current best solution is better than global, switch it
            if population[0].value > self.best_solution.value:
                self.best_solution = population[0]

            # Crossover and mutate new population
            new_population = []
            while len(new_population) < self.population_size:
                parent_a = random.choice(population)
                parent_b = random.choice(population)

                if parent_a == parent_b:
                    continue

                child_a, child_b = self.Solution.crossover(parent_a, parent_b, self.crossover)

                # Mutate childes
                child_a.mutate(self.mutate)
                child_b.mutate(self.crossover)

                # Calculate childes values
                child_a.calculate_value()
                child_b.calculate_value()

                # Add new childes to new population
                new_population.append(child_a)
                new_population.append(child_b)

            # Switch populations
            population = new_population
