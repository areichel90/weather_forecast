from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from noaa_api_test import *

latlon = [42.68, -71.13]  # north andover
_loc = location(latlon)
_loc.get_forecast()
df = process_data(_loc)

# --- base figure
style = 'SLATE'
forecast_fig = plot_forecast_interactive(df, _loc, display_vis=False)
load_figure_template('DARKLY')

# --- dash stuff
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
application = app.server
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "2.5%",
    "padding": "2rem 1rem",
    #"background-color": "#f8f9fa",
}
sidebar = html.Div([
    html.Br(),
    html.H4("Latitude: ", style={'display':"inline-block", 'margin-right':10}),
    dcc.Input(type='text',
              value=42.68,
              id='lat_in'),
    html.Br(),
    html.H4("Longitude: ", style={'display':"inline-block", 'margin-right':10}),
    dcc.Input(type='text',
              value=-71.13,
              id='lon_in'),
    html.Br(),html.Br(),
    html.Button(id="run_button", n_clicks=0, children="Submit", style={'margin-left': 10})
    ],
    style=SIDEBAR_STYLE)
content = html.Div([dcc.Graph(figure=forecast_fig, id='graph-content')])
app.layout = html.Div([
    html.H1(children=f'NOAA Weather Forecast',
            style={'textAlign':'left'}),
    dbc.Row(
        [dbc.Col(sidebar, width=2),
         dbc.Col(dcc.Graph(figure=forecast_fig, id='graph-content'), width='10')]
    ),
])


@callback(
    Output('graph-content', 'figure'),
    Input('run_button', 'n_clicks'),
    State('lat_in', 'value'),
    State('lon_in', 'value')
)
def update_graph(n_clicks, lat_in, lon_in):
    print(f"Input latitude: {lat_in}\nInput Longitude: {lon_in}")
    _loc = location([lat_in, lon_in])
    _loc.get_forecast()
    df = process_data(_loc)
    return plot_forecast_interactive(df, _loc, display_vis=False)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port='8085')
    #app.run(debug=True)
