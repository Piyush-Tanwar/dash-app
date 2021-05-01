import pandas as pd
pd.set_option('max_rows',20)
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default = "browser"

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table


df_1 = pd.read_excel('tirupati_election.xlsx',sheet_name= 'pie')

df_2 = pd.read_excel('tirupati_election.xlsx',sheet_name= 'table')

df_3 = pd.read_excel('tirupati_election.xlsx',sheet_name= 'bar_chart')

df_3['2019 Margin %'] = df_3['2019 Margin %']*100

df_3['2021 Margin %'] = df_3['2021 Margin %']*100

def pie_chart(df):
    fig = px.pie(data_frame = df,names = df.columns[0],values = df.columns[1])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(legend=dict(
    orientation="h",
    #yanchor="bottom",
    y=1.02,
    xanchor="center",
    x=1))
    return fig

def bar_chart(df):
    ac_seg=df['AC Segment']

    fig = go.Figure(data=[
        go.Bar(name='2019 Margin%', x=ac_seg, y=df['2019 Margin %']),
        go.Bar(name='2021 Margin%', x=ac_seg, y=df['2021 Margin %'])
    ])
# Change the bar mode
    fig.update_layout(barmode='group')
    return fig


def graph1():
    return dcc.Graph(id='pie_chart',figure=pie_chart(df_1))

def graph2():
    return dcc.Graph(id='bar_chart',figure=bar_chart(df_3))

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Tirupati byElections'

app.layout = html.Div([
    html.H1("Tirupati Election results"),
    graph1(),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i}
                 for i in df_2.columns],
        data=df_2.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ),
    graph2()
    ])



if __name__ == '__main__':
    app.run_server()