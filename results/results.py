import csv
import numpy as np
import matplotlib.pyplot as plt


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


def generate_chart(title, filename, rows):
    labels = [row[0] for row in rows]
    results = [row[1] for row in rows]
    index = np.arange(len(labels))

    width = 11.69-1.97
    height = (16.53-1.97)-0.39 if len(rows) > 20 else ((16.53-1.97)/2)-0.39

    plt.figure(figsize=(width, height), dpi=300)
    plt.barh(index, results)
    plt.xlabel('Wynik')
    plt.ylabel('Parametry')
    plt.yticks(index, labels)
    plt.xlim(200, 400)
    plt.title(title)

    plt.savefig(filename)


if __name__ == '__main__':
    for no_of_cities in [51]:
        data = import_data(f'results/{no_of_cities}.csv')
        for chart_name in data:
            generate_chart(
                f'{no_of_cities} miast: {chart_name}',
                f'results/charts/{chart_name} {no_of_cities}.png',
                data[chart_name]
            )
