from classes import Route
import random


class TabuSearch:
    class TabuEntry:
        def __init__(self, state_a, state_b, cadence):
            self.state_a = state_a
            self.state_b = state_b
            self.cadence = cadence

    def __init__(self, states, no_of_iterations, initial_cadence, critical_event, inc_support, dec_support):
        self.states = states
        self.no_of_iterations = no_of_iterations
        self.initial_cadence = initial_cadence
        self.critical_event = critical_event
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.critical_event_counter = 0
        self.best_route = None
        self.best_route_value = 0
        self.tabu_list = []

    def is_swap_legal(self, state_a, state_b):
        if state_a == state_b:
            return False

        for tabu_entry in self.tabu_list:
            if tabu_entry.state_a == state_a and tabu_entry.state_b == state_b \
                    or tabu_entry.state_a == state_b and tabu_entry.state_b == state_a:
                return False

        return True

    def update_tabu_list(self):
        for tabu_entry in self.tabu_list:
            tabu_entry.cadence -= 1
            if tabu_entry.cadence == 0:
                self.tabu_list.remove(tabu_entry)

    def run(self):
        # Generate random route
        route = Route(self.inc_support, self.dec_support)
        route.generate_random(self.states)
        route_value = route.calculate_value()

        # Save this route as best route
        self.best_route = route
        self.best_route_value = route_value

        for i in range(self.no_of_iterations):
            # Choice and swap two states
            while True:
                state_a = random.choice(self.states)
                state_b = random.choice(self.states)

                if self.is_swap_legal(state_a, state_b):
                    break

            route.swap(state_a, state_b)
            self.tabu_list.append(self.TabuEntry(state_a, state_b, self.initial_cadence))

            # Evaluate route value and save it as best route if it is more valuable
            route_value = route.calculate_value()
            if route_value > self.best_route_value:
                self.best_route = route
                self.best_route_value = route_value
            else:
                self.critical_event_counter += 1

            # Lower the cadence and remove outdated tabu entries from tabu list
            self.update_tabu_list()

            # Reset the simulation if there is no better solution since last "self.critical_event" iterations
            if self.critical_event != 0 and self.critical_event_counter == self.critical_event:
                # Generate new random route
                route.generate_random(self.states)
                route_value = route.calculate_value()

                # Evaluate it and save this route as best route
                if route_value > self.best_route_value:
                    self.best_route = route
                    self.best_route_value = route_value
