# """This is the version that I think is the cleanest. To do bonus two though some things have to be messed up (below)"""
# import csv
# import argparse
#
# parser = argparse.ArgumentParser()
# # positional
# parser.add_argument("old_filename", help="Source file path")
# parser.add_argument("new_filename", help="Destination path (doesn't have to exist)")
# # optional
# parser.add_argument("--in-delimiter", dest="delim", help="Delimiter in source file", default="|")
# parser.add_argument("--in-quote", dest="quote", help="Quote in source file", default='"')
#
# args = parser.parse_args()
# if args.new_filename == args.old_filename:
#     raise ValueError("Source and destination file are the same location. Don't read and write from/to the same place!")
#
# with open(args.old_filename, 'r', newline='') as source, open(args.new_filename, 'w', newline='') as dest:
#     reader = csv.reader(source, delimiter=args.delim, quotechar=args.quote)
#     writer = csv.writer(dest)
#
#     writer.writerows(reader)

"""Bonus two version"""
import argparse
import csv

parser = argparse.ArgumentParser()
# positional
parser.add_argument("old_filename", help="Source file path")
parser.add_argument("new_filename", help="Destination path (doesn't have to exist)")
# optional
parser.add_argument("--in-delimiter", dest="delim", help="Delimiter in source file")
parser.add_argument("--in-quote", dest="quote", help="Quote in source file")

args = parser.parse_args()
if args.new_filename == args.old_filename:
    raise ValueError("Source and destination file are the same location. Don't read and write from/to the same place!")

arguments = {} # empty dict
if args.delim: # if we have at least one set, create dict from them
    arguments["delimiter"] = args.delim
if args.quote:
    arguments["quotechar"] = args.quote

with open(args.old_filename, 'r', newline='') as source, open(args.new_filename, 'w', newline='') as dest:
    if not args.delim and not args.quote: # if we don't have either, detect!
        arguments["dialect"] = csv.Sniffer().sniff(source.read())
        source.seek(0)
    reader = csv.reader(source, **arguments)
    writer = csv.writer(dest)

    writer.writerows(reader)
