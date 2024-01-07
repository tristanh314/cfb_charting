import numpy as np
import pandas as pd
import openpyxl as op

############# USER INPUT REQUIRED #############
# INPUT RELATIVE PATH TO RAW DATA
drive_data = pd.read_csv('liberty_season_drives_raw_offense.csv', delimiter=',', header=None)
# INPUT RELATIVE PATH TO DESTINATION FILE
# file_name = 
######### DID YOU CHECK YOUR CHOICES? #########

# Filter for needed columns.
col_names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
           'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ',
           'BA','BB','BC','BD','BE','BF'
]
drive_data.columns=col_names
use_data=drive_data[['A','E','F','G','H','I','J','K', 'AT','AV']]

#Drop rows with no data from the original spreadsheet.
drop_rows = []
for i in range(0,(use_data.shape[0]-1)):
    if use_data.iloc[i]['E'] in ['1st','2nd','3rd','4th','C']:
        pass
    else:
        drop_rows+=[i]
use_data.drop(index=drop_rows, inplace=True)
use_data.to_csv('have_a_shufti.csv')
# Convert numerical columns to integers for memory savings.
cols = ['A','F','I','J','AT','AV']
for column in cols:
    use_data[column].apply(lambda x:int(x))

# Reindex dataframe for ease of aggregation.
use_data.set_index(keys=['A','I','J'], inplace=True)
print(use_data.head())
