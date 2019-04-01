from prettytable import PrettyTable
import requests
import geopy.distance
import pickle


class State:
    AIRPLANE_OVERHEAD = 60  # min
    AIRPLANE_SPEED = 950  # km/h

    def __init__(self, name, capital, electoral_votes):
        self.name = name
        self.capital = capital
        self.electoral_votes = electoral_votes
        self.coordinates = None

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

    @staticmethod
    def save(states):
        file = open('states.bin', mode='wb')
        pickle.dump(states, file)
        file.close()

    @staticmethod
    def load():
        file = open('states.bin', mode='rb')
        states = pickle.load(file)
        file.close()
        return states

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
