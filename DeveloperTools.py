# By Jared, ask if any questions
import plotly.graph_objs as go
from plotly.offline import plot, iplot
import pandas as pd
''' Charts data about respondents with unique developer types to see what tools like
    languages or IDEs they use. Considering developers with multiple types makes results
    less meaningful as they become more muddled. 
'''
def tool_data(df,dev_type,data_type):
    """
    input df is a pandas dataframe containing at least developer type, data_type, and respondent columns
    input dev_type is a string determining the type of developer to return tool values for. 
    input data_type is the string determining the type of data to chart, i.e. IDEs or languages
    output dataframe that contains the data and the number of developers of dev_type who use it.
    """
    assert(isinstance(df,pd.DataFrame)), "Data is not a dataframe"
    assert(isinstance(dev_type,basestring)), "Data is not a string"
    unique_elems = get_unique(df, data_type)
    clean = df.dropna(subset=['DeveloperType'])    
    # devs = clean.loc[clean['DeveloperType'].str.contains(typeDev)] # for developers with multiple types
    devs = clean.loc[clean['DeveloperType'] == dev_type]  # developer who is only this type, more specific results
    assert len(devs.index) > 0 , "This DeveloperType is not valid"
    devs = devs.dropna(subset=[data_type])
    populartools = {}
    count = devs['Respondent'].count()
    for elem in unique_elems:
        if "++" in elem or "#" in elem:
            dev = devs.loc[devs[data_type].str.contains(elem, regex = False)]
        else:
            # make sure to get exact element, i.e. not Objective-C when looking for C. PandasExercise :D
            dev = devs.loc[devs[data_type].str.contains(r"(?:^|\s)%s(?:$|\;)"%elem)]
        populartools[elem] = (dev['Respondent'].count() / (count * 1.0))*100
    
    return pd.DataFrame(populartools.items(), columns=[data_type, 'Users'])


def get_unique(df, data_type):
    """
    input df is pandas dataframe 
    input data_type is a string representing what element we will get all unique values for
    output is a set of unique items in IDE column
    """
    assert(isinstance(df,pd.DataFrame)), "Data is not a dataframe"
    unique_elems = set()
    for index, row in df.iterrows():
        if isinstance(row[data_type],basestring):
                elems = row[data_type].split(";")
                elems = map(str.strip, elems)
                unique_elems.update(set(elems))
                continue
    return unique_elems

def getdeveloperdata(df, data_type):
    """
    input df is pandas dataframe with at least developer type, data_type, and respondent columns
    input data_type is a string representing what data developer type is being viewed against
    output path to html file
    """
    #Get the data relevant to different developer types
    dfweb = tool_data(df,"Web developer",data_type)
    dfmobile = tool_data(df,"Mobile developer",data_type)
    dfdesktop = tool_data(df,"Desktop applications developer",data_type)
    dfdata = tool_data(df,"Data scientist",data_type)

    #Create the different bar graphs for each developer type
    trace_web = go.Bar(x=dfweb[data_type],
                            y=dfweb['Users'],
                            name='web',
                            marker=dict(color='rgb(158,202,225)'))
    trace_mobile = go.Bar(x=dfmobile[data_type],
                            y=dfmobile['Users'],
                            name='mobile',
                            visible = True,
                             marker=dict(color='rgb(255,165,0)'))
    trace_desktop = go.Bar(x=dfdesktop[data_type],
                            y=dfdesktop['Users'],
                            name='desktop',
                            visible = True,
                            marker=dict(color='rgb(46,139,87)'))
    trace_data = go.Bar(x=dfdata[data_type],
                            y=dfdata['Users'],
                            name='data',
                            visible = True,
                            marker=dict(color='rgb(178,34,34)'))

    data = [trace_web, trace_mobile, trace_desktop,trace_data]

    #Have an annotation point at the most popular tool for each developer type.
    web_annotations=[dict(x= dfweb['Users'].idxmax(),
                           y=dfweb['Users'].max(),
                           xref='x', yref='y',
                           text='Most used: <br>'+str(dfweb['Users'].max()) +  "%",
                           ax=0, ay=-40)]
    mobile_annotations=[dict(x=dfmobile['Users'].idxmax(),
                          y=dfmobile['Users'].max(),
                          xref='x', yref='y',
                          text='Most used: <br>'+str(dfmobile['Users'].max()) +  "%",
                          ax=0, ay=-40)] 
    desktop_annotations=[dict(x=dfdesktop['Users'].idxmax(),
                          y=dfdesktop['Users'].max(),
                          xref='x', yref='y',
                          text='Most used: <br>'+str(dfdesktop['Users'].max()) +  "%",
                          ax=0, ay=-40)] 
    data_annotations=[dict(x=dfdata['Users'].idxmax(),
                          y=dfdata['Users'].max(),
                          xref='x', yref='y',
                          text='Most used: <br>'+str(dfdata['Users'].max()) +  "%",
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
                             {'title': 'Developer Types and Tools: ' + data_type,
                             'annotations':all_annotations}])
            ]),
        ) 
    ])

    layout = dict(title='Developer Types and Tools: '+data_type, showlegend=True, yaxis=dict(title = "% of respondents"), updatemenus=updatemenus)

    fig = dict(data=data, layout=layout)
    #output to file and open in browser
    return plot(fig, filename='Developer' + data_type +'.html')
#Choose the relevant survey questions for this project
questions = pd.read_csv('survey_results_schema.csv', header=0, sep=',')
questions = questions['Column']
chosen = questions.iloc[[0,1,3,5,11,14,18,28,43,45,46,53,81,87,88,89,90,96,129,130,142,143,152]].tolist()

#Get relevant data from survey results
df= pd.read_csv('survey_results_public.csv', header=0, sep=',')[chosen]

#Get charts for programming languages and ides by developer type
getdeveloperdata(df,"HaveWorkedLanguage")
getdeveloperdata(df,"IDE")

