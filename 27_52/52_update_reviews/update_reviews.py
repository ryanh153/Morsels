from pathlib import Path
import argparse
from itertools import islice

import pandas

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser for update_reviews.py')
    parser.add_argument('main_file')
    parser.add_argument('update_file')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--sort', action='store_true')
    args = parser.parse_args()

    main_df = pandas.read_csv(Path(args.main_file), keep_default_na=False)
    update_df = pandas.read_csv(Path(args.update_file), keep_default_na=False)

    original_restaurants = {index: (row['Name'], row['Street']) for index, row in islice(main_df.iterrows(), 0, None)}
    update_restaurants = {index: (row['Name'], row['Street']) for index, row in islice(update_df.iterrows(), 0, None)}

    indices = [key for key, value in update_restaurants.items()
               if value in original_restaurants.values()]
    main_indices = [key for key, value in original_restaurants.items()
                    if value in update_restaurants.values()]

    if args.update:
        for main_index, update_index in zip(main_indices, indices):
            main_df.Comments[main_index] = update_df.Comments[update_index]
    update_df = update_df.drop(indices, axis=0)

    main_df = main_df.merge(update_df, how='outer')
    print(f'Added {len(update_df)} row(s)')

    if args.update:
        print(f'Updated {len(indices)} row(s)')

    if args.sort:
        main_df = main_df.sort_values(['State', 'City', 'Name'])

    main_df.to_csv(Path(args.main_file), index=False)
