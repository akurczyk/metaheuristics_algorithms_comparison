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

    print('All loaded states:')
    State.print_states(states)
    print()


def run_random_search(seconds):
    print('Running Random Search algoritm for ' + str(seconds) + ' seconds...')
    print()

    rs = RandomSearch(states, seconds, inc_support, dec_support)
    rs.run()
    print('Found optimal route with value of ' + str(rs.best_solution.value) + '.')
    print(str(rs.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    rs.best_solution.print()
    print()


def run_local_search(seconds):
    print('Running Local Search algoritm for ' + str(seconds) + ' seconds...')
    print()

    ls = LocalSearch(states, seconds, inc_support, dec_support)
    ls.run()
    print('Found optimal route with value of ' + str(ls.best_solution.value) + '.')
    print(str(ls.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    ls.best_solution.print()
    print()


def run_tabu_search(seconds, initial_cadence, critical_event):
    print('Running Tabu Search for ' + str(seconds) + ' seconds...')
    print()

    ts = TabuSearch(states, seconds, initial_cadence, critical_event, inc_support, dec_support)
    ts.run()
    print('Found optimal route with value of ' + str(ts.best_solution.value) + '.')
    print(str(ts.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    ts.best_solution.print()
    print()


def run_genetic_algorithm(seconds, population_size, crossover, mutate):
    print('Running Genetic Algorithm for ' + str(seconds) + ' seconds...')
    print()

    ga = GeneticAlgorithm(states, seconds, population_size, crossover, mutate, inc_support, dec_support)
    ga.run()
    print('Found optimal route with value of ' + str(ga.best_solution.value) + '.')
    print(str(ga.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    ga.best_solution.print()
    print()


def run_simulated_annealing(initial_temperature, cooling_coefficient, minimal_temperature):
    print('Running Simulated Annealing...')
    print()

    sa = SimulatedAnnealing(states, initial_temperature, cooling_coefficient, minimal_temperature,
                            inc_support, dec_support)
    sa.run()
    print('Found optimal route with value of ' + str(sa.best_solution.value) + '.')
    print(str(sa.best_solution.calculate_real_value()) + ' electoral votes were collected.')
    sa.best_solution.print()
    print()


def print_csv(*args):
    print(*args, sep=', ')


def benchmark():
    REPEATS = 2
    SECONDS = [60, 300, 1200]

    #for seconds in SECONDS:
    #    v = 0
    #    time_s = datetime.now()
    #    for k in range(REPEATS):
    #        rs = RandomSearch(states, seconds, inc_support, dec_support)
    #        rs.run()
    #        v += rs.best_solution.value
    #    time_e = datetime.now()
    #    tt = (time_e - time_s).total_seconds()
    #    print_csv('Random Search',
    #              str(seconds), '-',
    #              str(v/REPEATS), str(tt/REPEATS))

    #for seconds in SECONDS:
    #    v = 0
    #    time_s = datetime.now()
    #    for k in range(REPEATS):
    #        ls = LocalSearch(states, seconds, inc_support, dec_support)
    #        ls.run()
    #        v += ls.best_solution.value
    #    time_e = datetime.now()
    #    tt = (time_e - time_s).total_seconds()
    #    print_csv('Local Search',
    #              str(seconds), '-',
    #              str(v/REPEATS), str(tt/REPEATS))

    #for seconds in SECONDS:
    #    for initial_cadence in [10, 25, 50]:
    #        for critical_event in [10, 25, 50]:
    #            v = 0
    #            time_s = datetime.now()
    #            for k in range(REPEATS):
    #                ts = TabuSearch(states, seconds, initial_cadence, critical_event, inc_support, dec_support)
    #                ts.run()
    #                v += ts.best_solution.value
    #            time_e = datetime.now()
    #            tt = (time_e - time_s).total_seconds()
    #            print_csv('Tabu Search',
    #                      str(seconds), str(initial_cadence), str(critical_event),
    #                      str(v/REPEATS), str(tt/REPEATS))

    for crossover in ['pmx', 'ox']:
        for mutate in ['transposition', 'insertion', 'inversion']:
            for seconds in SECONDS:
                for population_size in [10, 25, 50]:
                    v = 0
                    time_s = datetime.now()
                    for k in range(REPEATS):
                        ga = GeneticAlgorithm(states, seconds, population_size, crossover, mutate,
                                              inc_support, dec_support)
                        ga.run()
                        v += ga.best_solution.value
                    time_e = datetime.now()
                    tt = (time_e - time_s).total_seconds()
                    print_csv('Genetic Algorithm ' + crossover + ' ' + mutate,
                              str(seconds), str(population_size),
                              str(v/REPEATS), str(tt/REPEATS))

    for initial_temperature in [100, 500, 1000]:
        for cooling_coefficient in [0.9, 0.99, 0.999, 0.9999]:
            for minimal_temperature in [initial_temperature * 0.25,
                                        initial_temperature * 0.5,
                                        initial_temperature * 0.75]:
                v = 0
                time_s = datetime.now()
                for k in range(REPEATS):
                    sa = SimulatedAnnealing(states, initial_temperature, cooling_coefficient, minimal_temperature,
                                            inc_support, dec_support)
                    sa.run()
                    v += sa.best_solution.value
                time_e = datetime.now()
                tt = (time_e - time_s).total_seconds()
                print_csv('Simulated Annealing',
                          str(initial_temperature), str(cooling_coefficient), str(minimal_temperature),
                          str(v/REPEATS), str(tt/REPEATS))


@click.command()
@click.argument('action', type=click.Choice(['rs', 'ls', 'ts', 'ga', 'sa', 'benchmark']))
@click.option('--seconds', default=20, type=int)
@click.option('--crossover', default='pmx', type=click.Choice(['pmx', 'ox']))
@click.option('--mutate', default='transposition', type=click.Choice(['transposition', 'insertion', 'inversion']))
@click.option('--population_size', default=20, type=int)
@click.option('--initial_cadence', default=20, type=int)
@click.option('--critical_event', default=20, type=int)
@click.option('--initial_temperature', default=1000, type=int)
@click.option('--cooling_coefficient', default=0.999, type=float)
@click.option('--minimal_temperature', default=1, type=int)
def command(action, seconds, crossover, mutate, population_size, initial_cadence, critical_event, initial_temperature,
            cooling_coefficient, minimal_temperature):
    load_states()

    if action == 'rs':
        run_random_search(seconds)
    elif action == 'ls':
        run_local_search(seconds)
    elif action == 'ts':
        run_tabu_search(seconds, initial_cadence, critical_event)
    elif action == 'ga':
        run_genetic_algorithm(seconds, population_size, crossover, mutate)
    elif action == 'sa':
        run_simulated_annealing(initial_temperature, cooling_coefficient, minimal_temperature)
    elif action == 'benchmark':
        benchmark()


if __name__ == '__main__':
    command()
