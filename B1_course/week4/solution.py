import re
import operator
from datetime import datetime


class LogDicts:
    re_capture = re.compile(r'([\d.]+) - - \[([^]]+)] \"([^\"]+)\"')
    date_format = '%d/%b/%Y:%H:%M:%S %z'

    def __init__(self, filename):
        self._dicts = self.log_to_list(open(filename, 'r'))

    def log_to_list(self, data):
        return [self.line_to_dict(line) for line in data]

    def line_to_dict(self, line):
        match = re.search(self.re_capture, line)
        if match is None:
            ip, time, request, date_time = 'No IP address found', 'No timestamp found', 'No request found',\
                                           datetime.now()
        else:
            ip, time, request, date_time = match.group(1), match.group(2), match.group(3),\
                                           datetime.strptime(match.group(2), self.date_format)

        return {'ip_address': ip, 'timestamp': time, 'request': request, 'date_time': date_time}

    def dicts(self, key=operator.itemgetter('date_time')):
        return sorted(self._dicts, key=key)

    def iterdicts(self, key=operator.itemgetter('date_time')):
        yield from sorted(self._dicts, key=key)

    def earliest(self, key=operator.itemgetter('date_time')):
        return sorted(self._dicts, key=key)[0]

    def latest(self, key=operator.itemgetter('date_time')):
        return sorted(self._dicts, key=key)[-1]

    def for_ip(self, ip, key=operator.itemgetter('ip_address')):
        return sorted([d for d in self._dicts if d['ip_address'] == ip], key=key)

    def for_request(self, request, key=operator.itemgetter('request')):
        return sorted([d for d in self._dicts if request in d['request']], key=key)
