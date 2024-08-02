import atexit
import dash
from dash import Dash, html, dcc, Output, Input, State, dash_table
import plotly.express as px
import pandas as pd
from mysql_utils import MySQLClient
from mysql.connector import Error
from mongodb_utils import MongoDBClient
from neo4j_utils import Neo4jClient
import socket

app = Dash(__name__)

# Connect to the Neo4j database
neo4jdb = Neo4jClient(uri="bolt://localhost:7687",
                      user="neo4j", 
                      password="ilovecs411")
neo4jdb.connect()
# Connect to the MongoDB database
mongodb = MongoDBClient(host="127.0.0.1", 
                        port=27017,
                        database_name="academicworld")
mongodb.connect()
# Connect to the MySQL database
db = MySQLClient(host="127.0.0.1", 
                 user="root",
                 password="test_root", 
                 database="academicworld")
db.connect()


# Create stored procedures and views
db.create_procedure_favorite_university()
db.create_procedure_favorite_paper()
db.recreate_favorite_university_table()
db.recreate_favorite_paper_table()
db.create_view_faulty_details()


# Fetch data from the database for widget 1
widget1_results = db.fetch_widget1_results()
widget2_university_results = db.fetch_widget2_universities()
db.disconnect()

# DataFrame for widget 1 graph
widget1_df = pd.DataFrame(widget1_results, columns=["Keywords", "Count"])

widget1_fig = px.pie(widget1_df, values='Count', names='Keywords')

widget1_fig.update_layout(
    autosize=True,
    plot_bgcolor='#CCCCFF',
    paper_bgcolor='#CCE5FF',
    font_color='#000000'
)

widget2_dropdown_options = [  # dropdown menu values for widget 2
    {"label": "Artificial intelligence", "value": "Artificial intelligence"},
    {"label": "Computer vision", "value": "Computer vision"},
    {"label": "Natural language processing", "value": "Natural language processing"},
    {"label": "Machine learning", "value": "Machine learning"},
    {"label": "Information retrieval", "value": "Information retrieval"},
]

widget2_university_dropdown_options = [  # dropdown menu values for universities
    {"label": university[0], "value": university[0]} for university in widget2_university_results
]

widget5_dropdown_options = [  # dropdown menu values for widget 5
    {"label": "Artificial intelligence", "value": "artificial intelligence"},
    {"label": "Computer vision", "value": "computer vision"},
    {"label": "Natural language processing", "value": "natural language processing"},
    {"label": "Machine learning", "value": "machine learning"},
    {"label": "Information retrieval", "value": "information retrieval"},
]


#
app.layout = html.Div(children=[
    # -------------------------------------------------------------- Header ----------------------------------------------------------------
    html.H1(children='Explore AI in the Academic World - A Dashboard for Grad School Applicants',  # title for the dashboard
            style={
                'textAlign': 'center',
                'color': '#7FDBFF'
            }
            ),

    # -------------------------------------------- Container for widget 1 & widget 2 & widget 3 --------------------------------------------
    html.Div(children=[

        html.Div(children=[  # Widget 1
            html.Div(children=''' Top 5 keywords among publications that are related to "AI" ''',  # title for the widget 1
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
            html.Div(children='''Top 5 professors that are relevant to the keyword related to “AI”''',  # title for the widget 2
                     style={
                         'textAlign': 'center',
                         'color': '#7FDBFF'
                     }
                     ),

            # display professor-list
            html.Div(id='professor-list',
                     style={'textAlign': 'center', 'marginTop': '20px'}),

            dcc.Dropdown(
                id='university-dropdown',  # dropdown university menu for the widget 2
                options=widget2_university_dropdown_options,  # Default value
                value=widget2_university_dropdown_options[0]['value'],
                style={
                    'width': '80%',
                    'margin': '0 auto',
                    'marginBottom': '20px'
                }
            ),
            dcc.Dropdown(  # dropdown subject menu for the widget 2
                id='subject-dropdown',
                options=widget2_dropdown_options,
                value='Artificial intelligence',  # Default value
                style={
                    'width': '80%',
                    'margin': '0 auto'
                }
            )
        ], style={'flex': 1, 'padding': '10px'}),

        html.Div(children=[  # Widget 3
            html.Div(children='''Spotlight on Professor with Contact Details''',  # title for the widget 3
                     style={
                         'textAlign': 'center',
                         'color': '#7FDBFF'
                     }
                     ),
            dcc.Input(id='prof-name', type='text', placeholder='Enter Professor Name'),
            html.Button('Submit', id='submit-button', n_clicks=0),
            html.Div(id='output-container')
        ], style={'flex': 1, 'padding': '10px'})

    ], style={'display': 'flex', 'flexDirection': 'row'}),

    # --------------------------------- Container for widget 4 & widget 5 ---------------------------------
    html.Div(children=[
        # Widget 4: University Ranking by Key Publications
        html.Div(children=[
            html.Div(children='''University Ranking by Key Publications''',  # title for the widget 4
                     style={
                         'textAlign': 'center',
                         'color': '#7FDBFF'
                     }
                     ),
            dcc.Dropdown(
                id='ranking-dropdown',
                options=widget2_dropdown_options,
                value='Artificial intelligence',
                style={
                    'width': '80%',
                    'margin': '0 auto'
                }
            ),
            dcc.Graph(
                id='university-ranking-chart',
                style={'width': '80%', 'margin': '0 auto'}
            )
        ], style={'flex': 1, 'padding': '10px'}),

        # Widget 5: Most Cited Publications in AI Subjects
        html.Div(children=[
            html.Div(children='''Most Cited Publications in AI Subjects''',  # title for the widget 5
                     style={
                         'textAlign': 'center',
                         'color': '#7FDBFF'
                     }
                     ),

            dcc.Dropdown(
                id='widget5-subject-dropdown',
                options=widget5_dropdown_options,
                value='artificial intelligence',
                style={'width': '80%', 'margin': '0 auto'}
            ),
            dcc.Graph(id='most-cited-publications-chart',
                      style={'width': '80%', 'margin': '0 auto'}),

            dash_table.DataTable(
                id='publications-table',
                columns=[
                    {"name": "Publication ID", "id": "id"},
                    {"name": "Title", "id": "title"}
                ],
                style_table={'width': '80%', 'margin': '0 auto',
                             'marginTop': '20px'},
                style_cell={
                    'textAlign': 'left',
                    'whiteSpace': 'normal'
                }
            )
        ], style={'flex': 1, 'padding': '10px'})
    ], style={'display': 'flex', 'flexDirection': 'row'}),


#--------------------------------- Container for widget 6 & widget 7 ---------------------------------
    html.Div(children=[ 
        # Widget 6
        html.Div(children=[
            html.Div(children='''Notepad for My Favorite Universities''',
                     style={
                         'textAlign': 'center',
                         'color': '#7FDBFF'
                     }
                     ),
            dcc.Input(id='university-id-input', type='text',
                      placeholder='Enter University ID'),
            html.Button('Add University', id='add-button', n_clicks=0),
            html.Button('Delete University', id='delete-button', n_clicks=0),
            html.Div(id='output-message'),
            html.H2("Favorite Universities List"),
            html.Table(id='favorite-universities-table')
        ], style={'flex': 1, 'padding': '10px'}),

        # Widget 7
        html.Div(children=[
            html.Div(children='''Notepad for My Favorite Papers''',
                     style={
                         'textAlign': 'center',
                         'color': '#7FDBFF'
                     }
                     ),
            dcc.Input(id='publication-id-input', type='text',
                      placeholder='Enter Publication ID'),
            html.Button('Add Publication', id='add-button-2', n_clicks=0),
            html.Button('Delete Publication',
                        id='delete-button-2', n_clicks=0),
            html.Div(id='output-message-2'),
            html.H2("Favorite Papers List"),
            html.Table(id='favorite-papers-table')
        ], style={'flex': 1, 'padding': '10px'})

    ], style={'display': 'flex', 'flexDirection': 'row'})

])
# ---------------------------------------------------------- CallBacks -----------------------------------------------------------------

# Callback for updating the professor list based on the selected keyword and university
@app.callback(
    Output('professor-list', 'children'),
    [Input('subject-dropdown', 'value'),
     Input('university-dropdown', 'value')]
)
def update_professor_list(selected_keyword, selected_university):
    db.connect()
    professor_results = db.fetch_widget2_results(
        selected_keyword, selected_university)
    if professor_results:
        return html.Ul([html.Li(prof[0]) for prof in professor_results])
    return "No professors available for the selected keyword."

# Callback for updating the university ranking chart based on the selected keyword
@app.callback(
    Output('university-ranking-chart', 'figure'),
    Input('ranking-dropdown', 'value')
)
def update_unversity_ranking(keyword):
    df = mongodb.fetch_top_unversity_by_keyword(keyword, 10)

    if df.empty:
        fig = px.bar(
            title=f'No relevant publications found for keyword: {keyword}'
        )
    else:
        fig = px.bar(
            df,
            x='UniversityName(UniversityId)',
            y='KeyPublicationCount',
            title=f'Key Publication Count for "{keyword.upper()}" by University',
            labels={'UniversityName(UniversityId)': 'UniversityName(UniversityId)',
                    'KeyPublicationCount': 'KeyPublicationCount'},
            text='KeyPublicationCount'
        )
        fig.update_layout(
            xaxis_tickangle=-65,
            xaxis={'categoryorder': 'total descending'},
            margin={'l': 40, 'b': 150, 't': 40, 'r': 0},
            height=600
        )
    return fig

# Callback for updating the most cited publications chart based on the selected keyword
@app.callback(
    [Output('most-cited-publications-chart', 'figure'),
        Output('publications-table', 'data')],
    Input('widget5-subject-dropdown', 'value')
)
def update_most_cited_publications(keyword):
    df = neo4jdb.fetch_most_cited_publications(keyword, 10)

    if df.empty:
        fig = px.bar(
            title=f'No relevant publications found for keyword: {keyword}'
        )
        table_data = []
    else:
        df['id'] = df['id'].str.replace('p', '')

        fig = px.bar(
            df,
            x='citations',
            y='id',
            title=f'Most Cited Publications for "{keyword.title()}"',
            labels={'id': 'Publication ID',
                    'citations': 'Number of Citations'},
            text='citations'
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            margin={'l': 40, 'b': 50, 't': 40, 'r': 0},
            height=600
        )
        table_data = df[['id', 'title']].to_dict('records')
    return fig, table_data

# Callback for adding and deleting favorite universities
def get_favorite_universities():
    query = "SELECT * FROM favorite_university"
    results = db.fetch_results(query)
    return results

@app.callback(
    Output('output-message', 'children'),
    Output('favorite-universities-table', 'children'),
    Input('add-button', 'n_clicks'),
    Input('delete-button', 'n_clicks'),
    State('university-id-input', 'value')
)
def update_favorite_universities(add_clicks, delete_clicks, university_id):

    if not dash.callback_context.triggered:
        return '', generate_table(get_favorite_universities(), flag="University")

    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if university_id:
        if button_id == 'add-button':
            query = f"""
                INSERT INTO favorite_university (id, name)
                SELECT id, name
                FROM university
                WHERE id = {university_id};
            """
            db.connect()
            db.connection.start_transaction()
            try:
                db.execute_query(query)
                db.connection.commit()
                message = "University added successfully."
            except Error as e:
                message = f"Transaction rolled back due to Error: {e}."
                db.connection.rollback()
        elif button_id == 'delete-button':
            query = f"""
                DELETE FROM favorite_university
                WHERE id = '{university_id}';
            """
            db.connect()
            db.connection.start_transaction()
            try:
                db.execute_query(query)
                db.connection.commit()
                message = "University deleted successfully."
            except Error as e:
                message = f"Transaction rolled back due to Error: {e}."
                db.connection.rollback()
    else:
        message = "Please enter a University ID."

    return message, generate_table(get_favorite_universities(), flag="University")

# Callback for adding and deleting favorite papers
def get_favorite_papers():
    query = "SELECT * FROM favorite_paper"
    results = db.fetch_results(query)
    return results

@app.callback(
    Output('output-message-2', 'children'),
    Output('favorite-papers-table', 'children'),
    Input('add-button-2', 'n_clicks'),
    Input('delete-button-2', 'n_clicks'),
    State('publication-id-input', 'value')
)
def update_favorite_papers(add_clicks, delete_clicks, publication_id):

    if not dash.callback_context.triggered:
        return '', generate_table(get_favorite_papers(), flag="Paper")

    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if publication_id:
        if button_id == 'add-button-2':
            query = f"""
                INSERT INTO favorite_paper (id, title, year, num_citations)
                SELECT id, title, year, num_citations
                FROM publication
                WHERE id = {publication_id};
            """
            db.connect()
            db.connection.start_transaction()
            try:
                db.execute_query(query)
                db.connection.commit()
                message = "Publication added successfully."
            except Error as e:
                message = f"Transaction rolled back due to Error: {e}."
                db.connection.rollback()
        elif button_id == 'delete-button-2':
            query = f"""
                DELETE FROM favorite_paper
                WHERE id = '{publication_id}'
            """
            db.connect()
            db.connection.start_transaction()
            try:
                db.execute_query(query)
                db.connection.commit()
                message = "Publication deleted successfully."
            except Error as e:
                message = f"Transaction rolled back due to Error: {e}."
                db.connection.rollback()
    else:
        message = "Please enter a Publication ID."

    return message, generate_table(get_favorite_papers(), flag="Paper")

def generate_table(data, flag="University"):
    if flag == "University":
        header = html.Tr(
            [html.Th("University ID"), html.Th("University Name")])
        if not data:
            return header
        rows = [html.Tr([html.Td(record[0]), html.Td(record[1])]) for record in data]
        table = html.Table([header] + rows, id='favorite-universities-table', style={'width': '100%'})
    elif flag == "Paper":
        header = html.Tr([html.Th("Publication ID"), html.Th("Title"), html.Th("Year"), html.Th("Citations")])
        if not data:
            return header
        rows = [html.Tr([html.Td(record[0]), html.Td(record[1]), html.Td(record[2]), html.Td(record[3])]) for record in data]
        table = html.Table([header] + rows, id='favorite-papers-table', style={'width': '100%'})
    return table

# Callback for updating the professor details based on the selected professor
@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks'),
    State('prof-name', 'value')]
)
def update_professor_highlight(n_clicks, value):
    if n_clicks > 0:
        query = f'''
            SELECT *
            FROM faculty_details
            WHERE Name = '{value}' AND PublicationYear > 2010
            ORDER BY Citations DESC
            LIMIT 1;;
        '''
        db.connect()
        results = pd.DataFrame(db.fetch_results(query), columns=["Name", 
                                                                 "Position", 
                                                                 "ResearchInterests", 
                                                                 "Email", 
                                                                 "Phone", 
                                                                 "University",
                                                                 "PublicationId",
                                                                 "PublicationTitle",
                                                                 "PublicationYear",
                                                                 "Citations"])
        if not results.empty:
            details = results.iloc[0]
            return html.Div([
                html.H5('You can contact the professor using the following information.'),
                html.Table([
                    html.Tr([html.Td("Name:"), html.Td(details["Name"])]),
                    html.Tr([html.Td("Position:"), html.Td(details["Position"])]),
                    html.Tr([html.Td("Research Interests:"), html.Td(details["ResearchInterests"])]),
                    html.Tr([html.Td("Email:"), html.Td(details["Email"])]),
                    html.Tr([html.Td("Phone:"), html.Td(details["Phone"])]),
                    html.Tr([html.Td("University:"), html.Td(details["University"])]),
                    html.Tr([html.Td("PublicationId:"), html.Td(details["PublicationId"])]),
                    html.Tr([html.Td("Title:"), html.Td(details["PublicationTitle"])]),
                    html.Tr([html.Td("PublicationYear:"), html.Td(details["PublicationYear"])]),
                    html.Tr([html.Td("Citations:"), html.Td(details["Citations"])])
                ])
            ])
        else:
            return 'No results found.'
    return ''


# Function to find a free port
def find_free_port(start_port=8050):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1

# Ensure the database disconnects when the app stops running
atexit.register(db.disconnect)
atexit.register(mongodb.disconnect)
atexit.register(neo4jdb.disconnect)

if __name__ == '__main__':
    app.run_server(debug=True, port=find_free_port())


