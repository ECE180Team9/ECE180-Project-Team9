
# coding: utf-8

# In[4]:


import plotly.graph_objs as go
from plotly.offline import plot, iplot
import pandas as pd
#This program outputs combined bar graphs with a drop down list to focus on a specific type of developer 
#and the tools used by them. 

def preferredIDE(df,typeDev):
    '''
    input df is a pandas dataframe containing at least developer type, ide, and respondent columns
    input typeDev is a string determining the type of developer to return IDE values for. 
    output dataframe that contains the ides and the number of developers of typeDev who use it.
    '''
    uniqueIDE = getIDEs(df)
    clean = df.dropna(subset=['DeveloperType'])         
    #devs = clean.loc[clean['DeveloperType'].str.contains(typeDev)] #for developers with multiple types
    devs = clean.loc[clean['DeveloperType'] == typeDev] #developer who is only this type
    devs = devs.dropna(subset=['IDE'])
    populartools = {}
    count = devs['Respondent'].count()
    for ide in uniqueIDE:
        removeplus = ide.replace("+", "")
        dev = devs.loc[devs['IDE'].str.contains(removeplus)]
        populartools[ide] = dev['Respondent'].count() / (count * 1.0)

    return pd.DataFrame(populartools.items(), columns=['IDE', 'Users'])

def getIDEs(df):
    '''
    input df is pandas dataframe 
    output is a set of unique items in IDE column
    '''
    uniqueIDE = set()
    noNan = df.dropna(subset=['DeveloperType'])
    for index, row in df.iterrows():
        if isinstance(row['IDE'],basestring):
                ides = row['IDE'].split(";")
                ides = map(str.strip, ides)
                uniqueIDE.update(set(ides))
                continue
    return uniqueIDE

#Choose the relevant survey questions for this project
questions = pd.read_csv('survey_results_schema.csv', header=0, sep=',')
questions = questions['Column']
chosen = questions.iloc[[0,1,3,5,11,14,18,28,43,45,46,53,81,87,88,89,90,96,129,130,142,143,152]].tolist()

#Get relevant data from survey results
df= pd.read_csv('survey_results_public.csv', header=0, sep=',')[chosen]

#Get the data relevant to different developer types
dfweb = preferredIDE(df,"Web developer")
dfmobile = preferredIDE(df,"Mobile developer")
dfdesktop = preferredIDE(df,"Desktop applications developer")
dfdata = preferredIDE(df,"Data scientist")

#Create the different bar graphs for each developer type
trace_web = go.Bar(x=dfweb['IDE'],
                        y=dfweb['Users'],
                        name='web',
                        marker=dict(color='rgb(158,202,225)'))
trace_mobile = go.Bar(x=dfmobile['IDE'],
                        y=dfmobile['Users'],
                        name='mobile',
                        visible = True,
                         marker=dict(color='rgb(255,165,0)'))
trace_desktop = go.Bar(x=dfdesktop['IDE'],
                        y=dfdesktop['Users'],
                        name='desktop',
                        visible = True,
                        marker=dict(color='rgb(46,139,87)'))
trace_data = go.Bar(x=dfdata['IDE'],
                        y=dfdata['Users'],
                        name='data',
                        visible = True,
                        marker=dict(color='rgb(178,34,34)'))

data = [trace_web, trace_mobile, trace_desktop,trace_data]

#Have an annotation point at the most popular tool for each developer type.
web_annotations=[dict(x= dfweb['Users'].idxmax(),
                       y=dfweb['Users'].max(),
                       xref='x', yref='y',
                       text='Most popular: <br>'+str(dfweb['Users'].max()) +  "%",
                       ax=0, ay=-40)]
mobile_annotations=[dict(x=dfmobile['Users'].idxmax(),
                      y=dfmobile['Users'].max(),
                      xref='x', yref='y',
                      text='Most popular: <br>'+str(dfmobile['Users'].max()) +  "%",
                      ax=0, ay=-40)] 
desktop_annotations=[dict(x=dfdesktop['Users'].idxmax(),
                      y=dfdesktop['Users'].max(),
                      xref='x', yref='y',
                      text='Most popular: <br>'+str(dfdesktop['Users'].max()) +  "%",
                      ax=0, ay=-40)] 
data_annotations=[dict(x=dfdata['Users'].idxmax(),
                      y=dfdata['Users'].max(),
                      xref='x', yref='y',
                      text='Most popular: <br>'+str(dfdata['Users'].max()) +  "%",
                      ax=0, ay=-40)] 
all_annotations=[dict(showarrow= False, text = "")] #no arrows here

#Handle the dropdown list selection and hiding/changing charts. 
updatemenus = list([
    dict(active=4,
         buttons=list([   
            dict(label = 'Web',
                 method = 'update',
                 args = [{'visible': [True, False,False,False]},
                         {'title': 'Web Developers',
                          'annotations': web_annotations}]),
            dict(label = 'Mobile',
                 method = 'update',
                 args = [{'visible': [False, True, False, False]},
                         {'title': 'Mobile Developers',
                         'annotations': mobile_annotations}]),
            dict(label = 'Desktop',
                 method = 'update',
                 args = [{'visible': [False, False, True, False]},
                         {'title': 'Desktop Application Developers',
                          'annotations': desktop_annotations}]),
            dict(label = 'Data',
                 method = 'update',
                 args = [{'visible': [False, False, False, True]},
                         {'title': 'Data Scientists',
                         'annotations': data_annotations}]),
            dict(label = 'All',
                 method = 'update',
                 args = [{'visible': [True, True, True, True]},
                         {'title': 'Developer Types and IDEs',
                         'annotations':all_annotations}])
        ]),
    ) 
])

layout = dict(title='Developer Tools', showlegend=True, yaxis=dict(title = "% of respondents"), updatemenus=updatemenus)

fig = dict(data=data, layout=layout)
#output to file and open in browser
plot(fig, filename='DeveloperTools.html')

