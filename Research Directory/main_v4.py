import dash
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime
from dash import dash_table

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

# some style parameters
main_height = 'auto'
colors = {
    'blue_back': '#E1F0EF',
    'gray_back': '#f2f2f2',
    'text': '#7FDBFF'
}

# layout
app.layout = html.Div(children=[

    # a title and subtitle
    html.Div(
        style={'textAlign': 'center',
               'padding': '2rem', 'margin': '1rem',
               'border-radius': '10px', 'boxShadow': '#e3e3e3 4px 4px 2px',
               'backgroundColor': colors['blue_back'], 'height': 'auto',
               },
        className='twelve columns',
        children=[
            html.H1(children='COVID19 DATA TRACKER'),
            html.H5(children='Group L')
        ]),

    # 5 statistic box
    html.Div(
        style={'textAlign': 'center', 'display': 'flex',
               'padding': '1rem', 'margin': '1rem',
               'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
               'backgroundColor': colors['gray_back'], 'height': 'auto',
               },
        className='twelve columns',
        children=[
            html.Div(
                style={'margin': '2rem', 'display': 'flex', 'flex-wrap': 'wrap',
                       'justify-content': 'space-between', 'width': '100%',
                       'height': 'auto', },
                children=[
                    # total vaccinations
                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px',
                               'backgroundColor': colors['blue_back'],
                               'width': '200px'},
                        children=[
                            html.Label('Total Vaccinations', style={'paddingTop': '.3rem', }),
                            html.H6(id='num_t_vacc', style={'fontWeight': 'bold', 'color': 'blue'}),
                        ], className="two columns number-stat-box"),

                    # New Cases
                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px',
                               'backgroundColor': colors['blue_back'],
                               'width': '200px'},
                        children=[
                            html.Label('New Cases', style={'paddingTop': '.3rem'}),
                            html.H6(id='num_new_case', style={'fontWeight': 'bold', 'color': 'red'}),
                        ], className="two columns number-stat-box"),

                    # Hospital Patients
                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px',
                               'backgroundColor': colors['blue_back'],
                               'width': '200px'},
                        children=[
                            html.Label('Hospital Patients', style={'paddingTop': '.3rem'}),
                            html.H6(id='num_hosp_p', style={'fontWeight': 'bold', 'color': 'green'}),
                        ], className="two columns number-stat-box"),

                    # ICU Patients
                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px',
                               'backgroundColor': colors['blue_back'],
                               'width': '200px'},
                        children=[
                            html.Label('ICU Patients', style={'paddingTop': '.3rem'}),
                            html.H6(id='num_icu_p', style={'fontWeight': 'bold', 'color': 'purple'}),
                        ], className="two columns number-stat-box"),

                    # Delta variant
                    html.Div(
                        style={'boxShadow': '#e3e3e3 4px 4px 2px',
                               'backgroundColor': colors['blue_back'],
                               'width': '200px'},
                        children=[
                            html.Label('Delta Variant', style={'paddingTop': '.3rem'}),
                            html.H6(id='num_delta', style={'fontWeight': 'bold', 'color': 'orange'}),
                        ], className="two columns number-stat-box"),
                ],
            ),
        ]),

    # top main fig container
    html.Div(
        style={'padding': '2rem', 'margin': '1rem',
               'display': 'flex',
               'border-radius': '10px', 'boxShadow': '#e3e3e3 4px 4px 2px',
               'backgroundColor': colors['gray_back'], 'height': 'auto'},
        className="twelve columns",
        children=[
            # 1st navigation bar
            html.Div(
                className="three columns",
                style={'padding': '2rem', 'margin': '2rem', 'display': 'inline-block',
                       'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
                       'backgroundColor': colors['blue_back'], 'height': 'auto'},
                children=[
                    html.Label('Filter by country:',
                               style={'fontWeight': 'bold',
                                      'marginTop': '2rem'}),
                    dcc.Dropdown(
                        style={'paddingLeft': '2rem', 'marginRight': '4rem', },
                        id='input_ctry',
                        options=[
                            {'label': 'United States', 'value': 'United States'},
                            {'label': 'Austria', 'value': 'Austria'},
                            {'label': 'Bulgaria', 'value': 'Bulgaria'},
                            {'label': 'France', 'value': 'France'},
                            {'label': 'Germany', 'value': 'Germany'},
                            {'label': 'Italy', 'value': 'Italy'},
                            {'label': 'Netherlands', 'value': 'Netherlands'},
                            {'label': 'Portugal', 'value': 'Portugal'},
                            {'label': 'Spain', 'value': 'Spain'},
                        ],
                        value='United States',
                    ),

                    html.Label('Choose of line:',
                               style={'marginTop': '3rem', 'fontWeight': 'bold'}),
                    dcc.Checklist(
                        style={'paddingLeft': '2rem'},
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
                    html.Label('Month:',
                               style={'marginTop': '3rem', 'fontWeight': 'bold'}),
                    dcc.RangeSlider(
                        id='input_month',
                        min=1,
                        max=9,
                        step=1,
                        value=[1, 9],
                        marks={
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

                ], ),
            # 1st main image
            html.Div(
                className="nine columns",
                style={'margin': '2rem', 'display': 'inline-block',
                       'boxShadow': '#e3e3e3 4px 4px 2px',
                       'border-radius': '10px',
                       'backgroundColor': 'white',
                       'height': 'auto'},
                children=[
                    html.Label(id='top_fig_title',
                               style={'marginTop': '2rem',
                                      'fontWeight': 'bold',
                                      'textAlign': 'center'}),
                    dcc.Graph(id='top_line_chart')
                ],
            ),

        ]),

    # table container
    html.Div(
        style={'padding': '2rem', 'margin': '1rem',
               'border-radius': '10px', 'boxShadow': '#e3e3e3 4px 4px 2px',
               'backgroundColor': colors['blue_back'], 'height': 'auto',
               },
        className="twelve columns",
        children=[
            # the stat table
            html.Div(
                style={'padding': '1rem', 'margin': '1rem',
                       'boxShadow': '#e3e3e3 4px 4px 2px',
                       'border-radius': '10px', 'backgroundColor': 'white',
                       'display': 'center', 'width': 'auto'},
                children=[
                    html.Label(id='table_ctry',
                               style={'textAlign': 'center',
                                      'padding': '1rem',
                                      'fontWeight': 'bold'}),
                    dash_table.DataTable(id='newstable',
                                         style_header={'textAlign': 'center'},
                                         style_data={
                                             'whiteSpace': 'normal',
                                             'height': 'auto',
                                             'lineHeight': '15px',
                                             'textAlign': 'center'}),

                ], )
        ]),

    # bottom main fig container
    html.Div(
        style={'padding': '2rem', 'margin': '1rem',
               'display': 'flex',
               'border-radius': '10px', 'boxShadow': '#e3e3e3 4px 4px 2px',
               'backgroundColor': colors['gray_back'], 'height': 'auto'},
        className="twelve columns",
        children=[
            # 2nd navigation bar
            html.Div(
                className="three columns",
                style={'padding': '1rem 2rem 1rem 2rem', 'margin': '2rem',
                       'display': 'inline-block',
                       'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
                       'backgroundColor': colors['blue_back'], 'height': 'auto'},
                children=[
                    html.Label('Age Group:',
                               style={'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        style={'paddingLeft': '2rem'},
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

                    html.Label('Vaccine Brand:',
                               style={'paddingTop': '1rem',
                                      'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        style={'paddingLeft': '2rem'},
                        id='input_vtype',
                        options=[
                            {'label': 'All types', 'value': 'all_types'},
                            {'label': 'Janssen', 'value': 'Janssen'},
                            {'label': 'Moderna', 'value': 'Moderna'},
                            {'label': 'Pfizer', 'value': 'Pfizer'}],
                        value='all_types',
                    ),

                    html.Label('Choose of data:',
                               style={'paddingTop': '1rem',
                                      'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        style={'paddingLeft': '2rem'},
                        id='input_outcome',
                        options=[
                            {'label': 'Deaths', 'value': 'death'},
                            {'label': 'Cases', 'value': 'case'},
                        ],
                        value='death',
                    ),
                ],
            ),
            # 2nd main image
            html.Div(
                className="nine columns",
                style={'margin': '2rem', 'display': 'inline-block',
                       'boxShadow': '#e3e3e3 4px 4px 2px',
                       'border-radius': '10px',
                       'backgroundColor': 'white',
                       'height': 'auto'},
                children=[
                    html.Label('Fully Vaccinations vs. Un-vaccinations',
                               style={'marginTop': '3rem',
                                      'fontWeight': 'bold',
                                      'textAlign': 'center'}),
                    dcc.Graph(id='bottom_line_chart')
                ],
            ),

        ]),

    html.Label('Reference: Our data come from 1. https://ourworldindata.org/, ',
               style={'textAlign': 'center',
                      'padding': '1rem',
                      'font-size': '1rem'}),
])

# ******************************************************************************
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

# ******************************************************************************
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

# ******************************************************************************
# Zuodong added for dashtable
dict = {}
dict["United States"] = pd.read_csv("United States.csv")
dict["Austria"] = pd.read_csv("Austria.csv")
dict["Bulgaria"] = pd.read_csv("Bulgaria.csv")
dict["France"] = pd.read_csv("France.csv")
dict["Germany"] = pd.read_csv("Germany.csv")
dict["Italy"] = pd.read_csv("Italy.csv")
dict["Netherlands"] = pd.read_csv("Netherlands.csv")
dict["Portugal"] = pd.read_csv("Portugal.csv")
dict["Spain"] = pd.read_csv("Spain.csv")


# ******************************************************************************

@app.callback(
    [Output('num_t_vacc', 'children'),
     Output('num_new_case', 'children'),
     Output('num_hosp_p', 'children'),
     Output('num_icu_p', 'children'),
     Output('num_delta', 'children'),
     Output(component_id='top_fig_title', component_property='children'),
     Output('top_line_chart', 'figure'),
     Output(component_id='bottom_line_chart', component_property='figure'),
     Output(component_id='table_ctry', component_property='children'),
     Output('newstable', 'data'),
     Output('newstable', 'columns')
     ],
    [Input('input_ctry', 'value'),
     Input('input_month', 'value'),
     Input('input_line', 'value'),
     Input('input_outcome', 'value'),
     Input('input_vtype', 'value'),
     Input('input_age', 'value')
     ]
)
def updates(ctry, month, input_line, outcome, input_vtype, input_age):
    # update statistic box
    # resample into semi-month
    dfStatVariTemp = dfVariant[dfVariant['location'] == ctry].resample('sm').mean()
    dfStatTemp = df[df['location'] == ctry].resample('sm').mean()

    # merge df
    dfStatMerge = dfStatVariTemp.join(dfStatTemp).reset_index().fillna(0)
    dfStatMerge = dfStatMerge.reset_index()
    dfStatMerge = dfStatMerge.fillna(0)

    month_bott_limit = datetime.strptime(f'2021-{month[0]}-01', '%Y-%m-%d')
    month_top_limit = datetime.strptime(f'2021-{month[1] + 1}-01', '%Y-%m-%d')
    # print(month, month_bott_imit, month_top_limit)

    dfStatMerge = dfStatMerge[(dfStatMerge['date'] >= month_bott_limit) & (dfStatMerge['date'] <= month_top_limit)]

    # print(ctry, '\n',
    #       dfmerge[['total_vaccinations', 'new_cases', 'hosp_patients', 'icu_patients', 'num_sequences']])

    num_t_vacc = int(dfStatMerge['total_vaccinations'].mean()) if dfStatMerge[
                                                                      'total_vaccinations'].mean() != 0.0 else 'NaN'
    num_n_case = int(sum(dfStatMerge['new_cases'])) if sum(dfStatMerge['new_cases']) != 0.0 else 'NaN'
    num_hos_p = int(sum(dfStatMerge['hosp_patients'])) if sum(dfStatMerge['hosp_patients']) != 0.0 else 'NaN'
    num_icu_p = int(sum(dfStatMerge['icu_patients'])) if sum(dfStatMerge['icu_patients']) != 0.0 else 'NaN'
    num_delta_v = int(sum(dfStatMerge['num_sequences'])) if sum(dfStatMerge['num_sequences']) != 0.0 else 'NaN'

    # update top_line_chart
    top_fig_title = f'{ctry} Normalized Value Line Chart'
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

    dfnorm = dfnorm[(dfnorm['Date'] >= month_bott_limit) & (dfnorm['Date'] <= month_top_limit)]
    # print(dfnorm)

    top_fig = px.line(dfnorm,
                      x='Date',
                      y=input_line,
                      markers=True)

    # update bottom_line_chart
    dfvaccTemp = dfvaccine.copy(deep=True)
    dfOutput = dfvaccTemp[(dfvaccTemp['Outcome'] == outcome)
                          & (dfvaccTemp['Age'] == input_age)
                          & (dfvaccTemp['Brand'] == input_vtype)]
    # print(dfOutput)

    vacc_fig = px.line(dfOutput,
                       x='Date',
                       y=['Fully vaccinations', 'Un-vaccinations'],
                       markers=True)

    # update table
    df2 = dict[ctry]
    output_ctry = f'{ctry} Granger Causality in Time Series'
    columns = [{"name": str(i), "id": str(i)} for i in df2.columns]
    data = df2.to_dict(orient='records')

    return num_t_vacc, num_n_case, num_hos_p, num_icu_p, num_delta_v, \
           top_fig_title, top_fig, vacc_fig, output_ctry, data, columns


if __name__ == '__main__':
    app.run_server(debug=True)
