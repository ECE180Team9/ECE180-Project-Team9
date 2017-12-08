

import matplotlib.pyplot as plt
import pandas as pd

# This script gets the average salary based on developer type and makes a bar chart
questions = pd.read_csv('survey_results_schema.csv', header=0, sep=',')
questions = questions['Column']
chosen = questions.iloc[[0,1,3,5,11,14,18,28,43,45,46,53,81,87,88,89,90,96,129,130,142,143,152]].tolist()
df= pd.read_csv('survey_results_public.csv', header=0, sep=',')[chosen]
noNan = df.dropna(subset=['DeveloperType'])

# get all unique types of developers
uniquedev =set()
for index, row in df.iterrows():
    if isinstance(row['DeveloperType'],basestring):
        devs = row['DeveloperType'].split(";")
        devs= map(str.strip, devs) # sometimes they have spaces before name in entry
        uniquedev.update(set(devs))
        continue
salaries = {}

# calculate average salaries for each type
for devType in uniquedev:
    dev = noNan.loc[noNan['DeveloperType'].str.contains(devType)]
    salaries[devType] = dev['Salary'].mean()
del salaries['Other']

# make a pandas dataframe and plot a horizontal bar chart
salaries = pd.DataFrame(salaries.items(), columns=["DeveloperType", 'Average Salary'])
salaries = salaries.set_index('DeveloperType')
salaries.plot(kind='barh')
plt.show()

