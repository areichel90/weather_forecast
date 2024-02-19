from dash import Dash, html, dcc, callback, Output, Input, State
from noaa_api_test import *

latlon = [42.68, -71.13]  # north andover
_loc = location(latlon)
_loc.get_forecast()
df = process_data(_loc)

# --- base figure
forecast_fig = plot_forecast_interactive(df, _loc, display_vis=False)

# --- dash stuff
app = Dash(__name__, )
application = app.server
app.layout = html.Div([
    html.H1(children=f'NOAA Weather forecast',
            style={'textAlign':'left'}),
    html.H4("Latitude: ", style={'display':"inline-block", 'margin-right':10}),
    dcc.Input(type='text',
              value=42.68,
              id='lat_in'),
    html.H4(" ", style={'display':"inline-block", 'margin-right':10}),
    html.H4("Longitude: ", style={'display':"inline-block", 'margin-right':10}),
    dcc.Input(type='text',
              value=-71.13,
              id='lon_in'),
    html.Button(id="run_button", n_clicks=0, children="Submit", style={'margin-left': 10}),
    dcc.Graph(figure=forecast_fig, id='graph-content')
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
    application.run(host='0.0.0.0', port='8081')
    #app.run(debug=True)
