import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
import pandas as pd

MAX_WORDS = 100

def_mappings = pd.read_csv('data/urban_dictionary.csv')
master_names = list(def_mappings['word'])
master_defs = list(def_mappings['definition'])

master_elements = dict(zip(master_names, master_defs))

app = dash.Dash(__name__)

app.config['suppress_callback_exceptions'] = True


word_list = []
for i in range(MAX_WORDS):
    word_list.append(
        html.Div(
            id='word-{}'.format(i),
            className='word-regular',
            n_clicks_timestamp=0
        )
    )

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='dropdown-input',
            options=[{
                'label': i,
                'value': i
            } for i in master_names],
            value=str(master_names[0]),
        ),
        html.Button(
            id='submit-button',
            children='Submit',
            n_clicks=0
        ),
        html.Div(
            children=word_list,
            id='dynamic-display',
            className='def-container'
        ),
        html.Div(
            id='dynamic-display-clicks'
        ),
        dcc.Store(
            id='n-words-store',
            storage_type='memory',
            data=2
        ),
        html.Div(
            id='testing',
            children=[len(def_mappings)]
        )
    ]
)


@app.callback([Output('word-{}'.format(i), 'children') for i in range(MAX_WORDS)],
              [Input('submit-button', 'n_clicks')],
              [State('dropdown-input', 'value')])
def update_words(n_clicks, state):
    global MAX_WORDS, master_elements
    full_def = master_elements[state]
    input_list = full_def.split()
    rest_of_output = [None for i in range(MAX_WORDS - len(input_list))]
    result = input_list + rest_of_output
    if n_clicks > 0:
        return result
    else:
        return [None for i in range(MAX_WORDS)]


@app.callback([Output('word-{}'.format(i), 'style') for i in range(MAX_WORDS)],
              [Input('submit-button', 'n_clicks')],
              [State('dropdown-input', 'value')])
def update_words(n_clicks, state):
    global MAX_WORDS, master_elements
    full_def = master_elements[state]
    input_list = full_def.split()
    display_style_vis = [{'display': 'flex'} for i in input_list]
    rest_of_output = [{'display': 'none'} for i in range(MAX_WORDS - len(input_list))]
    result = display_style_vis + rest_of_output
    if n_clicks > 0:
        return result
    else:
        return [{'display': 'flex'} for i in range(MAX_WORDS)]


@app.callback(
    Output('dynamic-display-clicks', 'children'),
    [Input('word-{}'.format(i), 'n_clicks_timestamp') for i in range(MAX_WORDS)],
    [State('dropdown-input', 'value')])
def get_clicked_div(*args):
    global master_elements
    clicks = list(args)[:-1]
    split_text = master_elements[args[-1]].split()
    last_clicked_idx = clicks.index(max(clicks))
    if last_clicked_idx < len(split_text):
        return split_text[last_clicked_idx]
    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True, port=8071)


