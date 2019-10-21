import argparse

parser = argparse.ArgumentParser()
# required arguments
parser.add_argument("source", help="source file to be converted.")
parser.add_argument("destination", help="destination file to be created.")
# optional arguments
parser.add_argument("--in-delimiter", help="delimiter in source file.", default="|")
parser.add_argument("--out-delimiter", help="delimiter in destination file.", default=",")

args = parser.parse_args()

with open(args.source, 'r') as read_from, open (args.destination, 'w') as write_to:
    for line in read_from:
        write_to.write(line.replace(args.in_delimiter,args.out_delimiter))