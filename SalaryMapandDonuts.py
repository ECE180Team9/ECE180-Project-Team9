

import pandas as pd
import matplotlib.pyplot as plt 
import plotly.plotly as py
from plotly.offline import plot, iplot

questions = pd.read_csv('survey_results_schema.csv', header=0, sep=',')
questions = questions['Column']
chosen = questions.iloc[[1,3,5,11,14,18,28,43,45,46,53,81,87,88,89,90,96,129,130,142,143,152]].tolist()
'''Can use these columns to use for drop down lists and get number of options for each
one to potentially decide on type of graph.''' 
df= pd.read_csv('survey_results_public.csv', header=0, sep=',')[chosen]

# Some pie charts for some stack overflow specific data
df['StackOverflowWhatDo'].value_counts().rename("").plot(kind='pie',  legend = False, title = "Wouldn't know what to do without it",autopct='%1.1f%%')
plt.show()
df['StackOverflowBetter'].value_counts().rename("").plot(kind='pie',  legend = False, explode=(0, 0, 0, 0.25, 0.7),title = "Makes the internet better",autopct='%1.1f%%')
plt.show()
professionals = df.loc[df['Professional'] == "Professional developer"]
professionals['StackOverflowCopiedCode'].value_counts().rename("Pro").plot(kind='pie',  legend = False,title="Copied Code Directly",autopct='%1.1f%%')
plt.show()

students = df.loc[df['Professional'] == "Student"]
students['StackOverflowCopiedCode'].value_counts().rename("Student").plot(kind='pie',  legend = False,title="Copied Code Directly",autopct='%1.1f%%')
plt.show()
# WOW not much change....

# Get data to map salaries to countries
data = df[(df['Salary'] > 100)] # ignore salaries less than 100
data = data[data['EmploymentStatus'] == "Employed full-time"]
count = data.groupby('Country')['Salary'].count()
count = count[ count > 25] #ignore countries with less than 25 reported salaries
country_data = data[data['Country'].isin(count.index)].groupby('Country')
#make country into a column with the other being the mean salary corresponding
country_data = pd.concat([country_data['Salary'].mean(),country_data['Salary'].mean().index.to_series()], axis=1).reset_index(drop=True)

# countries and 3 letter country codes
countries={'Afghanistan':'AFG',
'Aland Islands':'ALA','Albania':'ALB','Algeria':'DZA','American Samoa':'ASM','Andorra':'AND','Angola':'AGO','Anguilla':'AIA','Antigua and Barbuda':'ATG',
'Antarctica':'ATA','Argentina':'ARG','Armenia':'ARM','Aruba':'ABW','Australia':'AUS','Austria':'AUT','Azerbaijan':'AZE','Azerbaidjan':'AZE',
'Bahrain':'BHR','Bahamas':'BHS','Bangladesh':'BGD','Barbados':'BRB','Belarus':'BLR',
'Belgium':'BEL','Belize':'BLZ','Benin':'BEN','Bermuda':'BMU','Bhutan':'BTN','Bolivia':'BOL','Bosnia and Herzegovina':'BIH','Bosnia-Herzegovina':'BIH',
'Botswana':'BWA','Bouvet Island':'BVT','Brazil':'BRA','British Virgin Islands':'VGB','British Indian Ocean Territory':'IOT',
'Brunei':'BRN','Brunei Darussalam':'BRN','Bulgaria':'BGR','Burkina Faso':'BFA','Burma':'MMR',
'Burundi':'BDI','Cabo Verde':'CPV','Cape Verde':'CPV','Cambodia':'KHM','Cameroon':'CMR',
'Canada':'CAN','Cayman Islands':'CYM','Central African Republic':'CAF','Chad':'TCD','Chile':'CHL',
'Christmas Island':'CHR','China':'CHN','Colombia':'COL','Comoros':'COM','Congo, Democratic Republic of the':'COD',
'Congo, Republic of the':'COG','Cook Islands':'COK','Costa Rica':'CRI','Cote d\'Ivoire':'CIV',
"Ivory Coast (Cote D'Ivoire)":'CIV','Croatia':'HRV','Cuba':'CUB','Curacao':'CUW','Cyprus':'CYP',
'Czech Republic':'CZE','Denmark':'DNK','Djibouti':'DJI','Dominica':'DMA','Dominican Republic':'DOM',
'Ecuador':'ECU','Egypt':'EGY','El Salvador':'SLV','Equatorial Guinea':'GNQ','Eritrea':'ERI','Estonia':'EST',
'Ethiopia':'ETH','Falkland Islands (Islas Malvinas)':'FLK','Falkland Islands':'FLK','Faroe Islands':'FRO',
'Fiji':'FJI','Finland':'FIN','France':'FRA','French Polynesia':'PYF','Gabon':'GAB',
'Gambia, The':'GMB','Georgia':'GEO','Germany':'DEU','Ghana':'GHA','Gibraltar':'GIB',
'Greece':'GRC','Greenland':'GRL','Grenada':'GRD','Guam':'GUM','Guatemala':'GTM',
'Guernsey':'GGY','Guinea-Bissau':'GNB','Guinea':'GIN','Guyana':'GUY','French Guyana':'GUY','Haiti':'HTI',
'Honduras':'HND','Heard and McDonald Islands':'HMD','Hong Kong':'HKG','Hungary':'HUN','Iceland':'ISL',
'India':'IND','Indonesia':'IDN','Iran':'IRN','Iraq':'IRQ','Ireland':'IRL','Isle of Man':'IMN',
'Israel':'ISR','Italy':'ITA','Jamaica':'JAM','Japan':'JPN','Jersey':'JEY','Jordan':'JOR',
'Kazakhstan':'KAZ','Kenya':'KEN','Kiribati':'KIR','Korea, North':'KOR','Korea, South':'PRK',
'South Korea':'PRK','North Korea':'KOR','Kosovo':'KSV','Kuwait':'KWT','Kyrgyzstan':'KGZ',
'Laos':'LAO','Latvia':'LVA','Lebanon':'LBN','Lesotho':'LSO','Liberia':'LBR','Libya':'LBY','Liechtenstein':'LIE',
'Lithuania':'LTU','Luxembourg':'LUX','Macau':'MAC','Macedonia':'MKD','Madagascar':'MDG',
'Malawi':'MWI','Malaysia':'MYS','Maldives':'MDV','Mali':'MLI','Malta':'MLT','Marshall Islands':'MHL',
'Martinique (French)':'MTQ','Mauritania':'MRT','Mauritius':'MUS','Mexico':'MEX','Micronesia, Federated States of':'FSM',
'Moldova':'MDA','Moldavia':'MDA','Monaco':'MCO','Mongolia':'MNG','Montenegro':'MNE','Montserrat':'MSR',
'Morocco':'MAR','Mozambique':'MOZ','Myanmar':'MMR','Namibia':'NAM','Nepal':'NPL','Netherlands':'NLD',
'Netherlands Antilles':'ANT','New Caledonia':'NCL','New Caledonia (French)':'NCL','New Zealand':'NZL','Nicaragua':'NIC',
'Nigeria':'NGA','Niger':'NER','Niue':'NIU','Northern Mariana Islands':'MNP','Norway':'NOR','Oman':'OMN',
'Pakistan':'PAK','Palau':'PLW','Panama':'PAN','Papua New Guinea':'PNG','Paraguay':'PRY','Peru':'PER',
'Philippines':'PHL','Pitcairn Island':'PCN','Poland':'POL','Polynesia (French)':'PYF','Portugal':'PRT',
'Puerto Rico':'PRI','Qatar':'QAT','Reunion (French)':'REU','Romania':'ROU','Russia':'RUS','Russian Federation':'RUS',
'Rwanda':'RWA','Saint Kitts and Nevis':'KNA','Saint Lucia':'LCA','Saint Martin':'MAF','Saint Pierre and Miquelon':'SPM',
'Saint Vincent and the Grenadines':'VCT','Saint Vincent & Grenadines':'VCT','S. Georgia & S. Sandwich Isls.':'SGS','Samoa':'WSM',
'San Marino':'SMR','Saint Helena':'SHN','Sao Tome and Principe':'STP','Saudi Arabia':'SAU','Senegal':'SEN',
'Serbia':'SRB','Seychelles':'SYC','Sierra Leone':'SLE','Singapore':'SGP','Sint Maarten':'SXM',
'Slovakia':'SVK','Slovak Republic':'SVK','Slovenia':'SVN','Solomon Islands':'SLB','Somalia':'SOM','South Africa':'ZAF',
'South Sudan':'SSD','Spain':'ESP','Sri Lanka':'LKA','Sudan':'SDN','Suriname':'SUR',
'Swaziland':'SWZ','Sweden':'SWE','Switzerland':'CHE','Syria':'SYR','Taiwan':'TWN','Tajikistan':'TJK',
'Tadjikistan':'TJK','Tanzania':'TZA','Thailand':'THA','Timor-Leste':'TLS','Togo':'TGO','Tonga':'TON',
'Trinidad and Tobago':'TTO','Tunisia':'TUN','Turkey':'TUR','Turkmenistan':'TKM','Tuvalu':'TUV',
'Uganda':'UGA','Ukraine':'UKR','United Arab Emirates':'ARE','United Kingdom':'GBR','United States':'USA',
'U.S. Minor Outlying Islands':'UMI','Uruguay':'URY','Uzbekistan':'UZB','Vanuatu':'VUT',
'Vatican City State':'VAT','Venezuela':'VEN','Vietnam':'VNM','Virgin Islands':'VGB',
'Virgin Islands (USA)':'VIR','Virgin Islands (British)':'VGB','West Bank':'WBG','Yemen':'YEM',
'Zaire':'ZAR','Zambia':'ZMB','Zimbabwe':'ZWE'}
codes = []
for country in country_data['Country']:
    codes.append(countries[country])

# maps salaries to world map 
data = [ dict(
        type = 'choropleth',
        locations = codes,
        z = country_data['Salary'],
        text = country_data['Country'],
    
        colorscale = [[0,"rgb(5, 172, 10)"],[0.35,"rgb(40, 190, 60)"],[0.5,"rgb(70, 245, 100)"],\
            [0.6,"rgb(90, 245, 120)"],[0.7,"rgb(106, 247, 137)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '$',
            title = 'Average Salary<br>US$'),
      ) ]

layout = dict(
    title = 'Stack Overflow Average Salaries',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
plot(fig, validate = False)

# quantiles for salaries
data = df[(df['Salary'] > 100)]
data = data[data['EmploymentStatus'] != "Not employed, and not looking for work"]
data = data.dropna(axis=0, subset = ['Salary'])
data = data[data['EmploymentStatus'] == "Employed full-time"]
data= data.groupby(pd.qcut(data['Salary'], 4))['Salary'].count()
data.plot(kind='barh',alpha=0.3)
plt.show()

#ideal work start time can check with WorkStart and some analysis
# maybe transition over few years most popular languages. 


# returns data for students and professionals wanting to change the world
def ChangeTheWorld():
    entries = pd.read_csv('survey_results_public.csv', header=0, sep=',')
    students = entries.groupby(['Professional']).get_group('Student')   
    professionals = entries.groupby(['Professional']).get_group('Professional developer')
    studentsChangeWorld = students.groupby(['ChangeWorld']).count()['Respondent']
    prosChangeWorld = professionals.groupby(['ChangeWorld']).count()['Respondent']
    return studentsChangeWorld, prosChangeWorld

result = ChangeTheWorld()
# plot pie charts
result = (result[0].rename(""),result[1].rename(""))
result[0].plot(kind='pie',  legend = False, title = 'Students',autopct='%1.1f%%')
plt.show()
result[1].plot(kind='pie', legend = False, title = 'Professionals',autopct='%1.1f%%')
plt.show()

