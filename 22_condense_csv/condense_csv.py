from textwrap import dedent


def condense_csv(text, id_name):
    print(text)
    lines = text.split("  ")
    for line in text:
        print(line)
        id_val, key, val = line.split(',')
        print(f"{id_name}: {id_val}, {key}: {val}")


text = dedent("""
            01,Title,Ran So Hard the Sun Went Down
            02,Title,Honky Tonk Heroes (Like Me)
        """).strip()

for c in text:
    print(c)

# condense_csv(text, "Track")