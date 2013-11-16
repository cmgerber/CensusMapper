# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
from pandas.io.excel import ExcelFile

# <codecell>

infile = ExcelFile('ColorBrewer_all_schemes_RGBonly3.XLS')

# <codecell>

df = infile.parse(infile.sheet_names[0])

# <codecell>

df_fill = df.fillna(method = 'ffill')

# <codecell>

df_fill.head()

# <codecell>

df_fill = df_fill.drop(['Type', 'ColorNum'], axis = 1)

# <codecell>

df_fill.head()

# <codecell>

#df_key = pd.factorize(pd.lib.fast_zip([df_fill.ColorName, df_fill.NumOfColors]))

# <codecell>

#df_key[0]

# <codecell>

#df_fill.index = df_key[0]

# <codecell>

df_fill.head(40)

# <codecell>

df_fill.to_excel('ColorBrewer_all_schemes_RGBonly3_updated.XLS', sheet_name = 'Sheet1')

# <codecell>

df_fill.to_csv('ColorBrewer_all_schemes_RGBonly3_updated.csv', header = False)

# <codecell>

test_in = pd.read_csv('ColorBrewer_all_schemes_RGBonly3_updated.csv')

# <codecell>

test_in.head(30)

# <codecell>


