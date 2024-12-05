import pandas as pd
import re

desired_width = 320
desired_height = 320
pd.set_option('display.width', desired_width)
# pd.set_height('display.height', desired_height)
pd.set_option('display.max_columns', None)

df = pd.read_csv('./dataset/pokemon_data.csv')

## Read Headers
# print(df.columns)

## Read Each Column
# print(df['name'])

## Read each row
# for index, row in df.iterrows():
#     print(index, row)

## Read specific location by non-integer stuff
# print(df.loc[df['type1'] == "Fire"])

## Read specific location by integer
# print(df.iloc[2, 1])

## Basic mean/standard dev/etc. stats
#df.describe()

## sorting
# df.sort_values('Type1', 'HP', ascending)

## Create New Column
# df['total'] = df.iloc[:, 4:10].sum(axis=1)
#
# df.head(5)

## Switch New Column to different location in column order
# cols = list(df.columns.values)
# df = df[cols[0:4] + [cols[-1]] + cols[4:12]]

## Save to CSV
# df.to_csv('./dex_saves/modified.csv') # Includes the auto indexing done by pandas

# df.to_csv('./dex_saves/modified.csv', index=False) # Does not include the auto indexing done by pandas

## Filtering Data

# new_df = df.loc[(df['type1'] == 'Grass') & (df['type2'] == 'Poison') & (df['hp'] > 70)]

# new_df = new_df.reset_index(drop=True) # Reset Pandas Index when filtering data, removing old indices, not in place
# new_df.reset_index(drop=True, inplace=True) # Reset Pandas Index when filtering data, removing old indices, in place

# df.loc[df['Name'].str.contains('Mega')] # Get all that contains "mega"
# df.loc[~df['Name'].str.contains('Mega')] # Get all that does not contains "mega"


# df.loc[~df['type1'].str.contains('Fire|Grass', regex=True)] # Regex Filtering, add "flags=re.I" to ignore case
# df.loc[~df['name'].str.contains('^pi[a-z]*', regex=True)] # Regex Filtering, all names that start with PI

## Conditional Changes
# df.loc[df['Type 1'] == 'Fire', 'Type 1'] = 'Flamer' # Changes all 'Fire' types to be 'flamer' types
# df.loc[df['Type 1'] == 'Fire', 'Legendary'] = True # Changes all Legendaries to be Fire Types / all, and only, Fire Types are Legendary


# df.loc[df['total'] > 500, ['Generation', 'Legendary']] = 'TEST VALUE' # Changes Generation & Legendary fields to be TEST VALUE if the # of returned pokemon exceeds 500
# df.loc[df['total'] > 500, ['Generation', 'Legendary']] = ['TEST 1', 'TEST 2'] # Changes Generation to be TEST 1 and Legendary to be TEST 2 if the # of returned pokemon exceeds 500


## Aggregate Statistics
# new_df = df.groupby(['type1']).mean(numeric_only=True).sort_values('defense', ascending=False) # Average Stats by Type, sorted by highest defense
#
# df['count'] = 1
#
# new_df = df.groupby(['type1', 'type2']).count()['count']


## Working w/large amounts of data (I.E. loading in chunks of a file at a time)

# pd.read_csv('./dataset/pokemon_data.csv', chunksize=5) # 5 rows at a time

# print(df)
# print(new_df)

