import csv

def load_map_csv(path):
    grid = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            grid.append([int(cell) for cell in row])
    return grid