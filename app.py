# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.DataFrame({ # graph values for widget 1
    "Keywords": ["Artificial intelligence", "Computer vision", "Information retrieval", "Natural language processing", "Machine learning"],
    "Count": [300, 100, 900, 300, 100],
    "Keywords": ["Artificial intelligence", "Computer vision", "Information retrieval", "Natural language processing", "Machine learning"]
})

fig = px.bar(df, x="Keywords", y="Count", color="Keywords", barmode="group")

fig.update_layout(
    plot_bgcolor='#CCCCFF',
    paper_bgcolor='#CCE5FF',
    font_color='#000000'
)

dropdown_options = [ #dropdown menu values for widget 2
    {"label": "Artificial intelligence", "value": "ai"},
    {"label": "Computer vision", "value": "cv"},
    {"label": "Natural language processing", "value": "nlp"},
    {"label": "Machine learning", "value": "ml"},
    {"label": "Information retrieval", "value": "ir"},
]
  
professors = { ######### Needs to be modified #########
    'ai': ['Prof. A1', 'Prof. A2', 'Prof. A3', 'Prof. A4', 'Prof. A5'],
    'cv': ['Prof. B1', 'Prof. B2', 'Prof. B3', 'Prof. B4', 'Prof. B5'],
    'nlp': ['Prof. C1', 'Prof. C2', 'Prof. C3', 'Prof. C4', 'Prof. C5'],
    'ml': ['Prof. D1', 'Prof. D2', 'Prof. D3', 'Prof. D4', 'Prof. D5'],
    'ir': ['Prof. E1', 'Prof. E2', 'Prof. E3', 'Prof. E4', 'Prof. E5'],
}

app.layout = html.Div(children=[
    html.H1(children='Explore AI in Academic World', # Header
            style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }
    ),

    html.Div(children='''Publication that contains the keywords (e.g., computer vision) count''', # title for the widget 1
            style={
            'textAlign': 'center',
            'color': '#7FDBFF'
            }
    ),

    dcc.Graph(  # graph for the widget 1
        id='example-graph',
        figure=fig
    ),

    html.Div(style={'height': '50px'}), # blank space

    html.Div(children='''Top 5 professors that are relevant to the keyword “AI”''', # title for the widget 2
            style={
            'textAlign': 'center',
            'color': '#7FDBFF'
            }
    ),

     dcc.Dropdown( # dropdown menu for the widget 2
        id='professor-dropdown',
        options=dropdown_options,
        value='ai',  # Default value
        style={
            'width': '50%',
            'margin': '0 auto'
        }
    ),

    html.Div(id='professor-list', style={'textAlign': 'center', 'marginTop': '20px'})

])

@app.callback(
    Output('professor-list', 'children'),
    Input('professor-dropdown', 'value')
)
def update_professor_list(selected_keyword):
    if selected_keyword:
        return html.Ul([html.Li(prof) for prof in professors[selected_keyword]])
    return "No professors available for the selected keyword."

if __name__ == '__main__':
    app.run(debug=True)
