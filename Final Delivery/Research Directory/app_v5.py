import dash
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime
from dash import dash_table as table

# import dash_bootstrap_components as dbc
# import matplotlib.pyplot as plt
# import numpy as np
# import plotly.graph_objects as go

# css file
es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#  create an app
app = dash.Dash(__name__, external_stylesheets=es)

# below is necessary for heroku to run
server = app.server

# use dash_bootstrap to set up the css
# app = dash.Dash(external_stylesheets=[dbc.themes.MORPH])


# some style parameters
main_height = '60rem'
colors = {
    'background': '#E1F0EF',  # lightBlue
    'text': '#7FDBFF'
}

## layout
app.layout = html.Div(children=[

    # a title and subtitle
    html.Div(
        style={'textAlign': 'center',
               'padding': '3rem 1rem 1rem 1rem', 'margin': '1rem',
               'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
               'backgroundColor': colors['background'],
               },
        # className='twelve columns',
        children=[
            html.H1(children='COVID19 DATA TRACKER'),
            html.H5(children='Group L')
        ]),

    # a navigation bar
    html.Div(
        className="two columns",
        style={'padding': '1rem', 'margin': '2rem 1rem 1rem 1rem',
               'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
               'backgroundColor': colors['background'], 'height': main_height},
        children=[
            html.Label('Filter by country:', style={'paddingTop': '1rem'}),
            dcc.Dropdown(
                id='input_ctry',
                options=[
                    {'label': 'United States', 'value': 'United States'},
                    {'label': 'Argentina', 'value': 'Argentina'},
                    {'label': 'Austria', 'value': 'Austria'},
                    {'label': 'Brazil', 'value': 'Brazil'},
                    {'label': 'Bulgaria', 'value': 'Bulgaria'},
                    {'label': 'Cambodia', 'value': 'Cambodia'},
                    {'label': 'France', 'value': 'France'},
                    {'label': 'Germany', 'value': 'Germany'},
                    {'label': 'Ireland', 'value': 'Ireland'},
                    {'label': 'Italy', 'value': 'Italy'},
                    {'label': 'Japan', 'value': 'Japan'},
                    {'label': 'Kenya', 'value': 'Kenya'},
                    {'label': 'Malaysia', 'value': 'Malaysia'},
                    {'label': 'Mexico', 'value': 'Mexico'},
                    {'label': 'Netherlands', 'value': 'Netherlands'},
                    {'label': 'Nigeria', 'value': 'Nigeria'},
                    {'label': 'Poland', 'value': 'Poland'},
                    {'label': 'Portugal', 'value': 'Portugal'},
                    {'label': 'South Africa', 'value': 'South Africa'},
                    {'label': 'Spain', 'value': 'Spain'},
                ],
                value='United States',
            ),


            html.Label('Choose of data:', style={'paddingTop': '2rem', 'display': 'inline-block'}),
            dcc.Checklist(
                id='input_line',
                options=[
                    {'label': 'Total vaccinations', 'value': 'Total Vaccinations'},
                    {'label': 'New cases', 'value': 'New Cases'},
                    {'label': 'Hospital patients', 'value': 'Hospital Patients'},
                    {'label': 'ICU patients', 'value': 'ICU Patients'},
                    {'label': 'Delta variant', 'value': 'Delta Variant'},
                ],
                value=['Total Vaccinations', 'New Cases',
                       'Hospital Patients', 'ICU Patients',
                       'Delta Variant'],
            ),

            # slide bar
            html.Label('Month:', style={'paddingTop': '2rem'}),
            dcc.RangeSlider(
                id='input_month',
                min=1,
                max=9,
                step=1,
                value=[1, 9],
                marks={
                    # 0:  'Dec',
                    1: 'Jan',
                    2: 'Feb',
                    3: 'Mar',
                    4: 'Apr',
                    5: 'May',
                    6: 'Jun',
                    7: 'Jul',
                    8: 'Aug',
                    9: 'Sep'
                },
            ),

        ], ),  ##f2f2f2'

    # 2nd navigation bar
    html.Div(
        className="two columns",
        style={'padding': '1rem', 'margin': '2rem 1rem 1rem 1rem',
               'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
               'backgroundColor': colors['background'], 'height': main_height},
        children=[
            html.Label('Choose of data:', style={'paddingTop': '2rem', 'display': 'inline-block'}),
            dcc.RadioItems(
                id='input_age',
                options=[
                    {'label': 'All ages group', 'value': 'all_ages_adj'},
                    {'label': '12-17 group', 'value': '12-17'},
                    {'label': '18-29 group', 'value': '18-29'},
                    {'label': '30-49 group', 'value': '30-49'},
                    {'label': '50-64 group', 'value': '50-64'},
                    {'label': '65-79 group', 'value': '65-79'},
                    {'label': 'over 80 group', 'value': '80'}],
                value='all_ages_adj',
            ),

            html.Label('Choose of data:', style={'paddingTop': '2rem', 'display': 'inline-block'}),
            dcc.RadioItems(
                id='input_vtype',
                options=[
                    {'label': 'All types', 'value': 'all_types'},
                    {'label': 'Janssen', 'value': 'Janssen'},
                    {'label': 'Moderna', 'value': 'Moderna'},
                    {'label': 'Pfizer', 'value': 'Pfizer'}],
                value='all_types',
            ),

            html.Label('Choose of data:', style={'paddingTop': '2rem', 'display': 'inline-block'}),
            dcc.RadioItems(
                id='input_outcome',
                options=[
                    {'label': 'Deaths', 'value': 'death'},
                    {'label': 'Cases', 'value': 'case'},

                ],
                value='death',
            ),

        ], ),

    # main fig container
    html.Div(
        style={'padding': '2rem', 'margin': '2rem 1rem 1rem 1rem',
               'border-radius': '10px', 'boxShadow': '#e3e3e3 4px 4px 2px',
               'backgroundColor': '#f2f2f2', 'height': main_height},
        className="nine columns",
        children=[
            # five columns
            html.Div(
                style={'margin': '2rem', 'display': 'flex', 'flex-wrap': 'wrap',
                       'justify-content': 'space-between', 'width': '100%', },
                children=[
                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px'},
                        children=[
                            html.Label('Total Vaccinations', style={'paddingTop': '.3rem', }),
                            html.H6(id='num_t_vacc', style={'fontWeight': 'bold', 'color': 'blue'}),
                        ], className="two columns number-stat-box"),

                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px'},
                        children=[
                            html.Label('New Cases', style={'paddingTop': '.3rem'}),
                            html.H6(id='num_new_case', style={'fontWeight': 'bold', 'color': 'red'}),
                        ], className="two columns number-stat-box"),

                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px'},
                        children=[
                            html.Label('Hospital Patients', style={'paddingTop': '.3rem'}),
                            html.H6(id='num_hosp_p', style={'fontWeight': 'bold', 'color': 'green'}),
                        ], className="two columns number-stat-box"),

                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px'},
                        children=[
                            html.Label('ICU Patients', style={'paddingTop': '.3rem'}),
                            html.H6(id='num_icu_p', style={'fontWeight': 'bold', 'color': 'purple'}),
                        ], className="two columns number-stat-box"),

                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px', 'marginRight': '3rem', },
                        children=[
                            html.Label('Delta Variant', style={'paddingTop': '.3rem'}),
                            html.H6(id='num_delta', style={'fontWeight': 'bold', 'color': 'orange'}),
                        ], className="two columns number-stat-box"),
                ],
            ),

            # main image
            html.Div(
                style={'padding': '0.3rem', 'margin': '1rem 1rem 1rem 1.5rem',
                       'boxShadow': '#e3e3e3 4px 4px 2px',
                       'border-radius': '10px',
                       'backgroundColor': 'white'},
                children=[
                    dcc.Graph(id='line_chart')
                ],
            ),

            html.Div(
                style={'padding': '0.3rem', 'margin': '1rem 1rem 1rem 1.5rem',
                       'boxShadow': '#e3e3e3 4px 4px 2px',
                       'border-radius': '10px',
                       'backgroundColor': 'white'},
                children=[
                    dcc.Graph(id='line_chart1')
                ],
            ),

            # the stat table
            html.Div(
                style={'padding': '.3rem', 'margin': '1rem 1rem 1rem 1.5rem',
                       'boxShadow': '#e3e3e3 4px 4px 2px',
                       'border-radius': '10px', 'backgroundColor': 'white'},
                children=[
                    html.Label('Granger Causality in Time Series ', style={'textAlign': 'center'}),
                    # html.Div(children=[
                    #     dbc.Table('html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")])', bordered=True)
                    # ])
                    # table.DataTable(
                    #     id='tb',
                    #     columns=['A', 'B', 'p_value (lag=4)', 'A cause B?']
                    # )
                ], )
        ], )
])

# prepare data, put here, otherwise heroku will not load data
# select delta variant
dfVariant = pd.read_csv('covid-variants.csv')
dfVariant = dfVariant[(dfVariant['variant'] == 'Delta')]

# parse date, select range and indexing
dfVariant['date'] = pd.to_datetime(dfVariant['date'])
dfVariant = dfVariant[(dfVariant['date'] > '2021-1-1') & (dfVariant['date'] <= '2021-10-16')]
dfVariant = dfVariant[['date', 'location', 'num_sequences']]
dfVariant.set_index(dfVariant['date'], inplace=True)

# read in full data
df = pd.read_csv("owid-covid-data (1).csv")
# parse date, select range and indexing
df['date'] = pd.to_datetime(df['date'])
df = df[(df['date'] > '2021-1-1') & (df['date'] <= '2021-10-16')]
df = df[['date', 'location', 'total_vaccinations_per_hundred', 'hosp_patients_per_million',
         'icu_patients_per_million', 'new_cases', 'icu_patients', 'hosp_patients', 'total_vaccinations']]
df.set_index(df['date'], inplace=True)


@app.callback(
    Output(component_id='line_chart', component_property='figure'),
    [Input('input_ctry', 'value'),
     Input('input_month', 'value'),
     Input('input_line', 'value')])
def update_line_chart(ctry, month, lines):
    # resample into semi-month
    dfVariTemp = dfVariant[dfVariant['location'] == ctry].resample('sm').mean()
    dfTemp = df[df['location'] == ctry].resample('sm').mean()

    # merge df
    dfmerge = dfVariTemp.join(dfTemp)

    # normalize the data
    dfnorm = (dfmerge - dfmerge.min()) / (dfmerge.max() - dfmerge.min())
    dfnorm = dfnorm.reset_index()
    dfnorm.rename(columns={'date': 'Date',
                           'total_vaccinations_per_hundred': 'Total Vaccinations',
                           'new_cases': 'New Cases',
                           'hosp_patients_per_million': 'Hospital Patients',
                           'icu_patients_per_million': 'ICU Patients',
                           'num_sequences': 'Delta Variant'}, inplace=True)

    month_bott_limit = datetime.strptime(f'2021-{month[0]}-01', '%Y-%m-%d')
    month_top_limit = datetime.strptime(f'2021-{month[1] + 1}-01', '%Y-%m-%d')

    dfnorm = dfnorm[(dfnorm['Date'] >= month_bott_limit) & (dfnorm['Date'] <= month_top_limit)]

    fig = px.line(dfnorm,
                  x='Date',
                  y=lines,
                  markers=True)
    return fig


@app.callback(
    [Output('num_t_vacc', 'children'),
     Output('num_new_case', 'children'),
     Output('num_hosp_p', 'children'),
     Output('num_icu_p', 'children'),
     Output('num_delta', 'children'), ],
    [Input('input_ctry', 'value'),
     Input('input_month', 'value')]
)
def update_stat(ctry, month):
    # resample into semi-month
    dfVariTemp = dfVariant[dfVariant['location'] == ctry].resample('sm').mean()
    dfTemp = df[df['location'] == ctry].resample('sm').mean()

    # merge df
    dfmerge = dfVariTemp.join(dfTemp).reset_index().fillna(0)
    dfmerge = dfmerge.reset_index()
    dfmerge = dfmerge.fillna(0)

    month_bott_limit = datetime.strptime(f'2021-{month[0]}-01', '%Y-%m-%d')
    month_top_limit = datetime.strptime(f'2021-{month[1] + 1}-01', '%Y-%m-%d')
    # print(month, month_bott_imit, month_top_limit)

    dfmerge = dfmerge[(dfmerge['date'] >= month_bott_limit) & (dfmerge['date'] <= month_top_limit)]

    # print(ctry, '\n',
    #       dfmerge[['total_vaccinations', 'new_cases', 'hosp_patients', 'icu_patients', 'num_sequences']])

    num_t_vacc, num_n_case, num_hos_p, num_icu_p, num_delta_v = 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'
    num_t_vacc = int(dfmerge['total_vaccinations'].mean()) if dfmerge['total_vaccinations'].mean() != 0.0 else 'NaN'
    num_n_case = int(sum(dfmerge['new_cases'])) if sum(dfmerge['new_cases']) != 0.0 else 'NaN'
    num_hos_p = int(sum(dfmerge['hosp_patients'])) if sum(dfmerge['hosp_patients']) != 0.0 else 'NaN'
    num_icu_p = int(sum(dfmerge['icu_patients'])) if sum(dfmerge['icu_patients']) != 0.0 else 'NaN'
    num_delta_v = int(sum(dfmerge['num_sequences'])) if sum(dfmerge['num_sequences']) != 0.0 else 'NaN'

    return num_t_vacc, num_n_case, num_hos_p, num_icu_p, num_delta_v


dfvaccine = pd.read_csv("Rates_of_COVID-19_Cases_or_Deaths_by_Age_Group_and_Vaccination_Status.csv")
dfvaccine['year'] = '2021'
dfvaccine['date'] = pd.to_datetime(dfvaccine['year'].astype(str)
                                   + ' '
                                   + dfvaccine['mmwr_week'].astype(str)
                                   + ' 1',
                                   format='%Y %U %w')
# dfvaccine.set_index(dfvaccine['date'], inplace=True)
dfvaccine = dfvaccine[['date', 'outcome', 'vaccine_product', 'age_group', 'crude_vax_ir', 'crude_unvax_ir']]
dfvaccine = dfvaccine.ffill().bfill()
dfvaccine.rename(columns={'date': 'Date',
                          'outcome': 'Outcome',
                          'vaccine_product': 'Brand',
                          'age_group': 'Age',
                          'crude_vax_ir': 'Fully vaccinations',
                          'crude_unvax_ir': 'Un-vaccinations'}, inplace=True)


@app.callback(
    Output(component_id='line_chart1', component_property='figure'),
    [Input('input_outcome', 'value'),
     Input('input_vtype', 'value'),
     Input('input_age', 'value')]
)
def vaccines_update(outcome, input_vtype, input_age):
    dfvaccTemp = dfvaccine.copy(deep=True)
    dfOutput = dfvaccTemp[(dfvaccTemp['Outcome'] == outcome)
                          & (dfvaccTemp['Age'] == input_age)
                          & (dfvaccTemp['Brand'] == input_vtype)]
    print(dfOutput)

    fig1 = px.line(dfOutput,
                   x='Date',
                   y=['Fully vaccinations', 'Un-vaccinations'],
                   markers=True)
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)
