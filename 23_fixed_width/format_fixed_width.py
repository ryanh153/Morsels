def format_fixed_width(lol, padding=2, widths=None, alignments=None):
    if not len(lol):  # if list is length zero return string of length zero
        return ""
    else:
        s = []
        if widths is None:  # if not passed widths set by max length in each column
            widths = [0 for _ in lol[0]]
            for row in lol:  # get max size for each column
                for col, el in enumerate(row):
                    if len(el) > widths[col]:
                        widths[col] = len(el)

        if alignments is None:  # if alignments not passed set all to be left
            alignments = ['L' for _ in lol[0]]

        for row in lol:  # make list of lists with padding added
            for col, el in enumerate(row):
                if alignments[col] == 'L':
                    s.append(el)
                    if col != len(row)-1:
                        s.append(" "*(widths[col]-len(el)+padding))
                else:
                    s.append(" " * (widths[col] - len(el)))
                    s.append(el)
                    if col != len(row)-1:
                        s.append(" " * padding)
            s.append("\n")

        return "".join(s[:-1])  # ignore last new line
