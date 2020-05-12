import re


def markdownify(text):
    text = re.sub(r"[ \n]+", " ", text)  # replace one or more spaces/new lines with one whitespace character
    text = re.sub(r"<br>", "  \n", text)  # <br> tag means two spaces followed by a new line
    text = re.sub(r"</*strong>", "**", text)  # opening or closing <strong> tag with "**"
    link_re = re.compile(r'<a href="([^"]+)">([^<]+)</a>')
    matches = link_re.findall(text)  # get the hyperlink and name strings
    for match in matches:  # replace each one sequentially
        text = link_re.sub(f"[{match[1]}]({match[0]})", text, count=1)
    text = re.sub(r"<p>", "", re.sub(r"</p>", "\n\n", text)).rstrip()  # two new lines after paragraph (except last)
    return text