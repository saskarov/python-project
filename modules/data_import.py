import zipfile
import os

# Path to the zipped file
zip_path = 'data/IMDb.zip'

# Extract files
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('data/imdb')  # Extracted files will be in data/imdb
print("Files extracted to data/imdb")

import pandas as pd

# Load essential IMDb files
title_basics = pd.read_csv('data/imdb/title.basics.tsv', sep='\t', na_values='\\N')
title_ratings = pd.read_csv('data/imdb/title.ratings.tsv', sep='\t', na_values='\\N')

# Preview data
print(title_basics.head())
print(title_ratings.head())