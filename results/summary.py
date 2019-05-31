import csv
import numpy as np
import matplotlib.pyplot as plt
import sys


def import_data(location):
    data = {}

    file = open(location)
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        algorithm = row[0].strip()
        category = ' '.join([cell.strip() if cell.strip() != '-' else '' for cell in row[1:-2]])
        value = float(row[-2].strip())
        time = float(row[-1].strip())

        if not algorithm in data:
            data[algorithm] = []

        data[algorithm].append((category, value, time))

    return data


def get_summary_data():
    all_the_data = {}
    all_the_data[25] = {}
    all_the_data[51] = {}

    summary_data = {}
    summary_data[25] = {}
    summary_data[51] = {}

    for no_of_cities in [25, 51]:
        data = import_data(f'results/{no_of_cities}.csv')

        for algorithm in data:
            if algorithm == 'Simulated Annealing':
                continue

            fixed_algorithm_name = ' '.join(algorithm.split(' ')[0:2])

            for row in data[algorithm]:
                time = int(row[0].split(' ')[0])

                if time not in all_the_data[no_of_cities]:
                    all_the_data[no_of_cities][time] = {}
                    summary_data[no_of_cities][time] = {}

                if fixed_algorithm_name not in all_the_data[no_of_cities][time]:
                    all_the_data[no_of_cities][time][fixed_algorithm_name] = []
                    summary_data[no_of_cities][time][fixed_algorithm_name] = {}

                all_the_data[no_of_cities][time][fixed_algorithm_name].append(row)

            for time in summary_data[no_of_cities]:
                summary_data[no_of_cities][time][fixed_algorithm_name]['worst'] = 1000
                summary_data[no_of_cities][time][fixed_algorithm_name]['best'] = 0

                for row in all_the_data[no_of_cities][time][fixed_algorithm_name]:
                    if row[1] < summary_data[no_of_cities][time][fixed_algorithm_name]['worst']:
                        summary_data[no_of_cities][time][fixed_algorithm_name]['worst'] = row[1]

                    if row[1] > summary_data[no_of_cities][time][fixed_algorithm_name]['best']:
                        summary_data[no_of_cities][time][fixed_algorithm_name]['best'] = row[1]

    return summary_data


def generate_chart(title, filename, rows):
    labels = []
    for time in rows:
        for algorithm in rows[time]:
            labels.insert(0, f'{time} {algorithm}')

    results_worst = []
    for time in rows:
        for algorithm in rows[time]:
            results_worst.insert(0, rows[time][algorithm]['worst'])

    results_best = []
    for time in rows:
        for algorithm in rows[time]:
            results_best.insert(0, rows[time][algorithm]['best'])

    index = np.arange(len(labels))

    width = 11.69-1.97
    height = (16.53-1.97)-0.39 if len(rows) > 20 else ((16.53-1.97)/2)-0.39

    plt.figure(figsize=(width, height), dpi=300)
    plt.barh(index, results_best, color='#2AA5F7')
    plt.barh(index, results_worst, color='#1E78B4')
    plt.xlabel('Wynik')
    plt.ylabel('Parametry')
    plt.yticks(index, labels)
    plt.xlim(0, 400)
    plt.title(title)
    plt.subplots_adjust(left=0.25)

    plt.savefig(filename)


if __name__ == '__main__':
    data = get_summary_data()

    for no_of_cities in data:
        generate_chart(
            f'Podsumowanie: {no_of_cities} miast',
            f'results/charts/Summary {no_of_cities}.png',
            data[no_of_cities]
        )
