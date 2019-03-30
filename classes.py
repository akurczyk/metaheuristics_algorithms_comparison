from prettytable import PrettyTable
import requests
import geopy.distance
import random
import math


class State:
    AIRPLANE_OVERHEAD = 60  # min
    AIRPLANE_SPEED = 950  # km/h

    def __init__(self, name, capital, electoral_votes):
        self.name = name
        self.capital = capital
        self.electoral_votes = electoral_votes
        self.coordinates = None
        self.get_coordinates()

    def __str__(self):
        return self.name + '; ' + self.capital + '; ' + str(self.electoral_votes) + '; ' + str(self.coordinates)

    @staticmethod
    def print_states(states):
        table = PrettyTable(['Name', 'Capital', 'Electoral votes', 'Latitude', 'Longitude'], header_style='upper')
        table.align = 'l'

        for state in states:
            table.add_row([
                state.name,
                state.capital,
                state.electoral_votes,
                state.coordinates[0],
                state.coordinates[1],
            ])

        print(table)

    def get_coordinates(self):
        query = self.capital + ' ' + self.name
        url = 'https://nominatim.openstreetmap.org/search?q=' + query + '&format=json&polygon=1&addressdetails=1'

        response = requests.get(url).json()
        if not response:
            return

        self.coordinates = float(response[0]['lat']), float(response[0]['lon'])

    def get_travel_time_to(self, state):
        origin = self.coordinates
        destination = state.coordinates

        if not origin or not destination:
            return None

        distance = geopy.distance.distance(origin, destination).km
        return 0 if distance == 0.0 else self.AIRPLANE_OVERHEAD + (self.AIRPLANE_SPEED / 950) * 60


class Route:
    VISIT_TIME = 60 * 4
    INITIAL_SUPPORT = 0.2

    def __init__(self, inc_support, dec_support):
        self.inc_support = inc_support
        self.dec_support = dec_support
        self.states = []

    def __str__(self):
        return ', '.join([state.capital for state in self.states])

    def print(self):
        table = PrettyTable(['#', 'Name', 'Capital'], header_style='upper')
        table.align = 'l'

        i = 1
        for state in self.states:
            table.add_row([i, state.name, state.capital])
            i += 1

        print(table)

    def generate_random(self, states):
        self.states = []
        tmp_states = states.copy()

        for i in range(len(states)):
            current_state = random.choice(tmp_states)
            self.states.append(current_state)
            tmp_states.remove(current_state)

        # while self.calculate_time() < self.TIME_LIMIT:
        #     self.states.append(random.choice(states))
        #
        # if self.calculate_time() > self.TIME_LIMIT:
        #     self.states.pop()

    # def calculate_time(self):
    #     time = 0
    #     for i in range(len(self.states)):
    #         time += self.VISIT_TIME
    #
    #         if i != len(self.states) - 1:
    #             current_state = self.states[i]
    #             next_state = self.states[i + 1]
    #             time += current_state.get_travel_time_to(next_state)
    #
    #     return time

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
            value += math.floor(states_supports[state] * state.electoral_votes)

        return value

    def swap(self, state_a, state_b):
        index_a, index_b = self.states.index(state_a), self.states.index(state_b)
        self.states[index_b], self.states[index_a] = self.states[index_a], self.states[index_b]

        # self.states = [None if state == state_a else state for state in self.states]
        # self.states = [state_a if state == state_b else state for state in self.states]
        # self.states = [state_b if not state else state for state in self.states]

    def random_swap(self):
        index_a, index_b = tuple(random.sample(range(len(self.states)), 2))
        self.states[index_b], self.states[index_a] = self.states[index_a], self.states[index_b]

    @staticmethod
    def pmx(route_a, route_b):
        parent_a = route_a.states
        parent_b = route_b.states

        random_a = random.randint(0, len(parent_a))
        random_b = random.randint(0, len(parent_a))

        begin = min(random_a, random_b)
        end = max(random_a, random_b)

        child_a = parent_a[:begin] + parent_b[begin:end] + parent_a[end:]
        child_b = parent_b[:begin] + parent_a[begin:end] + parent_b[end:]

        for i in range(len(parent_a)):
            if i < begin or i >= end:
                if child_a[i] in child_a[begin:end]:
                    pos = child_a[begin:end].index(child_a[i]) + begin
                    child_a[i] = child_b[pos]

        for i in range(len(parent_a)):
            if i < begin or i >= end:
                if child_b[i] in child_b[begin:end]:
                    pos = child_b[begin:end].index(child_b[i]) + begin
                    child_b[i] = child_a[pos]

        route_a.states = child_a
        route_b.states = child_b

        return route_a, route_b
