import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import pandas as pd
import dash_table_experiments as dt
import plotly.graph_objs as go

import twitter
import lstm


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#10E8EB',
    'text': '#7FDBFF'
}


sentiment_colors = {-1:"#EE6055",
                    -0.5:"#FDE74C",
                     0:"#FFE6AC",
                     0.5:"#D0F2DF",
                     1:"#9CEC5B",}


app_colors = {
    'background': '#0E94AB',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(style={'backgroundColor': colors['background']},
children=[
        html.Div([
            html.Div(dcc.Input(id='input-box', type='text', value='barackobama',style={'margin-left':'47.5%','margin-top':'10px'})),
            html.Button('Submit', id='button', style={'backgroundColor': '#FFFFFF','margin-left': '50%','margin-top':'10px','margin-bottom':'10px'}),
            html.Div(id='output-container-button',
             children='')
        ]),
        html.Div([
              dcc.Graph(id='sentiment-pie',animate=False),     
        ], className="four columns",
           style={'margin': 'auto%','backgroundColor' : '0A9395'},
        ),
])

count = 5

@app.callback(
    dash.dependencies.Output('sentiment-pie', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')]) 
def update_output(n_clicks, value):     
    tweets = []
    
    CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
    CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
    ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
    ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN,
                    access_token_secret=ACCESS_TOKEN_SECRET)

    statuses = api.GetUserTimeline(screen_name=value, count=count, exclude_replies=False)

    for s in statuses:
        tweets.append(s.text)
    
    clear_tweet = lstm.clean_tweets(tweets)
    token_tweet = lstm.token_tweets(clear_tweet)
    result = lstm.result(token_tweet)
    fear = 0
    fun = 0
    happiness = 0
    neutral = 0
    sadness = 0
    print(result)
    
    for i in range(0,count):
        if result[i] == 0:
            sentiment = "Fear"
        elif result[i] == 1:
            sentiment = "fun"
        elif result[i] == 2:
            sentiment = "happiness"
        elif result[i] == 3:
            sentiment = "neutral"
        elif result[i] == 4:
            sentiment = "sadness"

        print(str(i+1)+". tweet = " + tweets[i] + "\nClean Tweet : " + clear_tweet[i]  +"\nSentiment : " + sentiment )

    for i in result:
        if i == 0:
            fear += 1
        elif i == 1:
            fun += 1
        elif i == 2:
            happiness += 1
        elif i == 3:
            neutral += 1
        elif i == 4:
            sadness += 1
     
    labels = ["Fear","Fun","Happiness","Neutral","Sadness"]
    values = [fear,fun,happiness,neutral,sadness]
    colors = ['#F60E0E', '#DF1BF0','0DD738','717578','05406E']

    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+percent', textinfo='value', 
                   textfont=dict(size=20, color=app_colors['text']),
                   marker=dict(colors=colors, 
                               line=dict(color=app_colors['background'], width=2)))

    data = {'Tweet' : tweets, 'Sentiment' : 'Sentiment'}
    df = pd.DataFrame(data)
    return {"data":[trace],'layout' : go.Layout(
                                                  title='Sentiment Pie ',
                                                  font={'color':app_colors['text']},
                                                  plot_bgcolor = app_colors['background'],
                                                  paper_bgcolor = app_colors['background'],
                                                  showlegend=True)}

if __name__ == '__main__':
    app.run_server(debug=False,host="0.0.0.0")
