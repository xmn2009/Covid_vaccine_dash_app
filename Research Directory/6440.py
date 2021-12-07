✕
ZJ
NewsAPI
app3.py
print("LOADING ALL PACKAGES")
import pandas as pd
import json
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import scispacy
import spacy
import en_core_sci_md
from tqdm import tqdm
import joblib
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import PCA, LatentDirichletAllocation
from scipy.spatial.distance import jensenshannon
import matplotlib.pyplot as plt
import numpy as np
import pprint
import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import numpy as np
import json
import os
import glob
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output
import dash_table
#import fr_core_news_sm
#import es_core_news_sm
#import it_core_news_sm
#import de_core_news_sm
import en_core_web_sm
import plotly.express as px
import plotly.graph_objs as go
from plotly.validators.scatter.marker import SymbolValidator
import burst_detection as bd
 
 
# start of Topic modeling
nlp = en_core_sci_md.load(disable=["tagger", "parser", "ner"])
nlp_en = en_core_web_sm.load()
spacy_stopwords_en = list(spacy.lang.en.stop_words.STOP_WORDS)
stop_words = [
    'doi', 'preprint', 'copyright', 'peer', 'reviewed', 'org', 'https', 'et', 'al', 'author', 'figure', 
    'rights', 'reserved', 'permission', 'used', 'using', 'biorxiv', 'fig', 'fig.', 'al.', 
    'di', 'la', 'il', 'del', 'le', 'della', 'dei', 'delle', 'una', 'da',  'dell',  'non', 'si','<td>','td','abstract','<td','td>','td><td','/td><td'
]
 
customize_stop_words = stop_words + spacy_stopwords_en #+ spacy_stopwords_fr + spacy_stopwords_es + spacy_stopwords_it + spacy_stopwords_de
for w in customize_stop_words:
    nlp.vocab[w].is_stop = True
 
def spacy_tokenizer(sentence):
    return [word.lemma_ for word in nlp(sentence) if not (word.like_num or word.is_stop or word.is_punct or word.is_space or len(word)==1)]
 
def process(df, country):
    df['text_processed'] = df['text'].map(lambda x: re.sub('[,\.!?]', '', x))
    df['text_processed'] = df['text'].map(lambda x: x.lower())
    df['text_processed'] = df['text'].map(lambda x: re.sub('<[^>]*>', '', x))
    vectorizer = joblib.load(model_dir+country+'_'+'bigram_vectorizer.csv')    # load count vector
    data_vectorized = joblib.load(model_dir+country+'_'+ 'bigram_data_vectorized.csv')  # load data vector
    return df, vectorizer, data_vectorized
    
def get_k_nearest_docs(doc_dist, doc_topic_dist, k=5, only_covid19=True):
    '''
    doc_dist: topic distribution (sums to 1) of one article
 
    Returns the index of the k nearest articles (as by Jensen–Shannon divergence in topic space).
    '''
 
    temp = doc_topic_dist
    distances = temp.apply(lambda x: jensenshannon(x, doc_dist), axis=1)
    k_nearest = distances[distances != 0].nsmallest(n=k).index
    k_distances = distances[distances != 0].nsmallest(n=k)
    return k_nearest, k_distances
# end of Topic modeling
 
 
## start of Dataset and model Loading
dict1 ={}
vector = {}
data_vector ={}
newslda={}
dist={}
countrylist=[]
data_dir = "Data/"
model_dir = "model/"
for filepath in glob.iglob(data_dir + '**/*.json', recursive=True): 
    country = filepath.split("/")[1].split(".")[0]
    print (country)
    df=pd.read_json(filepath, orient = 'records')
 
    df = df.drop_duplicates(subset=['title'])
    df = df.replace(np.nan, ' ', regex=True)
    df['text'] =  df['title']+", "+df['description']+", "+df['content']    
    
    print(df.shape)
    df = df.reset_index()
    dict1[country], vector[country], data_vector[country]  = process(df, country)  
    
    newslda[country] = joblib.load(model_dir+country+'_'+'lda.csv')  #load lda model 
    dist[country] =  pd.read_csv(model_dir+country+'_'+'dist.csv')      # load lda tranform lda
    countrylist.append(country)
    print(df.shape)
    
## end of Dataset and model Loading  
 
## start of scibite loading
import plotly
import plotly.offline as pof
from biosphere_common.schema import BSKG
from biosphere_common.services.core_api import BioSphereService
from biosphere_common.services.sagemaker import DeepLearningService
from biosphere_common.services.scibite import ScibiteService
from biosphere_common.viz.plots.plotly import PlotGen
 
plotly.offline.init_notebook_mode(connected=True)
bskg_api = BioSphereService()
bskg_deep = DeepLearningService(BSKG.DeepLinkVersion.v8)
s = ScibiteService()
 
def entity_extraction(text):
    annotation_mapping = s.make_request('', '', 'termite', text, 'json', True)
    entity=[]
    for key, value in annotation_mapping['RESP_PAYLOAD'].items():
        entity.append(key+"_"+value[0]['name']+", ")
    return entity
## end of scitbite loading
 
 
# loading date
df=pd.read_csv('Data/datefile.csv')
lastdate = df.Date.iloc[0]
message = "data last updated as of " + lastdate
###
#Create asterisk marks for burst signal
raw_symbols = SymbolValidator().values
asterisk = raw_symbols[242] 
###
 
 
#load and combine news data with google trends and case number
 
def state_positive_case(data, state):
    """
    extract daily positive COVID-19 case numbers of a specific state in US
    Args:
        data: daily updated COVID-19 case numbers of all states in US (https://covidtracking.com/data/download)
        state: two letter state name -> for ex: TX(Texas), CA(California)
    """
    import datetime
    daily_case = pd.read_csv(data)
    daily_state = daily_case[daily_case['state'] == state].reset_index(drop = True)
    daily_state['date'] = [datetime.datetime.strptime(str(r), '%Y%m%d').strftime('%Y-%m-%d') for r in daily_state['date']]
    daily_state = change_datetime(daily_state, 'date')
    daily_state = daily_state[['date','state','positive']]
    daily_state.columns = ['date', 'state','cumulative_cases']
    return(daily_state)
def aggregate_datetime(df, date_column, target_column, window, metric):
    """
    Calculate a summary metric for given date window on a grouped column
    Args:
        df: pandas dataframe
        date_column: date column name 
        target_column: aggregated column name 
        window: window to calculate sum -> for ex: 'W'(week), 'M' (month) or 'D'(day)
        metric: descriptive metric(s) for a column -> for ex: ['count'], ['sum'], ['count', 'sum','mean', 'median']
 
    Returns: A aggregated pandas dataframe with specific metrics
 
    """
    df_agg = df.groupby(pd.Grouper(key=date_column, freq=window))[target_column].agg(metric)
    df_agg = df_agg.reset_index() # keep datetime as a column
    return(df_agg)
def change_datetime(df, date_column):
    """
    Change a specific column into the format of datetime
    Args:
        df: pandas dataframe
        date_column: the column containing date information   
    Returns: pandas dataframe with a date time column
 
    """
    df.loc[:, date_column] = pd.to_datetime(df[date_column], infer_datetime_format=True)
    return(df)
 
def combine_data(case_data, state_name, news_data, Gtrends_data):
    
    #(1) extract state covid-19 case number
    df_case = state_positive_case(case_data, state_name)
 
    #(2) extract news sentiment score data and aggregate by week
    df = pd.read_json(news_data, orient = 'records')
    df.columns = ['source', 'author', 'title', 'description', 'url', 'urlToImage','publishedAt', 'content', 
                  'sent_score', 'datetime', 'date']
    df_burst = df[['datetime', 'sent_score']].copy()
    df_burst.loc[df_burst['sent_score'] > -0.05, 'sent_score'] = 0 # Consider news with sentiment score > -0.05 as non target news
    df_burst_agg = aggregate_datetime(df_burst, 'datetime', 'sent_score', 'W', ['count', 'sum'])
    df_burst_agg['sum'] = abs(df_burst_agg['sum']) # All news scores are negative values
    df_burst_agg.columns = ['date', 'count', 'sum']
    
    #(3) Merge case number and news sentiment data
    df_burst_agg = pd.merge(df_burst_agg, df_case,  how='left', left_on='date', right_on = 'date')
    
    #(4) extract Google trends score data and aggregate
    Gtrends = pd.read_csv(Gtrends_data)
    Gtrends = change_datetime(Gtrends, 'date')
    time_range =pd.Series([pd.Timestamp('2020-01-19T00')]).append(df_burst_agg['date']) # Make the initial date same with the news
    Gtrends_agg = Gtrends.groupby(pd.cut(Gtrends['date'], time_range, right = True)).agg(['mean'])
    
    #(5) Merge Google trends data
    df_burst_agg['COVID-19 Symptoms'] = Gtrends_agg['COVID-19 Symptoms']['mean'].values
    df_burst_agg['COVID-19 Testing'] = Gtrends_agg['COVID-19 Testing']['mean'].values
    #df_burst_agg['Urgent Care Near Me'] = Gtrends_agg['Urgent Care Near Me']['mean'].values
    df_burst_agg['COVID Guidelines'] = Gtrends_agg['COVID Guidelines']['mean'].values
    
    
    df_burst_agg['state'] = state_name
    #df_burst_agg = df_burst_agg.loc[index_initial_week:index_latest_week,].reset_index(drop = True)
   
    df_burst_agg['weekly_cases'] = df_burst_agg['cumulative_cases'].diff().fillna(0)
    if max(df_burst['datetime']).date() < max(df_burst_agg['date']).date():
        df_burst_agg = df_burst_agg.iloc[:-1] # Remove the latest week if it does not have complete data of news
    return(df_burst_agg)
 
#### detecting burst model
 
def fit(d_,r_,p_):
    from mpmath import log, binomial
    return(-np.float((log(binomial(int(d_),r_)) + r_*np.log(p_) + (d_-r_)*np.log(1-p_))))
def find_gamma(special_events_queque, total_events_queque, s_burst, time_num):
    news_num_threshold = np.median(total_events_queque)
    p_baseline = np.nansum(special_events_queque) / float(np.nansum(total_events_queque)) 
    p_burst = p_baseline * s_burst                         
    if p_burst > 1:                               
        p_burst = 0.99999
    target_news_num = news_num_threshold * p_burst
    fit_cost = fit(news_num_threshold, target_news_num, p_baseline) - fit(news_num_threshold,target_news_num, p_burst)
    gamma = fit_cost/(np.log(time_num))
    return(gamma)
 
def detect_burst(df, s = 1.2, gamma = None):
    special_events_queque = df['sum']
    total_events_queque = df['count']
    time_num = len(df)
    if gamma is None:
        gamma = find_gamma(special_events_queque, total_events_queque, s, time_num)
    else:
        gamma = gamma
    gamma= round(gamma, 2)
    q, d, r, p = bd.burst_detection(special_events_queque, total_events_queque,time_num,s,gamma,smooth_win=1)
    bursts = bd.enumerate_bursts(q, 'burstLabel')
    #find weight of bursts
    weighted_bursts = bd.burst_weights(bursts,r,d,p)
 
    df['special_ratio'] = df['sum']/df['count']
    df['burst_ratio'] = p[1]
    df['baseline_ratio'] = p[0]
    df['burst'] = q
    return(gamma, df)
 
### End of burst model
def display_links(dff):
    #links = dff['Study Link'].to_list()
    links = list(dff['url'])
    rows = []
    for x in links:
        link = '[news_link](' +str(x) + ')'
        rows.append(link)
    return rows
 
 
###
AZ_Gtrends = '/mnt/burst_data/google_trends_data/google_trends_US-AZ_US-AZ_2020.csv'
FL_Gtrends = '/mnt/burst_data/google_trends_data/google_trends_US-FL_US-FL_2020.csv'
TX_Gtrends = '/mnt/burst_data/google_trends_data/google_trends_US-TX_US-TX_2020.csv'
 
AZ_news = '/mnt/burst_data/news_data/Arizona.json'
FL_news = '/mnt/burst_data/news_data/Florida.json'
TX_news = '/mnt/burst_data/news_data/Texas.json'
 
case_data = '/mnt/burst_data/case_data/daily_0707.csv'
#countrylist=['Arizona', 'Florida', 'Texas']
dict2 ={}
d_gamma={}
 
d_gamma['Arizona'], dict2['Arizona'] = detect_burst(combine_data(case_data, 'AZ', AZ_news, AZ_Gtrends), s=1.2)
d_gamma['Florida'], dict2['Florida'] = detect_burst(combine_data(case_data, 'FL', FL_news, FL_Gtrends), s=1.2)
d_gamma['Texas'], dict2['Texas']= detect_burst(combine_data(case_data, 'TX', TX_news, TX_Gtrends), s=1.2)
 
 
 
 
print("APP STARTING")
 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
 
runID = os.environ['DOMINO_RUN_ID']
user = os.environ['DOMINO_PROJECT_OWNER']
project = os.environ['DOMINO_PROJECT_NAME']
 
assets_path = 'https://opendatasciencelab.jnj.com/'+ user + '/' + project +'/r/notebookSession/' + runID + 'assets/'
 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,assets_external_path = assets_path)
 
app.config.update({
 'routes_pathname_prefix': '',
 'requests_pathname_prefix': '/{}/{}/r/notebookSession/{}/'.format(
        os.environ.get("DOMINO_PROJECT_OWNER"),
        os.environ.get("DOMINO_PROJECT_NAME"),
        os.environ.get("DOMINO_RUN_ID"))
})
 
# Input
 
#marks={round(i/100.0,2): str(round(i/100.0,2)) for i in range(0,101,1)}
 
 
 
app.layout = html.Div([
 
    html.Div(
        html.H1('COVID-19 News Monitoring'),
    ),
       html.Div(
        html.H6(message)
    ),
    
 
    dcc.Tabs(id="tabs", value='Tab1', children=[
        # Tab 1 Biological Risk Factors
        
        
        
dcc.Tab(label='COVID-19 Surveillance', id='tab1', value='tab1', children =[
 
       html.Div(
        html.H4('News Trend Modeling')
    ),
      
        html.Div([
            dcc.Dropdown(
                id='countryname',
                options=[{'label': i, 'value': i} for i in countrylist],
                value='Texas'
            ),
        ],
        style={'marginBottom': '1em'}),
        
        dcc.Checklist(
                id='checklist',
                options=[{'label': i, 'value': i} for i in ['News_count', 'Weekly_cases', 'Google_trends', 'Negative_news','Burst_alert']],
                value=['News_count', 'Weekly_cases', 'News_sentiment_trends', 'Google_trends', 'Negative_news','Burst_alert'],
                labelStyle={'display': 'inline-block'}
            ),
 
 
 
      
       html.Div([
               dcc.Graph(
                         id= 'graphplot',
                         figure={}
                         )
              ]),
 
 
 
 
    html.H6(children='gamma: '),
    html.Div( 
 
        dcc.Slider(
        id='burstv',
        min=0.0,
        max=1.0,
        value=d_gamma['Texas'],
        step=0.01,
 
      
       ), 
    style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
]),
 
 
 
        # Tab 2 Environmental Risk Factors
    dcc.Tab(label='News Search', id='tab2', value= 'tab2', children=[
 
        html.Div([
        html.Div([
        dcc.Input(id='my-id', type='text', placeholder='Enter query word', value=''),    
         html.H4(children='Recommended Relevant news'),
        ],
        style={'width': '48%', 'display': 'inline-block'}),
 
        html.Div([
 
            dcc.Dropdown(
                id='country_name',
                options=[{'label': i, 'value': i} for i in countrylist],
                value='Texas'
            ),
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
       
        html.H5(children='News Search'),
        dash_table.DataTable(id='newstable', style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
    })
        ])
    ])
 
])
 
 
@app.callback(
    Output(component_id='graphplot', component_property='figure'),
    [Input('checklist', 'value'),
     Input('countryname','value'),
     Input('burstv','value')]
)
 
def update_graph(checklists, country, gamma_value):
 
    g, dx= detect_burst(dict2[country], s=1.2, gamma = gamma_value)
    
    dx1 =dx.loc[dx['burst']==1]    
    data=[]
    layout={}
    layout['xaxis']=dict(domain=[0.2, 0.8])
    
    if 'News_count' in checklists:
        a= go.Bar(x=dx['date'],y=dx['count'],name="Number of news per week") 
        data.append(a)
        layout['yaxis'] =dict(title="Number of news per week",titlefont=dict(color="#1f77b4"),tickfont=dict(color="#1f77b4"))
 
    if 'Weekly_cases' in checklists:
        b=go.Scatter(x=dx['date'],  y=dx['weekly_cases'], name="Number of cases per week",yaxis= "y2")
        data.append(b)
        layout['yaxis2'] =dict(title="Number of cases per week",titlefont=dict(color="#ff7f0e"),tickfont=dict(color="#ff7f0e"),anchor="free",overlaying="y",side="left",position=0.15)     
        
        
    if 'Google_trends' in checklists:
        c= go.Scatter(x=dx['date'], y=dx['COVID-19 Testing'], name="COVID-19 Testing",yaxis= "y3")
        data.append(c)
        layout['yaxis3'] =dict(title="COVID-19 Testing",titlefont=dict(color="#d62728"),tickfont=dict(color="#d62728"),anchor="x",overlaying="y",side="right")          
        
    if 'Negative_news' in checklists:
        d = go.Scatter(x=dx['date'], y=dx['special_ratio'], name="Fraction of negative news",yaxis= "y4")
        data.append(d)
        layout['yaxis4'] =dict(title="Fraction of negative news",titlefont=dict(color="#9467bd"),tickfont=dict(color="#9467bd"),anchor="free",overlaying="y",side="right",position=0.85)
    
    if 'Burst_alert' in checklists:
        e = go.Scatter(x=dx1['date'], y=dx1['special_ratio'], mode = 'markers',marker_symbol = asterisk, marker=dict(size=20),name="Burst signal",yaxis= "y4")
        data.append(e)
       # layout['yaxis5'] =dict(title="Burst Signal",titlefont=dict(color="#9467bd"),tickfont=dict(color="#9467bd"),anchor="free",overlaying="y",side="right",position=0.85) 
        
    layout['height']= 800   
    layout['plot_bgcolor']='rgb(204,229,255)'
    return go.Figure(data=data, layout=layout)
 
 
 
 
 
 
    
@app.callback(
    [Output(component_id='newstable', component_property='data'),
     Output(component_id='newstable', component_property='columns')],
    [Input('my-id', 'value'),  
    Input('country_name', 'value')]
)
 
 
 
def update_table(input_value, country_name):
    df = dict1[country_name]
    tasks = [input_value] if type(input_value) is str else ['environmental risk']
    tasks_vectorized = vector[country_name].transform(tasks)
    tasks_topic_dist = pd.DataFrame(newslda[country_name].transform(tasks_vectorized))
    doc_topic_dist = dist[country_name]
    for index, bullet in enumerate(tasks):
        print(bullet)
        recommended, distances = get_k_nearest_docs(tasks_topic_dist.iloc[index], doc_topic_dist, 30, True)
        recommended = df.iloc[recommended].copy()
        recommended = recommended[['title', 'url', 'date', 'content']]
        recommended.columns = ['title', 'url', 'date', 'content']
        
        recommended['jenssenshannon_distance'] = distances
 
        recommended['scibite'] = recommended['content'].apply(entity_extraction)# add scibite extraction
        recommended = recommended[['title', 'url', 'date', 'scibite']]
        print(recommended.shape)
        df1 =recommended
        df1['url'] = display_links(df1)
        df1['date'] = df1['date'].dt.date
       # columns = [{'name': col, 'id': col} for col in df1.columns]
        columns=[{'name': 'title', 'id':'title'}, 
                 {'name': 'url', 'id':'url','type':'text','presentation':'markdown'},
                 {'name': 'date', 'id':'date'},
                 {'name': 'scibite', 'id':'scibite'}]    
        
        data = df1.to_dict(orient='records')
        return data, columns
 
 
if __name__ == '__main__':
    app.run_server(port=8888, host='0.0.0.0', debug=True)
Discussion
 
Add a new comment
Markdown
 and 
Mathjax
 are supported. You can also @mention people.