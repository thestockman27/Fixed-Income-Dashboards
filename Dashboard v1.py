import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from fredapi import Fred
import yfinance as yf
from datetime import datetime, timedelta

# FRED API Key - Replace with your own key
api_key = "d7800cdb73138b20cc3428f1c05d45bd"
fred = Fred(api_key=api_key)

# Get Treasury yield curve data from FRED
def get_yield_curve_data():
    tenors = ["GS10", "GS5", "GS2", "GS1M"]
    data = {}
    for tenor in tenors:
        try:
            data[tenor] = fred.get_series(tenor, start_date="2020-01-01")
        except Exception as e:
            print(f"Error fetching data for {tenor}: {e}")
    return data

def calculate_forward_rates(yield_curve_data):
    forward_rates = {}
    for tenor, data in yield_curve_data.items():
        forward_rates[tenor] = (data - data.shift(1)) / data.shift(1)
    return forward_rates

# Get ETF performance data
def get_etf_performance(etf_symbols, period="1d"):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Adjust the period as needed

    etf_data = yf.download(etf_symbols, start=start_date, end=end_date, progress=False)['Adj Close']
    return etf_data

# Initial data load
yield_curve_data = get_yield_curve_data()
forward_rates = calculate_forward_rates(yield_curve_data)
etf_symbols = ["LQD", "TLT", "EMLC"]  # Replace with actual ETF symbols
etf_data = get_etf_performance(etf_symbols)

# Create the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
# Panel 1: 2D Yield Curve with Reversed Order and Dots
dcc.Graph(
    id='2d-yield-curve',
    figure={
        'data': [
            go.Scatter(x=list(reversed(yield_curve_data.keys())), y=yield_curve_data[tenor],
                       mode='markers', name=tenor)
            for tenor in reversed(list(yield_curve_data.keys()))
        ],
        'layout': go.Layout(
            title='2D US Treasury Yield Curve',
            xaxis=dict(title='Tenor'),
            yaxis=dict(title='Yield Rate'),
        )
    }
),







    # Panel 2: ETF Performance
    html.Div([
        html.H3('ETF Performance'),
        dcc.Dropdown(
            id='etf-period-dropdown',
            options=[
                {'label': 'Daily', 'value': '1d'},
                {'label': 'Weekly', 'value': '1wk'},
                {'label': 'Monthly', 'value': '1mo'},
                {'label': 'Year to Date', 'value': 'ytd'},
            ],
            value='1d',
            style={'width': '50%'}
        ),
        dcc.Graph(
            id='etf-performance',
            figure={
                'data': [
                    go.Scatter(x=etf_data.index, y=etf_data[symbol], mode='lines', name=symbol)
                    for symbol in etf_data.columns
                ],
                'layout': go.Layout(title='ETF Performance')
            }
        ),
    ]),
])

# Callbacks to update the graphs based on user input
@app.callback(
    Output('etf-performance', 'figure'),
    [Input('etf-period-dropdown', 'value')]
)
def update_etf_performance(selected_period):
    etf_data = get_etf_performance(etf_symbols, period=selected_period)
    figure = {
        'data': [
            go.Scatter(x=etf_data.index, y=etf_data[symbol], mode='lines', name=symbol)
            for symbol in etf_data.columns
        ],
        'layout': go.Layout(title='ETF Performance')
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
