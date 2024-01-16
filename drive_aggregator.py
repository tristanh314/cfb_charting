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

# Drop non-used rows, as well as two point conversions, from the original spreadsheet.
drop_rows = []
for i in range(0,(drive_data.shape[0]-1)):
    if drive_data.iloc[i]['E'] in ['1st','2nd','3rd','4th'] and drive_data.iloc[i]['G'] == 's':
        drive_data.iloc[i]['G'] = 'p'
    elif drive_data.iloc[i]['E'] in ['1st','2nd','3rd','4th'] and drive_data.iloc[i]['G'] in ['r','p']:
        pass
    else:
        drop_rows+=[i]
use_data=drive_data[['A','E','F','G','H','I','J','K', 'AT','AV']].drop(index=drop_rows)

# Convert screens back to passes for simplicity.
def scren_pass(string):
    if string == 's':
        return 'p'
    else:
        return string
use_data['G']=use_data['G'].apply(scren_pass)

# Convert numerical columns to integers for memory savings.
cols = ['A','F','I','J','AT','AV']
for column in cols:
    use_data[column] = use_data[column].apply(lambda x:int(x))

# use_data.to_csv('have_a_shufti.csv')
    
## This is still under construction ##
# Define a function to aggregate data for a single drive.
df_count=use_data.groupby(['A','I','G'])['G'].count()
print(df_count)

def drive_summary(game,drive):
    """
    Input: An (A, I) integer pair specifying a single drive in the use_data dataframe.
    Output: A dictionary containing the number of plays and explosive plays (runs, passing including screens, and total), drive length,
    and if the drive ended in a touchdown.
    """
    drive_sum={}
    drive_sum['Plays']=use_data[game,drive].shape[0]

    return drive_sum