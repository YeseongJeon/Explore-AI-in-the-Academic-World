import dash
from dash import html

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1('Hello, World!')
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
