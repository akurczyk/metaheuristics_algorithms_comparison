import click
from state import State
from random_search import RandomSearch
from genetic_algorithm import GeneticAlgorithm
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


def run_random_search(repeats):
    print('Running Random Search algoritm with ' + str(repeats) + ' repeats...')
    print()

    rs = RandomSearch(states, repeats, inc_support, dec_support)
    rs.run()
    print('Found optimal route with value of ' + str(rs.best_solution.value) + ' electoral votes:')
    rs.best_solution.print()
    print()


def run_genetic_algorithm(repeats, population_size):
    print('Running Genetic Algorithm with ' + str(repeats) + ' repeats...')
    print()

    ts = GeneticAlgorithm(states, repeats, population_size, inc_support, dec_support)
    ts.run()
    print('Found optimal route with value of ' + str(ts.best_solution.value) + ' electoral votes:')
    ts.best_solution.print()
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
@click.argument('action', type=click.Choice(['rs', 'ga', 'benchmark']))
@click.option('--repeats', default=10, type=int)
@click.option('--population_size', default=20, type=int)
def command(action, repeats, population_size):
    load_states()

    if action == 'rs':
        run_random_search(repeats)
    elif action == 'ga':
        run_genetic_algorithm(repeats, population_size)
    elif action == 'benchmark':
        benchmark()


if __name__ == '__main__':
    command()
