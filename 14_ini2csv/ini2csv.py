# import argparse
# import re
#
# parser = argparse.ArgumentParser()
# parser.add_argument("source_file")
# parser.add_argument("dest_file")
# parser.add_argument("--collapsed", action="store_true")
# args = parser.parse_args()
#
# curr_type = ""
# out_line = []
# with open(args.dest_file, 'w') as df:
#     with open(args.source_file, 'r') as f:
#
#         if args.collapsed:
#             df.write("header,indent_style,indent_size\n")
#         for line in f:
#             if re.match(r"\[\*\.\w+\]", line):
#                 curr_type = line[1:-2]
#                 if args.collapsed:
#                     if len(out_line) != 0:
#                         df.write("".join(out_line)+"\n")
#                         out_line = []
#                     out_line.append(curr_type.rstrip("\n"))
#             elif "=" in line:
#                 tag, _, val = line.partition(" = ")
#                 if args.collapsed:
#                     out_line.append(f",{val}".rstrip("\n"))
#                 else:
#                     df.write(f"{curr_type},{tag},{val}")
#
#     if args.collapsed:
#         df.write("".join(out_line)+"\n")

# Main problem (no bonus) with imports that are useful. Good practice
from argparse import ArgumentParser
import configparser
import csv

parser = ArgumentParser()
parser.add_argument("source_file")
parser.add_argument("dest_file")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.source_file)

with open(args.dest_file, 'w') as df:
    writer = csv.writer(df)

    # passing generator doesn't work on my system for some reason
    # writer.writerow(
    #     [name, key, value]
    #     for name, section in config.items()
    #     for key, value in section.items()
    # )

    for section in config.sections():
        for key, value in config[section].items():
            writer.writerow([section, key, value])

