from classes import Route


class RandomSearch:
    def __init__(self, states, no_of_iterations, inc_support, dec_support):
        self.states = states
        self.no_of_iterations = no_of_iterations
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.best_route = None
        self.best_route_value = 0

    def run(self):
        for i in range(self.no_of_iterations):
            route = Route(self.inc_support, self.dec_support)
            route.generate_random(self.states)
            route_value = route.calculate_value()

            if route_value > self.best_route_value:
                self.best_route = route
                self.best_route_value = route_value
