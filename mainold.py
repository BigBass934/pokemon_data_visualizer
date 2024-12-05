import pandas as pd
import re

# Variables for Pandas command line output in Pycharm
desired_width = 320

pd.set_option('display.width', desired_width)

pd.set_option('display.max_columns', None)

official_df = pd.read_csv('./dataset/pokemon_data.csv')

