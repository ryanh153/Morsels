import datetime

date_format = '%d/%b/%Y:%H:%M:%S %z'
date_str = '30/Jan/2010:00:03:18 +0200'

result = datetime.datetime.strptime(date_str, date_format)
print(result)