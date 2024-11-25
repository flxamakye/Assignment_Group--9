import dash
from dash import dcc, html, dash_table
import requests
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

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

# Fetch the data once
data = fetch_api_data()

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'), 
        page_size=10,
        style_table={'overflowX': 'auto'}
    ),
    # Date Range Filter
    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id='date-range',
        min_date_allowed=data['salesdate'].min(),
        max_date_allowed=data['salesdate'].max(),
        start_date=data['salesdate'].min(),
        end_date=data['salesdate'].max()
    ),

    # Product Filter
    html.Label("Select Product ID:"),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': pid, 'value': pid} for pid in data['productid'].unique()],
        value=data['productid'].unique(),
        multi=True
    ),

    # Region Filter
    html.Label("Select Region:"),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in data['region'].unique()],
        value=data['region'].unique(),  # Select all regions by default
        multi=True
    ),

    # Shipping Status Filter
    html.Label("Select Shipping Status:"),
    dcc.Dropdown(
        id='shipping-dropdown',
        options=[
            {'label': 'Free Shipping', 'value': 1},
            {'label': 'No Free Shipping', 'value': 0}
        ],
        value=[0, 1],  # Select both shipping statuses by default
        multi=True
    ),

    # Graphs
    html.Div([
        dcc.Graph(id='sales-over-time'),
        dcc.Graph(id='total-sold-bar-graph'),
    ])
])

# Callback to update the "sales-over-time" graph
@app.callback(
    Output('sales-over-time', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('product-dropdown', 'value'),
     Input('region-dropdown', 'value'),
     Input('shipping-dropdown', 'value')]
)
def update_sales_over_time(start_date, end_date, selected_products, selected_regions, selected_shipping):
    # Filter data based on the selected date range, product IDs, regions, and shipping status
    filtered_data = data[
        (data['salesdate'] >= pd.to_datetime(start_date)) &
        (data['salesdate'] <= pd.to_datetime(end_date)) &
        (data['productid'].isin(selected_products)) &
        (data['region'].isin(selected_regions)) &
        (data['freeship'].isin(selected_shipping))
    ]

    # Handle empty filtered data
    if filtered_data.empty:
        return {
            "data": [],
            "layout": {
                "title": "No data available for the selected filters",
                "xaxis": {"title": "Sales Date"},
                "yaxis": {"title": "Items Sold"}
            }
        }

    # Create a scatter plot without a trend line
    fig = px.scatter(
        filtered_data,
        x='salesdate',
        y='itemssold',
        title='Items Sold Over Time',
        labels={'salesdate': 'Sales Date', 'itemssold': 'Items Sold'}
    )

    return fig

# Callback to update the "total-sold-bar-graph"
@app.callback(
    Output('total-sold-bar-graph', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('product-dropdown', 'value'),
     Input('region-dropdown', 'value'),
     Input('shipping-dropdown', 'value')]
)
def update_total_sold_bar_graph(start_date, end_date, selected_products, selected_regions, selected_shipping):
    # Filter data based on the selected date range, product IDs, regions, and shipping status
    filtered_data = data[
        (data['salesdate'] >= pd.to_datetime(start_date)) &
        (data['salesdate'] <= pd.to_datetime(end_date)) &
        (data['productid'].isin(selected_products)) &
        (data['region'].isin(selected_regions)) &
        (data['freeship'].isin(selected_shipping))
    ]

    # Handle empty filtered data
    if filtered_data.empty:
        return {
            "data": [],
            "layout": {
                "title": "No data available for the selected filters",
                "xaxis": {"title": "Region"},
                "yaxis": {"title": "Total Items Sold"}
            }
        }

    # Group data by region and shipping status
    grouped_data = filtered_data.groupby(['region', 'freeship'])['itemssold'].sum().reset_index()
    fig = px.bar(
        grouped_data,
        x='region',
        y='itemssold',
        color='freeship',
        title='Total Items Sold by Region and Shipping Status',
        labels={'freeship': 'Free Shipping', 'itemssold': 'Total Items Sold'}
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', debug=False, port = 8058)
