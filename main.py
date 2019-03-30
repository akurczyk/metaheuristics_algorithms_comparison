import click
from data import states
from classes import State
from random_search import RandomSearch
from tabu_search import TabuSearch
from genetic_algorithm import GeneticAlgorithm
from datetime import datetime


def inc_support(value, time):
    return min(value + 0.0033 * time, 1)


def dec_support(value, time):
    return max(value * 0.99994 ** time, 0)


def print_loaded_states():
    print('All loaded states with coordinates downloaded from OpenStreetMap:')
    State.print_states(states)
    print()


def run_random_search(repeats):
    print('Running Random Search algoritm with ' + str(repeats) + ' repeats...')
    print()

    rs = RandomSearch(states, repeats, inc_support, dec_support)
    rs.run()
    print('Found optimal route with value of ' + str(rs.best_route_value) + ' electoral votes:')
    rs.best_route.print()
    print()


def run_tabu_search(repeats, initial_cadence, critical_event):
    print('Running Tabu Search algoritm with ' + str(repeats) + ' repeats...')
    print()

    ts = TabuSearch(states, repeats, initial_cadence, critical_event, inc_support, dec_support)
    ts.run()
    print('Found optimal route with value of ' + str(ts.best_route_value) + ' electoral votes:')
    ts.best_route.print()
    print()


def run_genetic_algorithm(repeats, population_size):
    print('Running Genetic Algorithm with ' + str(repeats) + ' repeats...')
    print()

    ts = GeneticAlgorithm(states, repeats, population_size, inc_support, dec_support)
    ts.run()
    print('Found optimal route with value of ' + str(ts.best_route_value) + ' electoral votes:')
    ts.best_route.print()
    print()


def benchmark():
    for i in [10, 50, 100, 500, 1000]:
        v = 0
        time_s = datetime.now()
        for k in range(10):
            rs = RandomSearch(states, i, inc_support, dec_support)
            rs.run()
            v += rs.best_route_value
        time_e = datetime.now()
        tt = (time_e - time_s).total_seconds() / 1
        print('Random Search, ' + str(i) + ', -, ' + str(v/10) + ', ' + str(tt))

    for i in [10, 50, 100, 500, 1000, 5000]:
        for j in [10, 25, 50]:
            v = 0
            time_s = datetime.now()
            for k in range(10):
                ts = TabuSearch(states, i, j, 20, inc_support, dec_support)
                ts.run()
                v += ts.best_route_value
            time_e = datetime.now()
            tt = (time_e - time_s).total_seconds() / 1
            print('Tabu Search, ' + str(i) + ', ' + str(j) + ', ' + str(v/10) + ', ' + str(tt))

    for i in [10, 50, 100, 500, 1000, 5000]:
        for j in [10, 25, 50]:
            v = 0
            time_s = datetime.now()
            for k in range(10):
                ga = GeneticAlgorithm(states, i, j, inc_support, dec_support)
                ga.run()
                v += ga.best_route_value
            time_e = datetime.now()
            tt = (time_e - time_s).total_seconds() / 1
            print('Genetic Algorithm, ' + str(i) + ', ' + str(j) + ', ' + str(v/10) + ', ' + str(tt))


@click.command()
@click.argument('action', type=click.Choice(['rs', 'ts', 'ga', 'benchmark']))
@click.option('--repeats', default=10, type=int)
@click.option('--initial_cadence', default=10, type=int)
@click.option('--critical_event', default=20, type=int)
@click.option('--population_size', default=20, type=int)
def command(action, repeats, initial_cadence, critical_event, population_size):
    print_loaded_states()

    if action == 'rs':
        run_random_search(repeats)
    elif action == 'ts':
        run_tabu_search(repeats, initial_cadence, critical_event)
    elif action == 'ga':
        run_genetic_algorithm(repeats, population_size)
    elif action == 'benchmark':
        benchmark()


if __name__ == '__main__':
    command()
