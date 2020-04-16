def format_fixed_width(rows, padding=2, widths=None, alignments=None):
    if not len(rows):  # if list is length zero return string of length zero
        s = ""
    else:
        if widths is None:  # if not passed widths set by max length in each column
            widths = [max(len(el) for el in col) for col in zip(*rows)]

        if alignments is None:  # if alignments not passed set all to be left
            alignments = [str.ljust for _ in rows[0]]
        else:
            alignments = [str.ljust if alignment == "L" else str.rjust for alignment in alignments]

        joiner = " "*padding
        s = "\n".join(
            joiner.join(alignment(el, width) for el, width, alignment in zip(row, widths, alignments)).rstrip()
            for row in rows)
    return s
