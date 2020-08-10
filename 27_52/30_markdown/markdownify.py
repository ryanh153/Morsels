import re

WHITESPACE_RE = re.compile(r"\s+")
LINEBREAK_RE = re.compile(r"<br>")
STRONG_RE = re.compile(r"</?strong>")
LINK_RE = re.compile(r'<a href="(.*?)">(.*?)</a>')
PARAGRAPH_RE = re.compile(r"</?p>")


def markdownify(text):
    text = WHITESPACE_RE.sub(" ", text)  # replace one or more spaces/new lines with one whitespace character
    text = PARAGRAPH_RE.sub("\n", text)  # replace start/end paragraph tags with one new line each
    text = LINEBREAK_RE.sub("  \n", text)  # <br> tag means two spaces followed by a new line
    text = STRONG_RE.sub("**", text)  # opening or closing <strong> tag with "**"
    text = LINK_RE.sub(r"[\2](\1)", text)  # get the hyperlink and name strings
    return text.strip()
