from dash import html, dcc, dash_table, Input, Output, State
import numpy as np

# Layout de la pestaña 1
def render_tab_1():
    return html.Div([
        html.Label("Seleccione el número de escenarios (productos, procesos o tecnologías a comparar):"),
        dcc.Markdown("En la siguiente tabla digite o copie los datos de cada una de las dimensiones (los decimales deben ir con punto (.)."),
        dcc.Dropdown(
            id='dropdown-rows',
            options=[{'label': i, 'value': i} for i in range(1, 11)],
            value=1,
            clearable=False
        ),
        dash_table.DataTable(
            id='dynamic-table',
            columns=[
                {'name': 'Etiqueta', 'id': 'Etiqueta', 'editable': False},
                {'name': 'Ambiental', 'id': 'LCA', 'editable': True,'type':'numeric'},
                {'name': 'Económico', 'id': 'LCC', 'editable': True,'type':'numeric'},
                {'name': 'Técnico', 'id': 'Tech', 'editable': True,'type':'numeric'},
                {'name': 'Social', 'id': 'SLCA', 'editable': True,'type':'text'},
                {'name': 'Descripción', 'id': 'Descripcion', 'editable': True}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            style_header={'fontWeight': 'bold'},
            editable=True
        ),

        html.Label("Selecciona el método de evaluación para la dimensión ambiental:"),
        dcc.RadioItems(
            id='evaluation-method',
            options=[
                {'label': 'Minimizar', 'value': 'min'},
                {'label': 'Maximizar', 'value': 'max'},
            ],
            value='min',
            inline=True,
            style={'margin': '10px 0'}
        ),
        html.Label("Selecciona el método de evaluación para la dimensión económica:"),
        dcc.RadioItems(
            id='evaluation-method1',
            options=[
                {'label': 'Minimizar', 'value': 'min'},
                {'label': 'Maximizar', 'value': 'max'},
            ],
            value='min',
            inline=True,
            style={'margin': '10px 0'}
        ),
        html.Label("Selecciona el método de evaluación para la dimensión técnica:"),
        dcc.RadioItems(
            id='evaluation-method2',
            options=[
                {'label': 'Minimizar', 'value': 'min'},
                {'label': 'Maximizar', 'value': 'max'},
            ],
            value='min',
            inline=True,
            style={'margin': '10px 0'}
        ),
        html.Label("Selecciona el método de evaluación para la dimensión social:"),
        dcc.RadioItems(
            id='evaluation-method3',
            options=[
                {'label': 'Minimizar', 'value': 'min'},
                {'label': 'Maximizar', 'value': 'max'},
            ],
            value='min',
            inline=True,
            style={'margin': '10px 0'}
        ),
        html.Button("Enviar", id="submit-button", n_clicks=0),
        html.Div(id="output-values"),
        
        dcc.Markdown("""Los datos de la dimensión ambiental 
                     corresponden a un valor único resultado del análisis de ciclo de vida después de usar 
                     una herramienta de evaluación (por ejemplo, SimaPro). Otro dato puede ser un impacto 
                     ambiental de un método estandarizado (ReCiPe, CML) como la huella de carbono, 
                     la huella hídrica u otro dato con significancia estadística para medir la dimensión ambiental
                     y los escenarios a comparar."""),
        dcc.Markdown("""Los datos de la dimensión económica corresponden 
                     a un valor único del resultado de un análisis del costo de ciclo de vida. 
                     Otros datos pueden ser el costo del producto o de la con significancia estadística para medir 
                     la dimensión económica y los escenarios a comparar."""),
        dcc.Markdown("""Los datos de la dimensión económica corresponden a un valor único del resultado de un análisis del costo de ciclo de vida. 
                     Otros datos pueden ser el costo del producto o de la con significancia estadística para medir 
                     la dimensión económica y los escenarios a comparar."""),
        dcc.Markdown("""Los datos de la dimensión social corresponden a un valor único resultado de un análisis 
                     social del ciclo de vida de acuerdo con las directrices del programa ambiental de las 
                     naciones unidas. Otros datos ser pueden ser las categorías o subcategorías de la misma 
                     directriz como el número de empleados con significancia estadística de los escenarios a
                      comparar."""),
        dcc.Markdown("""Los datos de la dimensión técnica corresponden a un único valor seleccionado y varios valores 
                     normalizados que pueden ser datos de calidad de un producto, datos de procesamiento como la 
                     resistencia a la tensión de un nuevo material."""),
                     
    ])

# Callbacks específicos de la pestaña 1
def register_callbacks_tab_1(app):
    @app.callback(
        Output('dynamic-table', 'data'),
        Input('dropdown-rows', 'value')
    )
    def update_table(num_rows):
        alphabet = [chr(65 + i) for i in range(26)]
        return [{'LCA': '', 'LCC': '', 'Tech': '', 'SLCA': '', 'Etiqueta': alphabet[i]} for i in range(num_rows)]

    @app.callback(
        Output('table-data-store', 'data'),  # Guardamos los datos en el dcc.Store
        Input('submit-button', 'n_clicks'),
        State('dynamic-table', 'data'),
        State('evaluation-method', 'value'),
        State('evaluation-method1', 'value'),
        State('evaluation-method2', 'value'),
        State('evaluation-method3', 'value')
    )
    def save_data(n_clicks,table_data,evaluation_method,evaluation_method1,evaluation_method2
                  ,evaluation_method3):
        if n_clicks > 0:
            # Convertimos los datos de la tabla en arreglos de NumPy
            lca = np.array([row.get('LCA','') for row in table_data])
            lcc = np.array([row.get('LCC','') for row in table_data])
            tech = np.array([row.get('Tech','') for row in table_data])
            slca = np.array([row.get('SLCA','') for row in table_data])
            description = [str(row.get('Descripcion', '')) for row in table_data]
            return {'LCA': lca.tolist(), 
                    'LCC': lcc.tolist(),
                    'Tech': tech.tolist(),
                    'SLCA': slca.tolist(),
                    'Descrip': description,
                    'method': evaluation_method,
                    'method1': evaluation_method1,
                    'method2': evaluation_method2,
                    'method3': evaluation_method3
                    }
        return {}  # Si no se presionó el botón, retornamos vacío

