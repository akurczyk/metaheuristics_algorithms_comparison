from prettytable import PrettyTable
import random
import math


class Route:
    VISIT_TIME = 60 * 4
    INITIAL_SUPPORT = 0.2

    def __init__(self, inc_support, dec_support):
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.states = []
        self.value = 0

    def __str__(self):
        return ', '.join([state.capital for state in self.states])

    def print(self):
        table = PrettyTable(['#', 'Name', 'Capital', 'All electoral votes'], header_style='upper')
        table.align = 'l'

        i = 1
        for state in self.states:
            table.add_row([i, state.name, state.capital, state.electoral_votes])
            i += 1

        print(table)

    def generate_random(self, states):
        self.states = []
        tmp_states = states.copy()

        for i in range(len(states)):
            current_state = random.choice(tmp_states)
            self.states.append(current_state)
            tmp_states.remove(current_state)

    def calculate_value(self):
        def dec_support(states_supports, time, excluded_state=None):
            for state in states_supports:
                if state != excluded_state:
                    states_supports[state] = self.dec_support(states_supports[state], time)

        states_supports = {}
        for state in self.states:
            states_supports[state] = self.INITIAL_SUPPORT

        for i in range(len(self.states)):
            state = self.states[i]

            dec_support(states_supports, self.VISIT_TIME, state)
            states_supports[state] = self.inc_support(states_supports[state], self.VISIT_TIME)

            if i != len(self.states) - 1:
                next_state = self.states[i + 1]
                travel_time = state.get_travel_time_to(next_state)
                dec_support(states_supports, travel_time)

        value = 0
        for state in states_supports:
            value += states_supports[state] * state.electoral_votes

        self.value = value

    def calculate_real_value(self):
        def dec_support(states_supports, time, excluded_state=None):
            for state in states_supports:
                if state != excluded_state:
                    states_supports[state] = self.dec_support(states_supports[state], time)

        states_supports = {}
        for state in self.states:
            states_supports[state] = self.INITIAL_SUPPORT

        for i in range(len(self.states)):
            state = self.states[i]

            dec_support(states_supports, self.VISIT_TIME, state)
            states_supports[state] = self.inc_support(states_supports[state], self.VISIT_TIME)

            if i != len(self.states) - 1:
                next_state = self.states[i + 1]
                travel_time = state.get_travel_time_to(next_state)
                dec_support(states_supports, travel_time)

        value = 0
        for state in states_supports:
            if states_supports[state] > 0.5:
                value += state.electoral_votes

        return value
