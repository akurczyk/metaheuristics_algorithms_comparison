from route import Route
import datetime


class RandomSearch:
    def __init__(self, states, seconds, inc_support, dec_support):
        self.states = states
        self.seconds = seconds
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.best_solution = Route(inc_support, dec_support)
        self.best_solution.calculate_value()

    def run(self):
        finish = datetime.datetime.now() + datetime.timedelta(seconds=self.seconds)
        while datetime.datetime.now() < finish:
            route = Route(self.inc_support, self.dec_support)
            route.generate_random(self.states)
            route.calculate_value()

            if route.value > self.best_solution.value:
                self.best_solution = route
