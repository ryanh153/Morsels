import re


def re_logtolist(data):
    # yield from (line_parse(line) for line in data)  # really should do this in modern python, but it doesn't pass
    return [line_to_dict(line) for line in data]


def line_to_dict(line):
    match = re.search(re_capture, line)
    if match is None:
        ip, time, request = 'No IP address found', 'No timestamp found', 'No request found'
    else:
        ip, time, request = match.group(1), match.group(2), match.group(3)
    return {'ip_address': ip, 'timestamp': time, 'request': request}


logtolist = re_logtolist
re_capture = re.compile(r'([\d.]+) - - \[([^]]+)] \"([^\"]+)\"')
