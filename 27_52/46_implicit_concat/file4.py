import re

pattern = re.compile(
    r"implicit\n"
    u"line continuation"
)
m = pattern.search("""
implicit
"""
'line continuation')
print('match' if m else 'no match')