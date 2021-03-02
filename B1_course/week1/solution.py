from collections import defaultdict, Counter


visits = defaultdict(Counter)


def collect_places():
    visits.clear()
    while True:
        loc = input('Tell me where you went: ')
        if not loc:
            break
        if loc.count(',') != 1:
            print("That's not a legal city, country combination")
            continue
        city, country = [val.strip() for val in loc.split(',')]
        visits[country.strip()][city.strip()] += 1


def display_places():
    print('You visited:')
    for country, entry in sorted(visits.items()):
        print(country)
        for city, num in sorted(entry.items()):
            num_str = f'({num})' if num > 1 else ''
            print(f'    {city} {num_str}')


if __name__ == '__main__':
    collect_places()
    display_places()