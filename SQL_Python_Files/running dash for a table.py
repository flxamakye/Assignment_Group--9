import dash
from dash import dcc, html, dash_table
import requests
import pandas as pd
from dash.dependencies import Input, Output

# Initialize the app
app = dash.Dash(__name__)

def fetch_api_data():
    url = "http://108.238.181.112:5001/data"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)

    # Parse 'salesdate' column specifically
    if 'salesdate' in df.columns:
        df['salesdate'] = pd.to_datetime(df['salesdate'], errors='coerce')

    return df

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("API Data Table"),
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in fetch_api_data().columns],
        data=fetch_api_data().to_dict('records')
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
