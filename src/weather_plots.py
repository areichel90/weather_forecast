import matplotlib.pyplot as plt
import plotly.graph_objects as go


def plot_temp(df):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    _temp = ax.plot(df.index, df.temperature, label='Temperature')
    _snow = ax2.plot(df.index, df.snowfall/2.54, label='Snowfall', c='orange')
    ax.set_ylabel("Temp [^oC]")
    ax2.set_ylabel("Snow Accumulation [in]")
    plots = _temp + _snow
    labels = [i.get_label() for i in plots]
    ax.legend(plots, labels)
    plt.show()

    #return fig

def plot_forecast_interactive(df, location, display_vis=True):
    from plotly.subplots import make_subplots
    print("plotting")
    fig = go.FigureWidget(make_subplots(rows=3, cols=1, shared_xaxes=True))

    # temperature plot
    fig['layout']['yaxis']['title'] = 'Temperature [^oC]'
    fig.add_trace(go.Scatter(x=df.index, y=df['temperature'], name='temperature [^oF]',),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['apparent_temp'], name='feels like [^oF]', ),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['windchill_temp'], name='windchill [^oF]', ),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=[32]*len(df),
                             name='Freezing Point',
                             line_dash='dash',
                             showlegend=False),
                  row=1, col=1)

    # snowfall plot
    plot_index = 2
    fig['layout'][f'yaxis{plot_index}']['title'] = 'Precipitation [in]'
    fig.add_trace(go.Scatter(x=df.index, y=df['snowfall'], name='hourly snowfall [in]',),
                  row=plot_index, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['cum_snow'], name='(total) snowfall [in]', ),
                  row=plot_index, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['perc_precip']/100, name='perc precip [^oF]', ),
                  row=plot_index, col=1)

    # windplot
    plot_index = 3
    fig['layout'][f'yaxis{plot_index}']['title'] = 'Wind [tbd]'
    fig.add_trace(go.Scatter(x=df.index, y=df['wind_speed'], name='windspeed [km/h]', ),
                  row=plot_index, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['cover'], name='cloud cover [%]', ),
                  row=plot_index, col=1)


    fig.update_layout(title_text=f'{df.index.min()} - {df.index.max()}<br>Lat/Lon: {location.lat}, {location.lon}'
                                 f'<br>Last Updated {location.lastUpdated}',
                      height=650,
                      hovermode='x unified',
                      legend_traceorder='normal')
    fig.update_traces(xaxis='x3')
    if display_vis:
        fig.show()

    return fig