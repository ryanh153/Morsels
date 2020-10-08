class PiecewiseRange:
    def __init__(self, range_str):
        self.range_str = range_str
        segments = range_str.split(',')
        self.ranges = []
        for segment in segments:
            if '-' in segment:
                val_str = segment.split('-')
                start, stop = int(val_str[0]), int(val_str[1])+1
                new_range = range(start, stop)
            else:
                new_range = range(int(segment), int(segment)+1)
            if self.ranges and self.ranges[-1].stop == new_range.start:
                self.ranges[-1] = range(self.ranges[-1].start, new_range.stop)
            else:
                self.ranges.append(new_range)

        range_str = ""
        for r in self.ranges:
            if len(r) == 1:
                range_str += f'{r.start}, '
            else:
                range_str += f'{r.start}-{r.stop-1}, '
        self.range_str = range_str[0:-2]

        self.length = sum(len(sub_range) for sub_range in self.ranges)

    def __iter__(self):
        for sub_range in self.ranges:
            yield from sub_range

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if index < 0:
            index += len(self)
        if index >= len(self):
            raise IndexError("Index is out of range")
        for sub_range in self.ranges:
            if index >= len(sub_range):
                index -= len(sub_range)
            else:
                return sub_range[index]

    def __repr__(self):
        return f'PiecewiseRange({repr(self.range_str)})'

    def __eq__(self, other):
        if isinstance(other, PiecewiseRange):
            return repr(self) == repr(other)
        return NotImplemented


r = PiecewiseRange('1-2, 4, 8-10, 11')
print(list(r))
print(r)
q = PiecewiseRange('1-2, 4, 8-11')
print(r == q)
