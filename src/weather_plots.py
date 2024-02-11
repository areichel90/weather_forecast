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

def plot_forecast_interactive(df):
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    # temperature plot
    fig['layout']['yaxis']['title'] = 'Temperature [^oC]'
    fig.add_trace(go.Scatter(x=df.index, y=df['temperature'], name='temperature [^oC]',),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=[32]*len(df),
                             name='Freezing Point',
                             line_dash='dash',
                             showlegend=False),
                  row=1, col=1)
    # snowfall plot
    fig['layout']['yaxis2']['title'] = 'Snowfall [in]'
    fig.add_trace(go.Scatter(x=df.index, y=df['snowfall'], name='hourly snowfall [in]',),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['cum_snow'], name='(total) snowfall [in]', ),
                  row=2, col=1)

    '''for c,col in enumerate(df.columns):
        fig.append_trace(go.Scatter(x=df.index, y=df[col]),
                      row=c+1, col=1)'''

    fig.update_layout(title_text=f'{df.index.min()} - {df.index.max()}',
                      hovermode='x unified',
                      legend_traceorder='normal')
    fig.update_traces(xaxis='x2')
    fig.show()