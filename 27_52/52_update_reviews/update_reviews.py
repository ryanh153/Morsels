# from pathlib import Path
# import argparse
# from itertools import islice
#
# import pandas
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Parser for update_reviews.py')
#     parser.add_argument('main_file')
#     parser.add_argument('update_file')
#     parser.add_argument('--update', action='store_true')
#     parser.add_argument('--sort', action='store_true')
#     args = parser.parse_args()
#
#     main_df = pandas.read_csv(Path(args.main_file), keep_default_na=False)
#     update_df = pandas.read_csv(Path(args.update_file), keep_default_na=False)
#
#     # get unique restaurant data from both files
#     original_restaurants = {index: (row['Name'], row['Street']) for index, row in islice(main_df.iterrows(), 0, None)}
#     update_restaurants = {index: (row['Name'], row['Street']) for index, row in islice(update_df.iterrows(), 0, None)}
#
#     # Get the indices in the update file where duplicate restaurants are found
#     update_indices = [key for key, value in update_restaurants.items()
#                       if value in original_restaurants.values()]
#
#     if args.update:
#         # if we're updating we need the locations of the duplicates in the main file too
#         main_indices = [key for key, value in original_restaurants.items()
#                         if value in update_restaurants.values()]
#         for main_index, update_index in zip(main_indices, update_indices):
#             main_df.Comments[main_index] = update_df.Comments[update_index]
#     update_df = update_df.drop(update_indices, axis=0)
#
#     main_df = main_df.merge(update_df, how='outer')
#     print(f'Added {len(update_df)} row(s)')
#
#     if args.update:
#         print(f'Updated {len(update_indices)} row(s)')
#
#     if args.sort:
#         main_df = main_df.sort_values(['State', 'City', 'Name'])
#
#     main_df.to_csv(Path(args.main_file), index=False)


import argparse
import csv


def restaurant_sort(entry):
    return entry[1]['State'], entry[1]['City'], entry[1]['Name']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser for update_reviews.py')
    parser.add_argument('main_file')
    parser.add_argument('update_file')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--sort', action='store_true')
    args = parser.parse_args()

    main_reader = csv.DictReader(open(args.main_file))
    updates_reader = csv.DictReader(open(args.update_file))

    main = {}
    for row in main_reader:
        main[row['Name'], row['Street']] = {key: val for key, val in zip(main_reader.fieldnames, row.values())}

    added, updates = 0, 0
    for row in updates_reader:
        if (row['Name'], row['Street']) not in main:
            added += 1
            main[row['Name'], row['Street']] = {key: val for key, val in zip(main_reader.fieldnames, row.values())}
        elif args.update and row['Comments']:
            updates += 1
            main[row['Name'], row['Street']]['Comments'] = row['Comments']

    print(f'Added {added} row(s)')
    if args.update:
        print(f'Updated {updates} row(s)')

    if args.sort:
        main = {k: v for k, v in sorted(main.items(), key=restaurant_sort)}

    with open(args.main_file, 'r+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=main_reader.fieldnames)
        writer.writeheader()
        writer.writerows(main.values())
