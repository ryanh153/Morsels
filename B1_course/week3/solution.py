import re


def re_logtolist(data):
    result = []
    for line in data:
        values = line_parse(line)
        if values is not None:
            ip_address, timestamp, request = values
        else:
            ip_address, timestamp, request = 'No IP address found', 'No timestamp found', 'No request found'

        result.append({'ip_address': ip_address, 'timestamp': timestamp, 'request': request})

    return result


def line_parse(line):
    match = re.search(re_capture, line)
    if match is None:
        return match
    else:
        return match.group(1), match.group(2), match.group(3)


logtolist = re_logtolist
re_capture = re.compile(r'([\d.]+) - - \[([^]]+)] \"([^\"]+)\"')
