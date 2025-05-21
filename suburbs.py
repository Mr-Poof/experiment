## Step 1: Combine all CSV and Geographical Data
# This file creates the databases


import pandas as pd
import os

abs_csv_list = []

from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db')



df1 = pd.read_csv("2021_NSW_Census_Data/SAL_Data/2021Census_G01_NSW_SAL.csv")#Basic characteristics (age, total pop)
df2 = pd.read_csv("2021_NSW_Census_Data/SAL_Data/2021Census_G02_NSW_SAL.csv")#Median income, rent etc.

#This excel files gives names and geographic location
geoData = pd.read_excel("georef-australia-state-suburb.xlsx", sheet_name="Sheet1",usecols = "A,B,E,G,H,I")

def formatCode(code):
    return f"SAL{code}"



Sydney_LGA_List = ['Bayside','Blacktown','Burwood','Camden','Canada Bay','Campbelltown',
    'Canterbury-Bankstown','Cumberland','Fairfield','Georges River',
    'Hawkesbury','The Hills Shire','Hornsby','Hunters Hill','Inner West','Ku-ring-gai',
    'Lane Cove','Liverpool','Mosman','North Sydney','Northern Beaches',
    'Parramatta','Penrith','Randwick','Ryde','Strathfield','Sutherland', 'Sydney',
    'Waverly','Willoughby','Woollahra']

#filter out any suburb not in the LGA List

#pass in a string of council(s), seperated by commas
def inSydney(council_string):
    councils = [c.strip() for c in council_string.split(",")]
    return any(c in Sydney_LGA_List for c in councils)

geoData = geoData[geoData['Official Name Local Government Area'].apply(inSydney)]

#format the SAL codes to match the ABS format and then rename the column
geoData['Official Code Suburb'] = geoData['Official Code Suburb'].apply(formatCode)
geoData = geoData.rename(columns = {'Official Code Suburb': 'SAL_CODE_2021'})

combined = df1.merge(df2, on = "SAL_CODE_2021", suffixes = (f'x{1}', f'y{1}'))
combined = combined.merge(geoData, on = "SAL_CODE_2021")

def cleanSuburbName(name):
    cleaned_name = name.split(" (")[0]
    return cleaned_name

combined['Official Name Suburb'] = combined['Official Name Suburb'].apply(cleanSuburbName)

combined = combined[combined["Tot_P_P"] > 100]

combined.to_sql(name = "Suburbs", con = engine, if_exists = 'replace')

#The Following Code will Read and Combine ALL CSV files and turn it into a database -> For now, this is too difficult to implement as there are innumerable variables, for now, we stick to just using a select few of these tables

'''#store them all in this list
abs_csv_list = []

#119 csv files
counter = 0;
for entry in os.scandir('2021_NSW_Census_Data/SAL_Data'):
    if entry.is_file() & entry.path.endswith('.csv'):
        df = pd.read_csv(entry.path)
        abs_csv_list.append(df)
        print(entry.path)

#print(len(abs_csv_list))

#combined = pd.merge(abs_csv_list[0], abs_csv_list[1], left_on = "SAL_CODE_2021", right_on = "SAL_CODE_2021")#, on = ["SAL_CODE_2021"])

combined = abs_csv_list[0]

#Merge first five csv files as test
for i in range(1, 5, 1):#len(abs_csv_list), 1):
    #combined = pd.merge(combined, abs_csv_list[i], left_on = "SAL_CODE_2021", right_on = "SAL_CODE_2021")

    combined = combined.merge(abs_csv_list[i], on = "SAL_CODE_2021", suffixes = (f'x{i}', f'y{i}'))
    #combined = combined.drop_duplicates()'''






