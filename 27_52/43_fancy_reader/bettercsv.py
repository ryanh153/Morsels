from csv import reader


class FancyReader:
    def __init__(self, str_iter, fieldnames=None):
        self.str_iter = iter(str_iter)
        if fieldnames is None:
            self.fieldnames = [name for name in list(reader([next(self.str_iter)], delimiter=',', quotechar='"'))[0]]
            self.line_num = 1
        else:
            self.fieldnames = fieldnames
            self.line_num = 0

    def __next__(self):
        self.line_num += 1
        return FancyLine(next(self.str_iter), self.fieldnames)

    def __iter__(self):
        return self


class FancyLine:
    def __init__(self, csv_str, fieldnames=None):
        line_data = list(reader([csv_str], delimiter=',', quotechar='"'))[0]
        if len(line_data) != len(fieldnames):
            raise ValueError(f'Must have the same number of entries as header names in each row\n'
                             f'line_data: {line_data}\n'
                             f'fieldnames: {fieldnames}')
        self.data = list(zip(line_data, fieldnames))
        self.index = 0

    def __getattr__(self, item):
        for value, name in self.data:
            if name == item:
                return value

    def __next__(self):
        if self.index < len(self.data):
            self.index += 1
            return self.data[self.index - 1][0]
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def __repr__(self):
        entries = ['='.join([name, repr(val)]) for val, name in self.data]
        inner_str = ", ".join(entries)
        return f"Row({inner_str})"


lines = ['my,fake,file', 'has,two,rows']
f_reader = FancyReader(lines, fieldnames=['w1', 'w2', 'w3'])
for row in f_reader:
    print(row)
    w1, w2, w3 = row
    print(w2)
    print(row.w1, row.w2, row.w3)
    print(f_reader.line_num)
    print()
