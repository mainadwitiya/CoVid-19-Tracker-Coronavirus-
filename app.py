import os
import pathlib
import re
import folium
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output, State
import dash_daq as daq
import gunicorn
import cufflinks as cf
import plotly.graph_objects as go
import pandas as pd

# Initialize app
external_stylesheets = [
    {
        'href': 'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.8.0/css/bulma.css',
        'rel': 'stylesheet',

    }
]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],

)


server = app.server
app.title = 'Covid-19 App'

# Load data
confirmed_timeseries_url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deaths_timeseries_url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
recovered_timeseries_url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
timeseries_confirmed_df=pd.read_csv(confirmed_timeseries_url)
timeseries_deaths_df=pd.read_csv(deaths_timeseries_url)
timeseries_recovered_df=pd.read_csv(recovered_timeseries_url)
#making this bigpicture stuff
'''new_timeseries_confirmed_df=timeseries_confirmed_df.drop(['Province/State'],axis=1)
new_timeseries_deaths_df=timeseries_deaths_df.drop(['Province/State'],axis=1)
new_timeseries_recovered_df=timeseries_recovered_df.drop(['Province/State'],axis=1)

new_timeseries_confirmed_df=new_timeseries_confirmed_df.groupby(['Country/Region'],as_index=False).agg('sum')
xc=new_timeseries_confirmed_df

new_timeseries_deaths_df=new_timeseries_deaths_df.groupby(['Country/Region'],as_index=False).agg('sum')
xd=new_timeseries_deaths_df

new_timeseries_recovered_df=new_timeseries_recovered_df.groupby(['Country/Region'],as_index=False).agg('sum')
xr=new_timeseries_recovered_df

def confirmed_by_country(country):
    cdf = xc[(xc["Country/Region"] == country)][xc.columns[4:]].T
    cdf = cdf.rename(columns={cdf.columns[0]: 'confirmed'})
    fig_confirmed = go.Figure()
    fig_confirmed.add_trace(go.Scatter(x=cdf.index, y=cdf['confirmed'], name="Confirmed",
                                 line_color='#9970AB',
                                 mode='lines+markers'))
    fig_confirmed.update_layout(title="Confirmed cases timeseries in "+country, template="plotly_dark",
                                      xaxis_title="Dates in mm/dd/yy",
                                      yaxis_title="Confirmed Count", showlegend=True)
    return(fig_confirmed)

def deaths_by_country(country):
    ddf = xd[(xd["Country/Region"] == country)][xd.columns[4:]].T
    ddf = ddf.rename(columns={ddf.columns[0]: 'deaths'})
    fig_deaths=go.Figure()
    fig_deaths.add_trace(go.Scatter(x=ddf.index, y=ddf['deaths'], name="Deaths",
                                 line_color='#FC4E2A',
                                 mode='lines+markers'))
    fig_deaths.update_layout(title="Number of deaths timeseries in " + country, template="plotly_dark",
                                xaxis_title="Dates in mm/dd/yy",
                                yaxis_title="Death Count", showlegend=True)
    return(fig_deaths)

def recovered_by_country(country):
    rdf = xr[(xr["Country/Region"] == country)][xr.columns[4:]].T
    rdf = rdf.rename(columns={rdf.columns[0]: 'Recovered'})
    fig_recovered=go.Figure()
    fig_recovered.add_trace(go.Scatter(x=rdf.index, y=rdf['Recovered'], name="Recovered",
                                 line_color='#FC4E2A',
                                 mode='lines+markers'))
    fig_recovered.update_layout(title="Number of recovery timeseries in " + country, template="plotly_dark",
                                xaxis_title="Dates in mm/dd/yy",
                                yaxis_title="Recovered Count", showlegend=True)
    return(fig_recovered)

def fatality_rate_by_country(country):
    cdf = xc[(xc["Country/Region"] == country)][xc.columns[4:]].T
    cdf = cdf.rename(columns={cdf.columns[0]: 'confirmed'})
    ddf = xd[(xd["Country/Region"] == country)][xd.columns[4:]].T
    ddf = ddf.rename(columns={ddf.columns[0]: 'deaths'})
    fatality_dataframe=pd.DataFrame()
    fatality_dataframe["fatality"]=ddf["deaths"]/cdf["confirmed"]*100
    fig_fatality=go.Figure()
    fig_fatality.add_trace(go.Scatter(x=fatality_dataframe.index, y=fatality_dataframe['Recovered'], name="Fatality",
                                       line_color='#FC4E2A',
                                       mode='lines+markers'))
    fig_fatality.update_layout(title="Fatality rate of " + country +" in percentage" , template="plotly_dark",
                                xaxis_title="Dates in mm/dd/yy",
                                yaxis_title="Fatality rate", showlegend=True)
    return (fig_fatality)










colordict = {0: 'lightblue', 1: 'lightgreen', 2: 'orange', 3: 'red'}
#FOLIUM MAP EPIC
world_map = folium.Map(location=[32, 53], zoom_start=4, min_zoom=1, tiles='Stamen Toner')

for lat, lon, value1, value2, value3,value4, name, province in zip(Big_picture['Lat'], Big_picture['Long'],
                                                            Big_picture['total confirmed'], Big_picture['total deaths'],
                                                            Big_picture['total recovered'],
                                                            Big_picture['Active cases'],
                                                            Big_picture['Country/Region'],
                                                            Big_picture['Province/State']):
    folium.CircleMarker([lat, lon],

                        radius=10,


                        popup=('<strong>Province/State</strong>: ' + str(province).capitalize() + '<br>'
                                                                                                  '<strong>Country</strong>: ' + str(
                            name).capitalize() + '<br>'
                                                 '<strong>Confirmed Cases</strong>: ' + str(value1) + '<br>'
                                                                                                      '<strong>Deaths</strong>: ' + str(value2) + '<br>''<strong>Recovered</strong>: '
                               + str(value3) + '<br>'
                               '<strong>Active cases</strong>: '+str(value4)+'<br>'),
                        color='red',

                        fill_color='#D73027',
                        fill_opacity=0.7).add_to(world_map)
world_map.save('index.html')


#FINAL BAR GRAPHCOMPARISON
total_new = pd.DataFrame()
total_new['Confirmed']=int
total_new['Deaths']=int
total_new['Recovered']=int

total_confirmed=Big_picture['total confirmed'].sum(axis=0)
total_deaths=Big_picture['total deaths'].sum(axis=0)
total_recovered=Big_picture['total recovered'].sum(axis=0)
labels=np.array(['Confirmed','Deaths','Recovered'])
value_total=[total_confirmed,total_deaths,total_recovered]

value_china=[allconfirmed_china,alldeaths_china,allrecovered_china]

value_rest=[abs(total_confirmed-allconfirmed_china),abs(total_deaths-alldeaths_china),abs(total_recovered-allrecovered_china)]


fig = go.Figure()
fig.add_trace(go.Bar(x=labels,
                y=value_total,
                name='TOTAL',
                marker_color='rgb(55, 83, 109)',
                     text=value_total
                ))
fig.add_trace(go.Bar(x=labels,
                y=value_china,
                name='China',
                marker_color='#B51F09',
                     text=value_china
                ))
fig.add_trace(go.Bar(x=labels,
                y=value_rest,
                name='Rest of the World',
                marker_color='#684E72',
                     text=value_rest
                ))
fig.update_layout(
    title='Comparison of China and Rest of th world',

    yaxis=dict(
        title='Count',
        ))
fig.update_traces(textposition='outside')









DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8

#PROVIDING LIST FOR MY GRAPHS

graph_list=["fig_all","fig","fig_china_confirmed","fig_china_deaths","fig_china_recovered","fig_china_fatality"]
# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(id="logo", children="Total Cases-" + str(total_confirmed)),

                html.H4(children="Covid-19 Tracker"),
                html.P(
                    id="description",
                    children="Coronaviruses (CoV) are a large family of viruses that cause illness ranging from the\
                             common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS-CoV)\
                             and Severe Acute Respiratory Syndrome (SARS-CoV).A novel coronavirus (nCoV) is a new\
                             strain that has not been previously identified in humans.\
                             Project is under development new changes soon and is opne for contributions\
                             Contributors can fork it from https://github.com/mainadwitiya/CoVid-19-Tracker-Coronavirus-"

                ),

            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("No. Of Deaths"), html.P(str(total_deaths))],

                                    id="wells",
                                    className="mini_container",
                                ),

                            ],
                            id="info-container",
                            className="row container-display",
                        ),

                        html.Div(

                            html.Div(html.Iframe(id='map', srcDoc=open('index.html', 'r').read(), width='100%',
                                                 height='500'))),

                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select graph:"),
                        dcc.Dropdown(
                            id="dropdown",

                            options=[
                                {
                                    "label": "Time Series graph of Covid-19 Outbreak in",
                                    "value": "",
                                },
                                {
                                    "label": "Bar chart for comparison of outbreak between  and ROW",
                                    "value": "fig",
                                },
                                {
                                    "label": "Time Series graph of Confirmed Cases",
                                    "value": "fig_china_confirmed",
                                },
                                {
                                    "label": "Time Series graph of Death toll",
                                    "value": "fig_china_deaths",
                                },
                                {
                                    "label": "Time Series graph of Recovered Patients",
                                    "value": "fig_china_recovered",
                                },
                                {
                                    "label": "Time Series Graph of Fatality Rate",
                                    "value": "fig_china_fatality",
                                },
                            ],
                            value=graph_list[0],
                        ),
                        dcc.Graph(id="graph"),

                    ],
                ),

                html.Div(

                )

            ],
        ),

    ],

)


@app.callback(
    Output(component_id="graph", component_property="figure"),
    [Input(component_id="dropdown", component_property="value")],
)
def update_output_div(input_value):
    if input_value == "fig_all":
        return fig_all

    if input_value == "fig":
        return fig

    if input_value == "fig_china_confirmed":
        return fig_china_confirmed

    if input_value == "fig_china_deaths":
        return fig_china_deaths

    if input_value == "fig_china_recovered":
        return fig_china_recovered

    if input_value == "fig_china_fatality":
        return fig_china_fatality


if __name__ == "__main__":
    app.run_server(debug=True)'''
Bigpicture = timeseries_confirmed_df
timeseries_deaths_df = pd.read_csv(deaths_timeseries_url)
timeseries_recovered_df = pd.read_csv(recovered_timeseries_url)
new_timeseries_confirmed_df = timeseries_confirmed_df.drop(['Province/State', 'Lat', 'Long'], axis=1)
new_timeseries_deaths_df = timeseries_deaths_df.drop(['Province/State', 'Lat', 'Long'], axis=1)
new_timeseries_recovered_df = timeseries_recovered_df.drop(['Province/State', 'Lat', 'Long'], axis=1)

# GETTING CONFIRMED CASES FOR CHINA

new_timeseries_confirmed_df = new_timeseries_confirmed_df.groupby(['Country/Region'], as_index=False).agg('sum')
xc = new_timeseries_confirmed_df
select_country_1 = xc[xc['Country/Region'] == 'China']
select_country_1 = select_country_1.loc[:, select_country_1.columns != 'Country/Region']
xc = select_country_1.T
mapping = {xc.columns[0]: 'Confirmed cases in Main Land China'}
zc = xc.rename(columns=mapping)
zc = zc.rename_axis('Date').reset_index()

# GETTING DEATHS IN CHINA

new_timeseries_deaths_df = new_timeseries_deaths_df.groupby(['Country/Region'], as_index=False).agg('sum')
xd = new_timeseries_deaths_df
select_country_2 = xd[xd['Country/Region'] == 'China']
select_country_2 = select_country_2.loc[:, select_country_2.columns != 'Country/Region']
xd = select_country_2.T
mapping = {xd.columns[0]: 'Deaths in Main Land China'}
zd = xd.rename(columns=mapping)
zd = zd.rename_axis('Date').reset_index()

# Getting Recovery in China######################################################################################


new_timeseries_recovered_df = new_timeseries_recovered_df.groupby(['Country/Region'], as_index=False).agg('sum')
xr = new_timeseries_recovered_df
select_country_3 = xr[xr['Country/Region'] == 'China']
select_country_3 = select_country_3.loc[:, select_country_3.columns != 'Country/Region']
xr = select_country_3.T
mapping = {xr.columns[0]: 'Recovered in Main Land China'}
zr = xr.rename(columns=mapping)
zr = zr.rename_axis('Date').reset_index()

# MAKING OF CHINA FRAME################################################################################################


CHINA_MAIN_FRAME = zc.iloc[:, 0:2]
CHINA_MAIN_FRAME['Deaths in MainLand China'] = zd.iloc[:, 1:2]
CHINA_MAIN_FRAME['Recovered in MainLand China'] = zr.iloc[:, 1:2]
CHINA_MAIN_FRAME['Fatality Rate'] = CHINA_MAIN_FRAME['Deaths in MainLand China'] / CHINA_MAIN_FRAME[
    'Confirmed cases in Main Land China'] * 100

# FIGURE NO 1 CONFIRMED CASES FIGURE##############################################################################################
fig_china_confirmed = go.Figure()
fig_china_confirmed.add_trace(
    go.Scatter(x=CHINA_MAIN_FRAME['Date'], y=CHINA_MAIN_FRAME['Confirmed cases in Main Land China'], name="Confirmed",
               line_color='#9970AB', mode='lines+markers'))
fig_china_confirmed.update_layout(title="Confirmed cases timeseries in china", template="plotly_dark",
                                  xaxis_title="Dates in mm/dd/yy",
                                  yaxis_title="Confirmed Count", showlegend=True)

# FIGURE NO 2 DEATH FIGURE #######################################################################################################
fig_china_deaths = go.Figure()

fig_china_deaths.add_trace(
    go.Scatter(x=CHINA_MAIN_FRAME['Date'], y=CHINA_MAIN_FRAME['Deaths in MainLand China'], name="Deaths",
               line_color='#FC4E2A', mode='lines+markers'))
fig_china_deaths.update_layout(title="Deaths timeseries in china", template="plotly_dark",
                               xaxis_title="Dates in mm/dd/yy",
                               yaxis_title="Death count", showlegend=True)

# FIGURE NO 3 RECOVERY FIGURE#################################################################################################

fig_china_recovered = go.Figure()

fig_china_recovered.add_trace(
    go.Scatter(x=CHINA_MAIN_FRAME['Date'], y=CHINA_MAIN_FRAME['Recovered in MainLand China'], name="Recovered",
               line_color='#B8E186', mode='lines+markers'))
fig_china_recovered.update_layout(title="Recovered timeseries in china", template="plotly_dark",
                                  xaxis_title="Dates in mm/dd/yy",
                                  yaxis_title="Recovered count", showlegend=True)

# FIGURE NO 4 FATALITY RATE####################################################################################################
fig_china_fatality = go.Figure()
fig_china_fatality.add_trace(
    go.Scatter(x=CHINA_MAIN_FRAME['Date'], y=CHINA_MAIN_FRAME['Fatality Rate'], name="Fatality Rate",
               line_color='#FECC5C', mode='lines+markers'))
fig_china_fatality.update_layout(title="Fatality Rate timeseries in china", template="plotly_dark",
                                 xaxis_title="Dates in mm/dd/yy",
                                 yaxis_title="Rate in Percentage", showlegend=True)

# FIGURE 5 china all######################################################################################################

# SCATTER PLOT FOR CHINA CONTAINS ALL
import plotly.graph_objects as go
import pandas as pd

fig_all = go.Figure()
fig_all.add_trace(
    go.Scatter(x=CHINA_MAIN_FRAME['Date'], y=CHINA_MAIN_FRAME['Confirmed cases in Main Land China'], name="Confirmed",
               line_color='#9970AB',
               mode='lines+markers'))

fig_all.add_trace(go.Scatter(x=CHINA_MAIN_FRAME['Date'], y=CHINA_MAIN_FRAME['Deaths in MainLand China'], name="Deaths",
                             line_color='#FC4E2A',
                             mode='lines+markers'))
fig_all.add_trace(
    go.Scatter(x=CHINA_MAIN_FRAME['Date'], y=CHINA_MAIN_FRAME['Recovered in MainLand China'], name="Recovered",
               line_color='#B8E186',
               mode='lines+markers'))
fig_all.update_layout(title="Plot for corona virus cases in china", template="plotly_dark",
                      xaxis_title="Dates in mm/dd/yy",
                      yaxis_title="Count", showlegend=True)

# more DATA MANIPULATION

timeseries_confirmed_df2 = timeseries_confirmed_df[timeseries_confirmed_df['Country/Region'] == 'China']
timeseries_deaths_df2 = timeseries_deaths_df[timeseries_confirmed_df['Country/Region'] == 'China']
timeseries_recovered_df2 = timeseries_recovered_df[timeseries_confirmed_df['Country/Region'] == 'China']
mainland_china = timeseries_confirmed_df2
mainland_china['total confirmed'] = timeseries_confirmed_df2.iloc[:, -1:].sum(axis=1)
mainland_china['total deaths'] = timeseries_deaths_df2.iloc[:, -1:].sum(axis=1)
mainland_china['total recovered'] = timeseries_recovered_df2.iloc[:, -1:].sum(axis=1)
allconfirmed_china = mainland_china['total confirmed'].sum()
alldeaths_china = mainland_china['total deaths'].sum()
allrecovered_china = mainland_china['total recovered'].sum()
Big_picture = timeseries_confirmed_df
Big_picture = Big_picture.iloc[:, np.r_[0:4]]
Big_picture['total confirmed'] = timeseries_confirmed_df.iloc[:, -1:]
Big_picture['total deaths'] = timeseries_deaths_df.iloc[:, -1:]
Big_picture['total recovered'] = timeseries_recovered_df.iloc[:, -1:]
print(Big_picture['total confirmed'])
df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
df_confirmed = df_confirmed.rename(columns={"Province/State":"state","Country/Region": "country"})

world_map = folium.Map(location=[10,0], tiles="Stamen Toner", zoom_start=2,max_zoom=6,min_zoom=2)
for i in range(0,len(df_confirmed)):
    folium.Circle(
        location=[df_confirmed.iloc[i]['Lat'], df_confirmed.iloc[i]['Long']],
        tooltip = "<h5 style='text-align:center;font-weight: bold'>"+df_confirmed.iloc[i]['country']+"</h5>"+

                    "<hr style='margin:10px;'>"+
                    "<ul style='color: #444;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
        "<li>Confirmed: "+str(df_confirmed.iloc[i,-1])+"</li>"+
        "<li>Deaths:   "+str(df_deaths.iloc[i,-1])+"</li>"+
        "<li>Mortality Rate:   "+str(np.round(df_deaths.iloc[i,-1]/(df_confirmed.iloc[i,-1]+1.00001)*100,2))+"</li>"+
                  "<hr style='margin:10px;'>" 
        "</ul>"
        ,
        radius=(int((np.log(df_confirmed.iloc[i,-1]+1.00001)))+0.2)*50000,
        color='#D73027',
        fill_color='#ff8533',
        fill_opacity=0.5).add_to(world_map)

world_map.save('index.html')



# FINAL BAR GRAPHCOMPARISON
total_new = pd.DataFrame()
total_new['Confirmed'] = int
total_new['Deaths'] = int
total_new['Recovered'] = int

total_confirmed = Big_picture['total confirmed'].sum(axis=0)
total_deaths = Big_picture['total deaths'].sum(axis=0)
total_recovered = Big_picture['total recovered'].sum(axis=0)
labels = np.array(['Confirmed', 'Deaths', 'Recovered'])
value_total = [total_confirmed, total_deaths, total_recovered]

value_china = [allconfirmed_china, alldeaths_china, allrecovered_china]

value_rest = [abs(total_confirmed - allconfirmed_china), abs(total_deaths - alldeaths_china),
              abs(total_recovered - allrecovered_china)]

fig = go.Figure()
fig.add_trace(go.Bar(x=labels,
                     y=value_total,
                     name='TOTAL',
                     marker_color='rgb(55, 83, 109)',
                     text=value_total
                     ))
fig.add_trace(go.Bar(x=labels,
                     y=value_china,
                     name='China',
                     marker_color='#B51F09',
                     text=value_china
                     ))
fig.add_trace(go.Bar(x=labels,
                     y=value_rest,
                     name='Rest of the World',
                     marker_color='#684E72',
                     text=value_rest
                     ))
fig.update_layout(
    title='Comparison of China and Rest of th world',

    yaxis=dict(
        title='Count',
    ))
fig.update_traces(textposition='outside')

DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8

# PROVIDING LIST FOR MY GRAPHS

graph_list = ["fig_all", "fig", "fig_china_confirmed", "fig_china_deaths", "fig_china_recovered", "fig_china_fatality"]
# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(id="logo", children="Total Cases-" + str(total_confirmed)),

                html.H4(children="Covid-19 Tracker"),
                html.P(
                    id="description",
                    children="Coronaviruses (CoV) are a large family of viruses that cause illness ranging from the\
                             common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS-CoV)\
                             and Severe Acute Respiratory Syndrome (SARS-CoV).A novel coronavirus (nCoV) is a new\
                             strain that has not been previously identified in humans.\
                             Project is under development new changes soon and is opne for contributions\
                             Contributors can fork it from https://github.com/mainadwitiya/CoVid-19-Tracker-Coronavirus-"

                ),

            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("No. Of Deaths"), html.P(str(total_deaths))],

                                    id="wells",
                                    className="mini_container",
                                ),

                            ],
                            id="info-container",
                            className="row container-display",
                        ),

                        html.Div(

                            html.Div(html.Iframe(id='map', srcDoc=open('index.html', 'r').read(), width='100%',
                                                 height='500'))),

                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select graph:"),
                        dcc.Dropdown(
                            id="dropdown",

                            options=[
                                {
                                    "label": "Time Series graph of Covid-19 Outbreak in China(day wise)",
                                    "value": "fig_all",
                                },
                                {
                                    "label": "Bar chart for comparison of outbreak between China and ROW",
                                    "value": "fig",
                                },
                                {
                                    "label": "Time Series graph of Confirmed Cases (China)",
                                    "value": "fig_china_confirmed",
                                },
                                {
                                    "label": "Time Series graph of Death toll (China)",
                                    "value": "fig_china_deaths",
                                },
                                {
                                    "label": "Time Series graph of Recovered Patients(China)",
                                    "value": "fig_china_recovered",
                                },
                                {
                                    "label": "Time Series Graph of Fatality Rate(China)",
                                    "value": "fig_china_fatality",
                                },
                            ],
                            value=graph_list[0],
                        ),
                        dcc.Graph(id="graph"),

                    ],
                ),

                html.Div(

                )

            ],
        ),

    ],

)


@app.callback(
    Output(component_id="graph", component_property="figure"),
    [Input(component_id="dropdown", component_property="value")],
)
def update_output_div(input_value):
    if input_value == "fig_all":
        return fig_all

    if input_value == "fig":
        return fig

    if input_value == "fig_china_confirmed":
        return fig_china_confirmed

    if input_value == "fig_china_deaths":
        return fig_china_deaths

    if input_value == "fig_china_recovered":
        return fig_china_recovered

    if input_value == "fig_china_fatality":
        return fig_china_fatality


if __name__ == "__main__":
    app.run_server(debug=True)