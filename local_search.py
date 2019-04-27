from route import Route
import copy


class LocalSearch:
    def __init__(self, states, no_of_iterations, inc_support, dec_support):
        self.states = states
        self.no_of_iterations = no_of_iterations
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.best_solution = self.Solution(self.inc_support, self.dec_support)
        self.best_solution.calculate_value()

    class Solution(Route):
        def __init__(self, inc_support, dec_support):
            super().__init__(inc_support, dec_support)

        def swap(self, state_a, state_b):
            index_a, index_b = self.states.index(state_a), self.states.index(state_b)
            self.states[index_b], self.states[index_a] = self.states[index_a], self.states[index_b]

    def run(self):
        # Generate random route
        solution = self.Solution(self.inc_support, self.dec_support)
        solution.generate_random(self.states)
        solution.calculate_value()

        # Save this route as best route
        self.best_solution = solution

        for i in range(self.no_of_iterations):
            # Choice best move regarding the tabu list
            tmp_best_solution = self.Solution(self.inc_support, self.dec_support)

            for i in self.states:
                for j in self.states:
                    if i != j:
                        tmp_solution = copy.deepcopy(solution)
                        tmp_solution.swap(i, j)
                        tmp_solution.calculate_value()
                        if tmp_solution.value > tmp_best_solution.value:
                            tmp_best_solution = tmp_solution

            solution = tmp_best_solution

            # Evaluate route value and save it as best route if it is more valuable
            solution.calculate_value()
            if solution.value > self.best_solution.value:
                self.best_solution = copy.copy(solution)
