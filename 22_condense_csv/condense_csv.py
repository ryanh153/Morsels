from io import StringIO
import csv


def condense_csv(text, id_name=None):
    groups = {}
    reader = csv.reader(text.splitlines())
    if id_name is None:
        [id_name, *_] = next(reader)
    headers = {id_name: None}
    for line in reader:
        identifier, attribute, value = line
        if identifier not in groups.keys():
            groups[identifier] = {id_name: identifier}
        headers[attribute] = None
        groups[identifier][attribute] = value
    out_file = StringIO()
    writer = csv.DictWriter(out_file, fieldnames=headers.keys())
    writer.writeheader()
    writer.writerows(list(groups.values()))

    return out_file.getvalue()
