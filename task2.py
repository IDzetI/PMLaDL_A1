import math
import random

# configs
file_name = "cities.csv"
temperature = 5000
city_count = 30
temperature_min = 1
cooling_rate = 0.0001


def accept_probability(energy, new_energy, temperature):
    # Если новое решение лучше, примите его
    if new_energy < energy:
        return 1.0

    # Если новое решение хуже, вычислите вероятность принятия
    return math.exp((energy - new_energy) / temperature)


def get_cities(file_name):
    file = open(file_name, encoding="utf_8_sig")
    lines = file.readlines()[1:]
    file.close()

    cities = []
    for line in lines:
        data = line.split(",")
        cities.append((float(data[17]), float(data[18]), data[6]))
    return cities


def get_distance(city_a, city_b):
    return math.sqrt((city_a[0] - city_b[0]) ** 2 + (city_a[1] - city_b[1]) ** 2)


def get_tour_distance(cities):
    dest = get_distance(cities[0], cities[-1])
    for i in range(1, len(cities)):
        dest += get_distance(cities[i - 1], cities[i])
    return dest


def swap_cities(cities, i1, i2):
    buf = cities[i1]
    cities[i1] = cities[i2]
    cities[i2] = buf
    return cities


def copy_tour(cities):
    r = []
    for c in cities:
        r.append(c)
    return r


# for c in get_cities(file_name):
#     print(c)

tour = get_cities(file_name)[:city_count]
random.shuffle(tour)

current_energy = get_tour_distance(tour)


best_tour = copy_tour(tour)
best_energy = current_energy

print("cities count:", len(tour))

print("initial tour length: ", best_energy)
result = "original tour: "
for city in best_tour:
    result += city[2] + " "
print(result)

while temperature > temperature_min:
    tour_pos1 = int(len(tour) * random.random())
    tour_pos2 = int(len(tour) * random.random())

    new_tour = swap_cities(tour, tour_pos1, tour_pos2)

    get_tour_distance(tour)

    new_energy = get_tour_distance(tour)
    if accept_probability(current_energy, new_energy, temperature):
        tour = copy_tour(new_tour)
        current_energy = new_energy

        if current_energy < best_energy:
            best_tour = copy_tour(tour)
            best_energy = current_energy

    temperature *= 1 - cooling_rate


print("result tour length: ", best_energy)
result = "result tour: "
for city in best_tour:
    result += city[2] + " "
print(result)
