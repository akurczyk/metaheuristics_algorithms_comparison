from route import Route


class RandomSearch:
    def __init__(self, states, no_of_iterations, inc_support, dec_support):
        self.states = states
        self.no_of_iterations = no_of_iterations
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.best_solution = None

    def run(self):
        for i in range(self.no_of_iterations):
            route = Route(self.inc_support, self.dec_support)
            route.generate_random(self.states)
            route.calculate_value()

            if route.value > self.best_solution.value:
                self.best_solution = route
