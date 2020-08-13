import matplotlib, pandas as pd, numpy as np, calendar
from datetime import datetime
from matplotlib import pyplot as plt

# read csv
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv', header=0)

# Convert to Celcius
df['Celcius'] = df.Data_Value / 10

# Convert date
df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

# split into < 2015 and 2015
df_2005 = df[df.Date < "2015-01-01"]
df_2015 = df[df.Date >= "2015-01-01"].groupby('Date')

# Get min, max for 2015
max2015 = df_2015.max().reset_index()[["Date", "Celcius"]]
min2015 = df_2015.min().reset_index()[["Date", "Celcius"]]

# print(min2015, max2015)

# For years < 2015 we need to summarize by the day of the year
# we cheat a little bit and set the year equals to 2015
df_2005['daymonth'] = df_2005.Date.dt.strftime(date_format="%d-%m")
df_2005["daymonth"] = df_2005["daymonth"] + "-2015"

# drop feb 29
df_2005 = df_2005[df_2005['daymonth'] != "29-02-2015"].groupby("daymonth")

# get the max and min
max2005 = df_2005.max().reset_index()
min2005 = df_2005.min().reset_index()

# Convert to date time, slice date and celcius and sort by date
max2005['Date'] = pd.to_datetime(max2005['daymonth'], format="%d-%m-%Y")
max2005 = max2005[["Date", "Celcius"]]
max2005.sort_values(by="Date", inplace=True)

# Convert to date time, slice date and celcius and sort by date
min2005['Date'] = pd.to_datetime(min2005['daymonth'], format="%d-%m-%Y")
min2005 = min2005[["Date", "Celcius"]]
min2005.sort_values(by="Date", inplace=True)

# plot the min, max for 20015 to 2014
plt.plot(min2005.Date, min2005.Celcius, label="Min. 2005-2014", alpha=.25)
plt.plot(max2005.Date, max2005.Celcius, alpha=0.25, label="Max. 2005-2014")

x = plt.gca()
x.spines['top'].set_visible(False)
x.spines['right'].set_visible(False)
x.set_xlim([datetime(2015,1,1), datetime(2015,12,31)])
# x.spines['left'].set_position(('data',1))

# format tick marks
plt.xticks(np.arange('2015-01', '2015-12', dtype='datetime64[D]'))
np.arange('2015-01', '2016-01', dtype='datetime64[M]', )
plt.xticks(np.arange('2015-01', '2016-01', dtype='datetime64[M]'), 
    [ calendar.month_abbr[i] for i in range(1,13) ])

# plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Temperature (Celcius)')

plt.gca().fill_between(min2005.Date, 
                        min2005.Celcius, 
                        max2005.Celcius, 
                        alpha=0.25, 
                        facecolor='grey')

# set index as the date 
max2005.set_index('Date', inplace=True)
max2015.set_index('Date', inplace=True)
min2015.set_index("Date", inplace=True)
min2005.set_index("Date", inplace=True)

# create bool filter of hotter and colder days
max2015['hotter'] = max2015>max2005
min2015['colder'] = min2015<min2005

# get values from the dataframe
hotter=max2015[max2015.hotter].reset_index()
colder=min2015[min2015.colder].reset_index()

# add the plot
plt.plot(hotter.Date, hotter.Celcius, 'o', markersize=2.5, color='red', label="2015 > Max 2005-2014")
plt.plot(colder.Date, colder.Celcius, 'o', markersize=2.5, color='blue', label="2015 < Min 2005-2014")

plt.legend(frameon=False)
plt.title("Min/Max Temperatures for years 2005-2014 with Overlay of 2015\n Temperature readings that are hotter or colder")

plt.savefig('ans.png')