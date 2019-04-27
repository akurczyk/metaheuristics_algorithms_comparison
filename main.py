import click
from state import State
from random_search import RandomSearch
from local_search import LocalSearch
from tabu_search import TabuSearch
from genetic_algorithm import GeneticAlgorithm
from simulated_annealing import SimulatedAnnealing
from datetime import datetime


def inc_support(value, time):
    return min(value + 0.0033 * time, 1)


def dec_support(value, time):
    return max(value * 0.99994 ** time, 0)


def load_states():
    global states
    states = State.load()
    states = states[:10]  # !!!!!!!!!!!!

    print('All loaded states:')
    State.print_states(states)
    print()


def run_random_search(repeats):
    print('Running Random Search algoritm with ' + str(repeats) + ' repeats...')
    print()

    rs = RandomSearch(states, repeats, inc_support, dec_support)
    rs.run()
    print('Found optimal route with value of ' + str(rs.best_solution.value) + '.')
    print(str(rs.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    rs.best_solution.print()
    print()


def run_local_search(repeats):
    print('Running Local Search algoritm with ' + str(repeats) + ' repeats...')
    print()

    ls = LocalSearch(states, repeats, inc_support, dec_support)
    ls.run()
    print('Found optimal route with value of ' + str(ls.best_solution.value) + '.')
    print(str(ls.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    ls.best_solution.print()
    print()


def run_tabu_search(repeats, initial_cadence, critical_event):
    print('Running Tabu Search with ' + str(repeats) + ' repeats...')
    print()

    ts = TabuSearch(states, repeats, initial_cadence, critical_event, inc_support, dec_support)
    ts.run()
    print('Found optimal route with value of ' + str(ts.best_solution.value) + '.')
    print(str(ts.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    ts.best_solution.print()
    print()


def run_genetic_algorithm(repeats, population_size):
    print('Running Genetic Algorithm with ' + str(repeats) + ' repeats...')
    print()

    ga = GeneticAlgorithm(states, repeats, population_size, inc_support, dec_support)
    ga.run()
    print('Found optimal route with value of ' + str(ga.best_solution.value) + '.')
    print(str(ga.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    ga.best_solution.print()
    print()


def run_simulated_annealing(repeats, initial_temperature, cooling_coefficient):
    print('Running Simulated Annealing with ' + str(repeats) + ' repeats...')
    print()

    sa = SimulatedAnnealing(states, repeats, initial_temperature, cooling_coefficient, inc_support, dec_support)
    sa.run()
    print('Found optimal route with value of ' + str(sa.best_solution.value) + '.')
    print(str(sa.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    sa.best_solution.print()
    print()


def benchmark():
    for i in [10, 50, 100, 500, 1000]:
        v = 0
        time_s = datetime.now()
        for k in range(10):
            rs = RandomSearch(states, i, inc_support, dec_support)
            rs.run()
            v += rs.best_solution.value
        time_e = datetime.now()
        tt = (time_e - time_s).total_seconds() / 1
        print('Random Search, ' + str(i) + ', -, ' + str(v/10) + ', ' + str(tt))

    for i in [10, 50, 100, 500, 1000, 5000]:
        for j in [10, 25, 50]:
            v = 0
            time_s = datetime.now()
            for k in range(10):
                ga = GeneticAlgorithm(states, i, j, inc_support, dec_support)
                ga.run()
                v += ga.best_solution.value
            time_e = datetime.now()
            tt = (time_e - time_s).total_seconds() / 1
            print('Genetic Algorithm, ' + str(i) + ', ' + str(j) + ', ' + str(v/10) + ', ' + str(tt))


@click.command()
@click.argument('action', type=click.Choice(['rs', 'ls', 'ts', 'ga', 'sa', 'benchmark']))
# TODO: Zamienić repeats na czas pracy
@click.option('--repeats', default=10, type=int)
@click.option('--population_size', default=20, type=int)
@click.option('--initial_cadence', default=20, type=int)
@click.option('--critical_event', default=20, type=int)
@click.option('--initial_temperature', default=1000, type=int)
@click.option('--cooling_coefficient', default=0.999, type=float)
@click.option('--minimal_temperature', default=1, type=int)
def command(action, repeats, population_size, initial_cadence, critical_event, initial_temperature,
            cooling_coefficient, minimal_temperature):
    load_states()

    if action == 'rs':
        run_random_search(repeats)
    elif action == 'ls':
        run_local_search(repeats)
    elif action == 'ts':
        run_tabu_search(repeats, initial_cadence, critical_event)
    elif action == 'ga':
        run_genetic_algorithm(repeats, population_size)
    elif action == 'sa':
        run_simulated_annealing(initial_temperature, cooling_coefficient, minimal_temperature)
    elif action == 'benchmark':
        benchmark()


if __name__ == '__main__':
    command()
