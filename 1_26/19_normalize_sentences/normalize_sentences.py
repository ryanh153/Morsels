import re

# [^A-Z]{3} catches Dr. Mr. and Mrs. as not being the ends of sentences
EOS = r"[^A-Z]{3}[.?!] [A-Z]"


def normalize_sentences(text):
    """Normalize test so all sentences end in two spaces."""
    result = []
    for i, c in enumerate(text):
        result.append(c)
        if i > 2 and i+2 < len(text) and re.match(EOS, text[i-3:i+3]):
            result.append(' ')

    return "".join(result)
