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

    if len(rows) > 20:
        plt.figure(figsize=(width, height), dpi=150)
        plt.barh(index, results)
        plt.xlabel('Osiągnięty rezultat wyborczy (funkcja ciągła)')
        if ' ' in rows[0][0][:-1]:
            plt.ylabel('Parametry')
        else:
            plt.ylabel('Czas obliczeń (w sekundach)')
        plt.yticks(index, labels)
        plt.xlim(0, 400)
        plt.title(title)
        plt.subplots_adjust(left=0.25)

        plt.savefig(filename)
    else:
        plt.figure(figsize=(width, height), dpi=150)
        plt.bar(index, results)
        plt.ylabel('Średni osiągnięty rezultat wyborczy (funkcja ciągła)')
        if ' ' in rows[0][0][:-1]:
            plt.xlabel('Parametry')
        else:
            plt.xlabel('Czas obliczeń (w sekundach)')
        plt.xticks(index, labels, rotation='vertical')
        plt.ylim(0, 400)
        plt.title(title)
        plt.subplots_adjust(bottom=0.25)

        plt.savefig(filename)


def generate_time_chart(title, filename, rows):
    labels = [row[0] for row in rows]
    results = [row[2] for row in rows]
    index = np.arange(len(labels))

    width = 11.69-1.97
    height = (16.53-1.97)-0.39 if len(rows) > 20 else ((16.53-1.97)/2)-0.39

    plt.figure(figsize=(width, height), dpi=150)
    plt.barh(index, results)
    plt.xlabel('Czas obliczeń (w sekundach)')
    plt.ylabel('Parametry')
    plt.yticks(index, labels)
    plt.title(title)
    plt.subplots_adjust(left=0.25)

    plt.savefig(filename)


if __name__ == '__main__':
    for no_of_cities in [25, 51]:
        data = import_data(f'results/{no_of_cities}.csv')
        for chart_name in data:
            generate_chart(
                f'{no_of_cities} miast: {chart_name}',
                f'results/charts/{chart_name} {no_of_cities}.png',
                data[chart_name]
            )

            if chart_name == 'Simulated Annealing':
                generate_time_chart(
                    f'{no_of_cities} miast: {chart_name}',
                    f'results/charts/{chart_name} {no_of_cities} Time.png',
                    data[chart_name]
                )
