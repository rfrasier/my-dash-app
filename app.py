from dash import Dash, html, dcc, callback, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import pandas as pd
import datetime as dt


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


# Utility functions
def get_timestamp():
    return dt.datetime.now()


# Data functions
def get_data():
    df = pd.read_csv('data.csv')
    return df


# Callbacks
# TODO: Uncomment this callback, which tries to combine the bottom two, and comment out the bottom two in order to see the error: Maximum update depth exceeded. This can happen when a component repeatedly calls setState inside componentWillUpdate or componentDidUpdate. React limits the number of nested updates to prevent infinite loops.
# @callback(
#     Output('data-storage', 'data'),
#     Output('table-component', 'children'),
#     Input('update-button', 'n_clicks'),
#     prevent_initial_call=True,
#     running=[(Input('update-button', 'disabled'), True, False)]
# )
# def store_data(n_clicks):
#     # Log to terminal
#     print(f"{get_timestamp()}\tstore_data()\tn_clicks={n_clicks}\ttriggered_id={ctx.triggered_id}")
#     if n_clicks == 0:
#         raise PreventUpdate
#     df = get_data()
#     df.reset_index(drop=True, inplace=True)
#     data = df.to_dict('records')
#     component = create_table_component(df)
#     return data, component


@callback(
    Output('data-storage', 'data'),
    Input('update-button', 'n_clicks'),
    prevent_initial_call=True,
    running=[(Input('update-button', 'disabled'), True, False)]
)
def store_data(n_clicks):
    # Log to terminal
    print(f"{get_timestamp()}\tstore_data()\tn_clicks={n_clicks}\ttriggered_id={ctx.triggered_id}")
    if n_clicks == 0:
        raise PreventUpdate
    df = get_data()
    df.reset_index(drop=True, inplace=True)
    data = df.to_dict('records')
    return data


@callback(
    Output('table-component', 'children'),
    Input('data-storage', 'modified_timestamp'),
    State('data-storage', 'data')
)
def update_table(modified_timestamp, data):
    # Log to terminal
    print(f"{get_timestamp()}\tupdate_table()\tmodified_timestamp={modified_timestamp}\ttriggered_id={ctx.triggered_id}")
    if data is None:
        raise PreventUpdate
    df = pd.DataFrame(data)
    component = create_table_component(df)
    return component


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
