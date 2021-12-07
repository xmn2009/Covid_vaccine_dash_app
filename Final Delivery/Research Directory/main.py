import dash
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime as dt
from dash import dash_table as table

# a header, a dropdown and a graph

es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#  create an app
app = dash.Dash(__name__, external_stylesheets=es)

# prepare data

# select delta variant
dfVariant = pd.read_csv('covid-variants.csv')
dfVariant = dfVariant[(dfVariant['variant'] == 'Delta')]

# parse date, select range and indexing
dfVariant['date'] = pd.to_datetime(dfVariant['date'])
dfVariant = dfVariant[(dfVariant['date'] > '2021-1-1') & (dfVariant['date'] <= '2021-10-16')]
dfVariant.set_index(dfVariant['date'], inplace=True)
# print(dfVariant.columns)

# read in full data

df = pd.read_csv("owid-covid-data (1).csv")

# parse date, select range and indexing
df['date'] = pd.to_datetime(df['date'])
df = df[(df['date'] > '2021-1-1') & (df['date'] <= '2021-10-16')]
df.set_index(df['date'], inplace=True)
# print(df.columns)

# below locations looks OK
location = ['Argentina', 'Austria', 'Brazil', 'Bulgaria', 'Cambodia', 'France', 'Germany', 'Ireland', 'Italy',
            'Japan', 'Kenya', 'Malaysia', 'Mexico', 'Netherlands', 'Nigeria', 'Poland', 'Portugal', 'South Africa',
            'Spain', 'United States']

# some style parameters
main_height = '60rem'

# layout
app.layout = html.Div(children=[

    html.Div(children=[
        html.H1(children='COVID19',
                className="",
                style={'textAlign': 'center', 'paddingTop': '2rem',
                       'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px',
                       'backgroundColor': '#f2f2f2', }),
    ]),

    ################### Filter box ######################
    html.Div(children=[
        html.Label('Filter by country:', style={'paddingTop': '2rem'}),
        dcc.Dropdown(
            id='input_ctry',
            options=[
                {'label': 'United States', 'value': '20'},
                {'label': 'Argentina', 'value': '1'},
                {'label': 'Austria', 'value': '2'},
                {'label': 'Brazil', 'value': '3'},
                {'label': 'Bulgaria', 'value': '4'},
                {'label': 'Cambodia', 'value': '5'},
                {'label': 'France', 'value': '6'},
                {'label': 'Germany', 'value': '7'},
                {'label': 'Ireland', 'value': '8'},
                {'label': 'Italy', 'value': '9'},
                {'label': 'Japan', 'value': '10'},
                {'label': 'Kenya', 'value': '11'},
                {'label': 'Malaysia', 'value': '12'},
                {'label': 'Mexico', 'value': '13'},
                {'label': 'Netherlands', 'value': '14'},
                {'label': 'Nigeria', 'value': '15'},
                {'label': 'Poland', 'value': '16'},
                {'label': 'Portugal', 'value': '17'},
                {'label': 'South Africa', 'value': '18'},
                {'label': 'Spain', 'value': '19'},
            ],
        ),

        html.Label('Filter by date (M-D-Y):', style={'paddingTop': '10rem'}),
        dcc.DatePickerRange(
            id='input_date',
            month_format='DD/MM/YYYY',
            show_outside_days=True,
            minimum_nights=0,
            initial_visible_month=dt(2021, 1, 1),
            min_date_allowed=dt(2021, 1, 1),
            max_date_allowed=dt(2021, 10, 1),
            start_date=dt.strptime("2021-01-01", "%Y-%m-%d").date(),
            end_date=dt.strptime("2021-10-1", "%Y-%m-%d").date()
        ),

        html.Label('Day of the week:', style={'paddingTop': '5rem'}),
        dcc.Dropdown(
            id='input_days',
            options=[
                {'label': 'Sun', 'value': '1'},
                {'label': 'Mon', 'value': '2'},
                {'label': 'Tue', 'value': '3'},
                {'label': 'Wed', 'value': '4'},
                {'label': 'Thu', 'value': '5'},
                {'label': 'Fri', 'value': '6'},
                {'label': 'Sat', 'value': '7'}
            ],
            value=['1', '2', '3', '4', '5', '6', '7'],
            multi=True
        ),

        html.Label('Choose of data:', style={'paddingTop': '5rem', 'display': 'inline-block'}),
        dcc.Checklist(
            id='input_num',
            options=[
                {'label': 'Total vaccinations', 'value': '1'},
                {'label': 'New cases', 'value': '2'},
                {'label': 'Delta variant', 'value': '3'},
                {'label': 'Hospital patients', 'value': '4'},
                {'label': 'ICU patients', 'value': '5'},
            ],
            value=['1', '2', '3', '4', '5'],
        ),

        # html.Label('Speed limits (mph):', style={'paddingTop': '2rem'}),
        # dcc.RangeSlider(
        #     id='input_speed_limit',
        #     min=20,
        #     max=70,
        #     step=10,
        #     value=[20, 70],
        #     marks={
        #         20: '20',
        #         30: '30',
        #         40: '40',
        #         50: '50',
        #         60: '60',
        #         70: '70'
        #     },
        # ),

    ], className="three columns",
        style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
               'marginTop': '2rem', 'backgroundColor': '#f2f2f2', 'height': main_height}),

    # HERE insert the code for four boxes & graph
    html.Div(children=[
        # Number of some statistics
        html.Div(children=[
            html.Div(children=[
                html.H3(id='t_vacc', style={'fontWeight': 'bold'}),
                html.Label('Total vaccinations', style={'paddingTop': '.3rem'}),
            ], className="two columns number-stat-box"),

            html.Div(children=[
                html.H3(id='new_case', style={'fontWeight': 'bold', 'color': '#f73600'}),
                html.Label('New cases', style={'paddingTop': '.3rem'}),
            ], className="two columns number-stat-box"),

            html.Div(children=[
                html.H3(id='delta', style={'fontWeight': 'bold', 'color': '#00aeef'}),
                html.Label('Delta variant', style={'paddingTop': '.3rem'}),
            ], className="two columns number-stat-box"),

            html.Div(children=[
                html.H3(id='hosp_p', style={'fontWeight': 'bold', 'color': '#a0aec0'}),
                html.Label('Hospital patients', style={'paddingTop': '.3rem'}),
            ], className="two columns number-stat-box"),

            html.Div(children=[
                html.H3(id='icu_p', style={'fontWeight': 'bold', 'color': '#a0aec0'}),
                html.Label('ICU patients', style={'paddingTop': '.3rem'}),
            ], className="two columns number-stat-box"),

        ], style={'margin': '2rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%',
                  'flex-wrap': 'wrap'}),

        # main image
        html.Div(children=[
            dcc.Graph(id='line_chart')
        ], className="twelve columns",
            style={'padding': '.3rem', 'marginTop': '1rem', 'marginLeft': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px',
                   'border-radius': '10px', 'backgroundColor': 'white', }),

        # the table
        html.Div(children=[
            html.Label('Granger Causality in Time Series ', style={'textAlign': 'center'}),
            # table.DataTable(
            #     id='tb',
            #     columns=['A', 'B', 'p_value (lag=4)', 'A cause B?']
            # )
        ], className="twelve columns",
            style={'padding': '.3rem', 'marginTop': '1rem', 'marginLeft': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px',
                   'border-radius': '10px', 'backgroundColor': 'white', })

    ], className="nine columns",
        style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
               'marginTop': '2rem', 'marginLeft': '2rem','backgroundColor': '#f2f2f2', 'height': main_height}),

], )

if __name__ == '__main__':
    app.run_server(debug=True)
