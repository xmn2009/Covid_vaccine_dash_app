import dash
import pandas
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime as dt
from dash import dash_table as table
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt

# css file
es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#  create an app
app = dash.Dash(__name__, external_stylesheets=es)

# use dash_bootstrap to set up the css
# app = dash.Dash(external_stylesheets=[dbc.themes.MORPH])

# some style parameters
main_height = '60rem'
colors = {
    'background': 'lightBlue',
    'text': '#7FDBFF'
}

## layout
app.layout = html.Div(children=[

    # a title
    html.H1(children='COVID19',
            className="",
            style={'textAlign': 'center', 'paddingTop': '2rem',
                   'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px',
                   'backgroundColor': colors['background'], 'border-radius': '10px'}),

    # a navigation bar
    html.Div(children=[
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

        html.Label('Filter by date (M-D-Y):', style={'paddingTop': '16rem'}),
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

        html.Label('Day of the week:', style={'paddingTop': '2rem'}),
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

        # html.Label('Choose of data:', style={'paddingTop': '2rem', 'display': 'inline-block'}),
        # dcc.Checklist(
        #     id='input_line',
        #     options=[
        #         {'label': 'Total vaccinations', 'value': '1'},
        #         {'label': 'New cases', 'value': '2'},
        #         {'label': 'Delta variant', 'value': '3'},
        #         {'label': 'Hospital patients', 'value': '4'},
        #         {'label': 'ICU patients', 'value': '5'},
        #     ],
        #     value=['1', '2', '3', '4', '5'],
        # ),

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

    ], className="three columns",
        style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
               'marginTop': '2rem', 'backgroundColor': 'lightBlue', 'height': main_height}),  ##f2f2f2'

    # main fig and stat
    html.Div(children=[

        # five columns
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
            style={'padding': '.3rem', 'marginTop': '1rem', 'marginLeft': '1rem',
                   'boxShadow': '#e3e3e3 4px 4px 2px',
                   'border-radius': '10px', 'backgroundColor': 'white', }),

        # the stat table
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
               'marginTop': '2rem', 'marginLeft': '2rem', 'backgroundColor': '#f2f2f2', 'height': main_height}),

])


@app.callback(
    Output(component_id='line_chart', component_property='figure'),
    [Input('input_ctry', 'value'),
     Input('input_month', 'value')])
def update_line_chart(ctry, month):
    # resample into semi-month
    dfVariTemp = dfVariant[dfVariant['location'] == ctry].resample('sm').mean()
    dfTemp = df[df['location'] == ctry].resample('sm').mean()

    # merge df
    dfmerge = dfVariTemp.join(dfTemp)
    # print(dfmerge.index)
    # dfmerge.reset_index()

    # normalize the data
    dfnorm = (dfmerge - dfmerge.min()) / (dfmerge.max() - dfmerge.min())
    # print(dfnorm.index.month)
    dfnorm.rename(columns={'total_vaccinations_per_hundred': 'Total Vaccinations',
                           'new_cases': 'New Cases',
                           'hosp_patients_per_million': 'Hospital Patients',
                           'icu_patients_per_million': 'ICU Patients',
                           'num_sequences': 'Delta Variant'}, inplace=True)

    month_bott_imit = month[0]
    month_top_limit = month[1]

    print(month, month_bott_imit, month_top_limit)

    # dfnorm = dfnorm[dfnorm.index < month_limit]
    print(dfnorm)

    fig = px.line(dfnorm,
                  y=['Total Vaccinations',
                     'New Cases',
                     'Hospital Patients',
                     'ICU Patients',
                     'Delta Variant'],
                  markers=True)

    return fig


if __name__ == '__main__':
    # prepare data
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
             'icu_patients_per_million', 'new_cases']]
    df.set_index(df['date'], inplace=True)

    app.run_server(debug=True)
