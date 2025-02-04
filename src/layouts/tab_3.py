from dash import html, dcc, Input, Output, dash_table
import numpy as np
import numpy as np

import plotly.graph_objects as go

# Layout de la pestaña 3
def render_tab_3():
    return html.Div([
    dcc.Markdown("""En este diagrama se visualiza el valor del índice de sostenibilidad 
                 de cada uno de los escenarios de acuerdo con el porcentaje de importancia seleccionado."""),
    
    html.Div([
        html.Label("Importancia de la dimensión ambiental (%):"),
        dcc.Input(id='input-lca', type='number', value=25, min=0, max=100, step=1),
        html.Label("Importancia de la dimensión económica (%):"),
        dcc.Input(id='input-lcc', type='number', value=25, min=0, max=100, step=1),
        html.Label("Importancia de la dimensión técnica (%):"),
        dcc.Input(id='input-tech', type='number', value=25, min=0, max=100, step=1),
        html.Label("Importancia de la dimensión social (%):"),
        dcc.Input(id='input-soc', type='number', value=25, min=0, max=100, step=1),
    ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '10px'}),
    
    html.Button("Actualizar Gráfico", id='update-button', n_clicks=0),
    
    dcc.Graph(id='radar-plot', style={'margin-top': '20px'}),

    html.Div([
    html.H4("Descripción:"),
    dash_table.DataTable(
        id='description-table',
        columns=[{'name': 'Descripción', 'id': 'Descripcion'}],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={'fontWeight': 'bold'}
    )])
])



# Callbacks específicos de la pestaña 3
def register_callbacks_tab_3(app):
    @app.callback(
        Output('radar-plot', 'figure'),
        Input('update-button', 'n_clicks'),
        Input('input-lca', 'value'),
        Input('input-lcc', 'value'),
        Input('input-tech', 'value'),
        Input('input-soc', 'value'),
        Input('table-data-store', 'data')
    )
    def update_radar_plot(n_clicks, porc1, porc2, porc3, porc4,data):
        if porc1 + porc2 + porc3 + porc4 != 100:
            return go.Figure().update_layout(
                title="La suma de los porcentajes debe ser igual a 100",
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            )
        
        # Datos de entrada
        Val_LCA = np.array(data['LCA'],dtype=np.float64)
        Val_LCC = np.array(data['LCC'],dtype=np.float64)
        Val_Tech = np.array(data['Tech'],dtype=np.float64)
        Val_Social = np.array(data['SLCA'],dtype=np.float64)

        m = data['method']
        m1 = data['method1']
        m2 = data['method2']
        m3 = data['method3']
                
        #LCA
        if m == 'min':
            minVal_LCA = np.amin(Val_LCA)
            Vaadim_LCA = minVal_LCA/Val_LCA
        elif m == 'max':
            minVal_LCA = np.amax(Val_LCA)
            Vaadim_LCA = Val_LCA/minVal_LCA
        #LCC
        if m1 == 'min':
            minVal_LCC = np.amin(Val_LCC)
            Vaadim_LCC = minVal_LCC/Val_LCC
        elif m1 == 'max':
            minVal_LCC = np.amax(Val_LCC)
            Vaadim_LCC = Val_LCC/minVal_LCC
        # Tech
        if m2 == 'min':
            maxVal_Tech = np.amin(Val_Tech)
            Vaadim_Tech = maxVal_Tech/Val_Tech
        elif m2 == 'max':
            maxVal_Tech = np.amax(Val_Tech)
            Vaadim_Tech = Val_Tech/maxVal_Tech
        # Soc
        if m3 == 'min':
            maxVal_Soc = np.amin(Val_Social)
            Vaadim_Soc = maxVal_Soc/Val_Social
        elif m3 == 'max':
            maxVal_Soc = np.amax(Val_Social)
            Vaadim_Soc = Val_Social/maxVal_Soc

        # Calcular valores
        valores = []
        for j in range(len(Vaadim_LCA)):
            ValA_t = porc1 / 100 * Vaadim_LCA[j]
            ValB_t = porc2 / 100 * Vaadim_LCC[j]
            ValC_t = porc3 / 100 * Vaadim_Tech[j]
            ValD_t = porc4 / 100 * Vaadim_Soc[j]
            suma = ValA_t + ValB_t + ValC_t + ValD_t
            valores.append(suma)

        categories = ['A', 'B', 'C', 'D', 'E', 'F']

        # Generar el radar plot
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categories,
            fill='toself',
            name='Escenario'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False
        )
        return fig
    
    @app.callback(
        Output('description-table','datap'),
        Input('table-data-store','data')
    )
    def update_descriptions(data):
        if data and 'Descrip' in data:
            return [{'Descripcion': desc} for desc in data['Descrip']]
        return []