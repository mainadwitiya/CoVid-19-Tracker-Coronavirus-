import folium as folium
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import folium

import matplotlib.pyplot as plt
url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-28-2020.csv'
confirmed_timeseries_url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
deaths_timeseries_url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
recovered_timeseries_url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

daily_df=pd.read_csv(url)
new_daily_df=daily_df.drop(["Province/State","Last Update"], axis=1)
new_daily_df2 = new_daily_df.groupby(['Country/Region']).agg('sum')
x=new_daily_df2.sum(axis=0)
myarray=np.array(x)
print(myarray)

labels=np.array(['Confirmed','Deaths','Recovered'])
color=np.array(['#F0AFE1','#69ADE3','#3D9740'])
fatality_rate=myarray[1]/myarray[0]*100;


'''Here the timeseries data will be uploaded and since in github it gets updated daily so no need to change the URL.
Basically 3 datas will be uploaded and then visualization of them will be done after cleaning.
3 datasets which will be uploaded will be of confirmed cases, deaths and recovered.
'''

timeseries_confirmed_df=pd.read_csv(confirmed_timeseries_url)
Bigpicture=timeseries_confirmed_df
timeseries_deaths_df=pd.read_csv(deaths_timeseries_url)
timeseries_recovered_df=pd.read_csv(recovered_timeseries_url)
new_timeseries_deaths_df=timeseries_deaths_df.drop(['Province/State','Lat','Long'],axis=1)
new_timeseries_deaths_df=new_timeseries_deaths_df.groupby(['Country/Region'],as_index=False).agg('sum')
x=new_timeseries_deaths_df
select_country = x[x['Country/Region'] == 'Mainland China']
select_country=select_country.loc[:,select_country.columns!='Country/Region']
x=select_country.T
mapping={x.columns[0]:'Deaths in Main Land China'}
z=x.rename(columns=mapping)
z=z.rename_axis('Date').reset_index()




#first figure starts
trace_Total=go.Bar(x=labels,
                   y=myarray,
                   name='Corona virus info',
                   opacity=.5,
                   marker=dict(color=color.tolist()),
                   width=0.3)
data=[trace_Total]
layout=dict(title="Info",
            showlegend=True)
fig=go.Figure(data=data, layout=layout)
#fig 1 ends


fig2=px.line(z,x='Date',y='Deaths in Main Land China')



m = folium.Map(location=[45.5236, -122.6750])
m.save('index.html')


app=dash.Dash()

app.layout=html.Div([
    html.Div(html.H1(children="hello")),
    html.H2("dash me"),
    html.Div(
        dcc.Graph(id="intial chart",
                  figure=fig)),
html.Div(
        dcc.Graph(id="second chart",
                  figure=fig2)),
    html.Div(html.Iframe(id='map',srcDoc=open('index.html','r').read(), width='100%',height='500'))

])
if __name__=='__main__':
    app.run_server(debug=True)
