# Chapter 55 - Pandas for Panel Data

# Access dataset
url1 = 'https://raw.githubusercontent.com/QuantEcon/lecture-python/master/source/_static/lecture_specific/pandas_panel/realwage.csv'

import pandas as pd
pd.set_option('display.max_columns', 6)
pd.options.display.float_format = '{:,.2f}'.format

realwage = realwage.pivot_table(values='value',index='Time',columns=['Country','Series','Pay period'])

realwage.index = pd.to_datetime(realwage.index)
type(realwage.index)

realwage_f = realwage.xs(('Hourly','In 2015 constant prices at 2015 USD exchange rates'),level=('Pay period','Series'), axis=1)
realwage_f.head()

url2 = 'https://raw.githubusercontent.com/QuantEcon/lecture-python/master/source/_static/lecture_specific/pandas_panel/countries.csv'

worlddata = pd.read_csv(url2, sep=';')
worlddata.head()

worlddata = worlddata[['Country (en)','Continent']]
worlddata = worlddata.rename(columns={'Country (en)': 'Country'})
worlddata.head()

realwage_f.transpose().head()

merged = pd.merge(realwage_f.transpose(), worlddata, how='left', left_index=True, right_on='Country')
merged.head()

merged[merged['Continent'].isnull()]

missing_continents = {'Korea': 'Asia',
                      'Russian Federation': 'Europe',
                      'Slovak Republic': 'Europe'}

merged['Country'].map(missing_continents)

merged['Continent'] = merged['Continent'].fillna(merged['Country'].map(missing_continents))

merged[merged['Country'] == 'Korea']

replace = ['Central America','North America','South America']

for country in replace:
    merged['Continent'].replace(to_replace=country,value='America',inplace=True)

merged = merged.set_index(['Continent','Country']).sort_index()
merged.head()

merged.columns

merged = merged.transpose()
merged.head()

merged.mean().head(10)

import matplotlib.pyplot as plt
%matplotlib inline
import matplotlib
matplotlib.style.use('seaborn-v0_8')

merged.mean().sort_values(ascending=False).plot(kind='bar', title="Average real minimum wage 2006 - 2016")
#Set country labels
country_labels = merged.mean().sort_values(ascending=False).index.get_level_values('Country').tolist()
plt.xticks(range(0, len(country_labels)), country_labels)
plt.xlabel('Country')
plt.show()

# Passing in axis=1 to .mean() will aggregate over columns (giving the average minimum wage for all countries over time)
merged.mean(axis=1).head()

# Plot as a line graph
merged.mean(axis=1).plot()
plt.title('Average real minimum wage 2006 - 2016')
plt.ylabel('2015 USD')
plt.xlabel('Year')
plt.show()

merged.T.groupby(level='Continent').mean().T.head()

merged.T.groupby(level='Continent').mean().T.plot()
plt.title('Average real minimum wage')
plt.ylabel('2015 USD')
plt.xlabel('Year')
plt.show()

merged.stack().describe()

grouped = merged.T.groupby(level='Continent')
grouped

import seaborn as sns
continents = grouped.groups.keys()
for continent in continents:
    data = grouped.get_group(continent).stack(future_stack=True).dropna()
    if data.nunique() >= 2:
        sns.kdeplot(data, label=continent, fill=True)
    else:
        print(f"Not enough unique data points to plot KDE for {continent}")

plt.title('Real minimum wages distribution')
plt.xlabel('US dollars')
plt.legend()
plt.show()

# Exercise 1
url3 = 'https://raw.githubusercontent.com/QuantEcon/lecture-python/master/source/_static/lecture_specific/pandas_panel/employ.csv'

employ = pd.read_csv(url3)
employ = employ.pivot_table(values='Value',index=['DATE'],columns=['UNIT','AGE','SEX','INDIC_EM','GEO'])
employ.index = pd.to_datetime(employ.index)

employ.columns.names

for name in employ.columns.names:
    print(name, employ.columns.get_level_values(name).unique())

# Exercise 2
employ.columns = employ.columns.swaplevel(0,-1)
employ = employ.sort_index(axis=1)

geo_list = employ.columns.get_level_values('GEO').unique().tolist()
countries = [x for x in geo_list if not x.startswith('Euro')]
employ = employ[countries]
employ.columns.get_level_values('GEO').unique()

employ_f = employ.xs(('Percentage of total population', 'Active population'),level=('UNIT','INDIC_EM'),axis=1)
employ_f.head()

employ_f = employ_f.drop('Total', level='SEX', axis=1)

box = employ_f.loc['2015'].unstack().reset_index()
sns.boxplot(x="AGE", y=0, hue="SEX", data=box, palette=("husl"),showfliers=False)
plt.xlabel('')
plt.xticks(rotation=35)
plt.ylabel('Percentage of population (%)')
plt.title('Employment in Europe (2015)')
plt.legend(bbox_to_anchor=(1,0.5))
plt.show()
