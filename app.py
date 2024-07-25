# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
from mysql_utils import MySQLClient

app = Dash(__name__)

db = MySQLClient(host="127.0.0.1", user="root", password="password", database="academicworld")
db.connect()
widget1_results = db.fetch_widget1_results()
db.disconnect()

# DataFrame for widget 1
widget1_df = pd.DataFrame(widget1_results, columns=["Keywords", "Count"])

widget1_fig = px.bar(widget1_df, x="Keywords", y="Count", color="Keywords", barmode="group")

widget1_fig.update_layout(
    autosize=True,
    plot_bgcolor='#CCCCFF',
    paper_bgcolor='#CCE5FF',
    font_color='#000000'
)

widget2_dropdown_options = [ #dropdown menu values for widget 2
    {"label": "Artificial intelligence", "value": "ai"},
    {"label": "Computer vision", "value": "cv"},
    {"label": "Natural language processing", "value": "nlp"},
    {"label": "Machine learning", "value": "ml"},
    {"label": "Information retrieval", "value": "ir"},
]
  
widget2_professors = { ######### Needs to be modified #########
    'ai': ['Prof. A1', 'Prof. A2', 'Prof. A3', 'Prof. A4', 'Prof. A5'],
    'cv': ['Prof. B1', 'Prof. B2', 'Prof. B3', 'Prof. B4', 'Prof. B5'],
    'nlp': ['Prof. C1', 'Prof. C2', 'Prof. C3', 'Prof. C4', 'Prof. C5'],
    'ml': ['Prof. D1', 'Prof. D2', 'Prof. D3', 'Prof. D4', 'Prof. D5'],
    'ir': ['Prof. E1', 'Prof. E2', 'Prof. E3', 'Prof. E4', 'Prof. E5'],
}


app.layout = html.Div(children=[
 #-------------------------------------------- Header --------------------------------------------
    html.H1(children='Explore AI in Academic World',
            style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }
    ),

 #-------------------------------------------- Container for widget 1 & widget 2 & widget 3 --------------------------------------------
    html.Div(children=[ 

        html.Div(children=[ # Widget 1
            html.Div(children=''' Top 5 keywords among publications that are related to "AI" ''', # title for the widget 1
            style={
                'textAlign': 'center',
                'color': '#7FDBFF'
            }
            ),
            
            dcc.Graph(  # graph for the widget 1
                id='example-graph',
                figure=widget1_fig,
                style={'width': '80%', 'margin': '0 auto'}
            )
        ], style={'flex': 1, 'padding': '10px'}),

        html.Div(children=[  # Widget 2
            html.Div(children='''Top 5 professors that are relevant to the keyword “AI”''',  # title for the widget 2
                    style={
                        'textAlign': 'center',
                        'color': '#7FDBFF'
                    }
            ),

            dcc.Dropdown(  # dropdown menu for the widget 2
                id='professor-dropdown',
                options=widget2_dropdown_options,
                value='ai',  # Default value
                style={
                    'width': '80%',
                    'margin': '0 auto'
                }
            ),

            html.Div(id='professor-list', style={'textAlign': 'center', 'marginTop': '20px'})
        ], style={'flex': 1, 'padding': '10px'}),

        html.Div(children=[ # Widget 3
            html.Div(children='''Show the trend of keywords related to AI over the years''', # title for the widget 3
            style={
            'textAlign': 'center',
            'color': '#7FDBFF'
            }
            ),
            
            dcc.Graph(  # graph for the widget 3
                id='example-graph',
                figure=widget1_fig,
                style={'width': '80%', 'margin': '0 auto'}
            )
        ], style={'flex': 1, 'padding': '10px'})


    ], style={'display': 'flex', 'flexDirection': 'row'}),

 #-------------------------------------------- Container for widget 4 & widget 5 & widget 6 --------------------------------------------
    html.Div(children=[ 

        html.Div(children=[ # Widget 4
            html.Div(children='''Show the trend of keywords related to AI over the years''', # title for the widget 4
            style={
            'textAlign': 'center',
            'color': '#7FDBFF'
            }
            ),
            
            dcc.Graph(  # graph for the widget 4
                id='example-graph',
                figure=widget1_fig,
                style={'width': '80%', 'margin': '0 auto'}
            )
        ], style={'flex': 1, 'padding': '10px'}),

        html.Div(children=[ # Widget 5
            html.Div(children='''Show the trend of keywords related to AI over the years''', # title for the widget 5
            style={
            'textAlign': 'center',
            'color': '#7FDBFF'
            }
            ),
            
            dcc.Graph(  # graph for the widget 5
                id='example-graph',
                figure=widget1_fig,
                style={'width': '80%', 'margin': '0 auto'}
            )
        ], style={'flex': 1, 'padding': '10px'}),

        html.Div(children=[ # Widget 6
            html.Div(children='''Show the trend of keywords related to AI over the years''', # title for the widget 6
            style={
            'textAlign': 'center',
            'color': '#7FDBFF'
            }
            ),
            
            dcc.Graph(  # graph for the widget 6
                id='example-graph',
                figure=widget1_fig,
                style={'width': '80%', 'margin': '0 auto'}
            )
        ], style={'flex': 1, 'padding': '10px'})
    ], style={'display': 'flex', 'flexDirection': 'row'})

])
 #-------------------------------------------- CallBacks --------------------------------------------
@app.callback(
    Output('professor-list', 'children'),
    Input('professor-dropdown', 'value')
)
def update_professor_list(selected_keyword):
    if selected_keyword:
        return html.Ul([html.Li(prof) for prof in widget2_professors[selected_keyword]])
    return "No professors available for the selected keyword."

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

# Ensure the database disconnects when the app stops running
import atexit
atexit.register(db.disconnect)
