from route import Route
import copy
import datetime


class TabuSearch:
    def __init__(self, states, seconds, initial_cadence, critical_event, inc_support, dec_support):
        self.states = states
        self.seconds = seconds
        self.initial_cadence = initial_cadence
        self.critical_event = critical_event
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.critical_event_counter = 0
        self.best_solution = self.Solution(self.inc_support, self.dec_support)
        self.best_solution.calculate_value()
        self.tabu_list = []

    class Solution(Route):
        def __init__(self, inc_support, dec_support):
            super().__init__(inc_support, dec_support)

        def swap(self, state_a, state_b):
            index_a, index_b = self.states.index(state_a), self.states.index(state_b)
            self.states[index_b], self.states[index_a] = self.states[index_a], self.states[index_b]

    class TabuEntry:
        def __init__(self, state_a, state_b, cadence):
            self.state_a = state_a
            self.state_b = state_b
            self.cadence = cadence

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
        solution = self.Solution(self.inc_support, self.dec_support)
        solution.generate_random(self.states)
        solution.calculate_value()

        # Save this route as best route
        self.best_solution = solution

        finish = datetime.datetime.now() + datetime.timedelta(seconds=self.seconds)
        while datetime.datetime.now() < finish:
            # Choice best move regarding the tabu list
            tmp_best_solution = self.Solution(self.inc_support, self.dec_support)
            best_i, best_j = None, None

            for i in self.states:
                for j in self.states:
                    if self.is_swap_legal(i, j):
                        tmp_solution = copy.deepcopy(solution)
                        tmp_solution.swap(i, j)
                        tmp_solution.calculate_value()
                        if tmp_solution.value > tmp_best_solution.value:
                            tmp_best_solution = tmp_solution
                            best_i, best_j = i, j

            solution = tmp_best_solution
            self.tabu_list.append(self.TabuEntry(best_i, best_j, self.initial_cadence))

            # Evaluate route value and save it as best route if it is more valuable
            solution.calculate_value()
            if solution.value > self.best_solution.value:
                self.best_solution = copy.copy(solution)
            else:
                self.critical_event_counter += 1

            # Lower the cadence and remove outdated tabu entries from tabu list
            self.update_tabu_list()

            # Reset the simulation if there is no better solution since last "self.critical_event" iterations
            if self.critical_event != 0 and self.critical_event_counter == self.critical_event:
                # Generate new random route
                solution.generate_random(self.states)
                solution.calculate_value()

                # Evaluate it and save this route as best route
                if solution.value > self.best_solution.value:
                    self.best_solution = solution
