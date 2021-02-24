from collections import defaultdict


global visits


def collect_places():
    global visits
    visits = defaultdict(dict)
    while True:
        loc = input('Tell me where you went: ')
        if loc == '':
            break
        if loc.count(',') != 1:
            print("That's not a legal city, country combination")
        else:
            city, country = [val.strip() for val in loc.split(',')]
            country_entry = visits[country]
            if city not in country_entry:
                country_entry.update({city: 1})
            else:
                country_entry[city] += 1


def display_places():
    global visits
    sort_visits()
    print('You visited:')
    for country in visits:
        print(country)
        for city in visits[country]:
            if visits[country][city] == 1:
                print(f'    {city}')
            else:
                print(f'    {city} ({visits[country][city]})')


def sort_visits():
    global visits
    visits = {k: v for k, v in sorted(visits.items())}
    for entry in visits:
        visits[entry] = {k: v for k, v in sorted(visits[entry].items())}
