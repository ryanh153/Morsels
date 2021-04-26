from collections import defaultdict


class TableFull(Exception):
    pass


class Person:
    def __init__(self, first, last):
        self.first, self.last = first, last


class GuestList:
    max_at_table = 10

    def __init__(self):
        self.seating_map = defaultdict(list)

    def assign(self, person, table):
        if len(self.table(table)) >= self.max_at_table:
            raise TableFull
        self.move_if_seated(person)

        self.seating_map[table].append(person)

    def move_if_seated(self, person):
        current_seat = self.get_table(person)
        if current_seat is not None:
            self.seating_map[current_seat].remove(person)

    def get_table(self, person):
        for table, guests in self.seating_map.items():
            if person in guests:
                return table
        return None

    def table(self, query_table):
        return [person for person in self.seating_map[query_table]]

    def spaces_at_table(self, table):
        return self.max_at_table - len(self.seating_map[table])

    def guests(self):
        return [person for one_table in self.seating_map.values() for person in one_table]

    def free_space(self):
        return {table: self.spaces_at_table(table) for table in self.seating_map.keys()}

    def unassigned(self):
        return [person for person in self.seating_map[None]]

    def __len__(self):
        return len([person for one_table in self.seating_map.values() for person in one_table])

    def __repr__(self):
        result = []
        for table, table_guests in sorted(self.seating_map.items(), key=lambda x: x[0] or -1):
            result.append(f'{table}\n')
            for person in sorted(table_guests, key=lambda x: (x.last, x.first)):
                result.append(f'\t{person.last}, {person.first}\n')

        return ''.join(result)
