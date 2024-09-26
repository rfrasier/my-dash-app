from dash import Dash, html, dcc, callback, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import pandas as pd


# Configuration global variables
HOST = '127.0.0.1'
PORT = 8050
DEBUG = True

# App
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ]
)


# Stores
stores = html.Div([
    dcc.Store(id='data-storage', storage_type='session')
])


# Inputs
update_button = html.Div(
    dbc.Button(
        id='update-button',
        children='Update',
        n_clicks=0
    )
)


# Table component
table_component = html.Div(id='table-component')


# Table component creation function
def create_table_component(df: pd.DataFrame) -> html.Div:
    component = html.Div([
        DataTable(
            data=df.to_dict('records')
        )
    ])
    return component


# Data functions
def get_data():
    df = pd.read_csv('data.csv')
    return df


# Callbacks
@callback(
    Output('data-storage', 'data'),
    Output('table-component', 'children'),
    Input('update-button', 'n_clicks'),
    prevent_initial_call=True,
    running=[(Input('update-button', 'disabled'), True, False)]
)
def update_table_component(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    df = get_data()
    df.reset_index(drop=True, inplace=True)
    data = df.to_dict('records')
    component = create_table_component(df)
    return data, component


# Layout
app.layout = html.Div([
    stores,
    html.H1('My Dash App'),
    update_button,
    table_component
])


# Run app
if __name__ == "__main__":
    app.run_server(host=HOST, port=PORT, debug=DEBUG)
