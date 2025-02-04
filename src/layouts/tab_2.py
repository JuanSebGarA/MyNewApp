from dash import html, dcc, Input, Output, State, dash_table
import numpy as np
import pandas as pd
from ternary_plot import create_ternary_contour  

# Layout de la pestaña 2
def render_tab_2():
    return html.Div([
        dcc.Markdown("""Los 4 diagramas ternarios representan la combinación de las 4 dimensiones. 
                     Los ejes incorporan el porcentaje de importancia de cada dimensión y la cuarta dimensión
                      se representa en escala de color donde rojo es el valor más bajo y verde el más alto. 
                     Dentro de los diagramas se encuentran los escenarios escogidos."""),
        dcc.Markdown("""Los tomadores de decisiones podrán visualizar todas las opciones generadas."""),
        html.P("Aquí se mostrará la gráfica."),
        html.Button("Enviar", id="submit-button", n_clicks=0),
                # Contenedor para la primera fila de gráficas
        html.Div([
            dcc.Graph(id="data-graph-1", style={'width': '45%', 'display': 'inline-block'}),
            dcc.Graph(id="data-graph-2", style={'width': '45%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justify-content': 'space-between'}),

        # Contenedor para la segunda fila de gráficas
        html.Div([
            dcc.Graph(id="data-graph-3", style={'width': '45%', 'display': 'inline-block'}),
            dcc.Graph(id="data-graph-4", style={'width': '45%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-top': '20px'}),
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




# Callbacks específicos de la pestaña 2
def register_callbacks_tab_2(app):
    @app.callback(
        [Output('data-graph-1', 'figure'),
         Output('data-graph-2', 'figure'),
         Output('data-graph-3', 'figure'),
         Output('data-graph-4', 'figure')],
        [Input('table-data-store', 'data'),
         Input("submit-button", "n_clicks")],  # Accedemos a los datos guardados
    )
    def create_graph(data,n_clicks):
        if n_clicks > 0:
            if data:
                def categoriza(val):
                    if val == 0:
                        sal = 'A'
                    elif val == 1:
                        sal = 'B'
                    elif val == 2:
                        sal = 'C'
                    elif val == 3:
                        sal = 'D'
                    elif val == 4:
                        sal = 'E'
                    elif val == 5:
                        sal = 'F'
                    return sal

                def categorizainv(val):
                    if val == 'A':
                        sal = 0
                    elif val == 'B':
                        sal = 1
                    elif val == 'C':
                        sal = 2
                    elif val == 'D':
                        sal = 3
                    elif val == 'E':
                        sal = 4
                    elif val == 'F':
                        sal = 5
                    return sal
                # 1. Preprocesamos los datos recibidos del formulario (almacenados en `table-data-store`)
                df_porc = pd.DataFrame(data)  # Asegúrate de que la estructura de los datos sea correcta

                # Extraemos las columnas LCA, LCC, Tech y SLCA
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

                # Adimensionalizamos las variables

                valor_com1 = Vaadim_Soc.tolist()
                valor_com2 = Vaadim_Tech.tolist()
                valor_com3 = Vaadim_LCC.tolist()
                valor_com4 = Vaadim_LCA.tolist()

                # Ahora calculamos los valores para cada caso
                Porc_1 = np.linspace(1, 0, num=100)  # Valor porcentual de LCA
                Porc_2 = np.flip(Porc_1)
                Porc_3 = np.array([])

                Porc_1f = np.array([])
                Porc_2f = np.array([])

                tam = len(Porc_1)
                for i in range(tam):
                    for j in range(tam - i):
                        dif = Porc_1[j + i] + Porc_2[j]
                        valor = np.round(1 - dif, 9)
                        Porc_3 = np.append(Porc_3, valor)
                        Porc_1f = np.append(Porc_1f, Porc_1[j + i])
                        Porc_2f = np.append(Porc_2f, Porc_2[j])
                col1 = Porc_1f.T
                col2 = Porc_2f.T
                col3 = Porc_3.T

                mtrx = np.array([col2,col1,col3]).T
                df_porc = pd.DataFrame(mtrx)
                # Calculamos los valores para los diferentes casos
                # Caso 1: Esto es solo un ejemplo, adapta a tus necesidades
                caso_optimoI = []
                for i in range(len(Porc_1f)):
                    sumas = []
                    for j in range(len(Vaadim_LCA)):
                        valLCA_A = Porc_1f[i] * Vaadim_LCA[j]
                        valLCC_A = Porc_2f[i] * Vaadim_LCC[j]
                        valTec_A = Porc_3[i] * Vaadim_Tech[j]
                        suma = valLCA_A + valLCC_A + valTec_A
                        sumas.append(suma)
                    valmax = max(sumas)
                    index = sumas.index(valmax)
                    caso_optimoI.append(categoriza(index))
                
                
                caso_optimoII=[]
                for i in range(len(Porc_1f)):
                    sumas = []
                    for j in range(len(Vaadim_LCA)):
                        valLCA_B = Porc_1f[i]*Vaadim_LCA[j]
                        valLCC_B = Porc_2f[i]*Vaadim_LCC[j]
                        valSoc_B = Porc_3[i]*Vaadim_Soc[j]
                        suma = valLCA_B + valLCC_B + valSoc_B
                        sumas.append(suma)
                    valmax = max(sumas)
                    index = sumas.index(valmax)
                    caso_optimoII.append(categoriza(index))

                caso_optimoIII = []
                for i in range(len(Porc_1f)):
                    sumas = []
                    for j in range(len(Vaadim_LCA)):
                        valLCA_C = Porc_1f[i]*Vaadim_LCA[j]
                        valTec_C = Porc_2f[i]*Vaadim_Tech[j]
                        valSoc_C = Porc_3[i]*Vaadim_Soc[j]
                        suma = valLCA_C + valTec_C + valSoc_C
                        sumas.append(suma)
                    valmax = max(sumas)
                    index = sumas.index(valmax)
                    caso_optimoIII.append(categoriza(index))

                caso_optimoIV = []
                for i in range(len(Porc_1f)):
                    sumas = []
                    for j in range(len(Vaadim_LCA)):
                        valLCC_D = Porc_1f[i]*Vaadim_LCC[j]
                        valTec_D = Porc_2f[i]*Vaadim_Tech[j]
                        valSoc_D = Porc_3[i]*Vaadim_Soc[j]
                        suma = valLCC_D + valTec_D + valSoc_D
                        sumas.append(suma)
                    valmax = max(sumas)
                    index = sumas.index(valmax)
                    caso_optimoIV.append(categoriza(index))

                df_porc['Caso Optimo I'] = caso_optimoI
                df_porc['Caso Optimo II'] = caso_optimoII
                df_porc['Caso Optimo III'] = caso_optimoIII
                df_porc['Caso Optimo IV'] = caso_optimoIV

                df_Caso1 = df_porc.filter(items = [0,1,2,'Caso Optimo I'])
                df_Caso2 = df_porc.filter(items = [0,1,2,'Caso Optimo II'])
                df_Caso3 = df_porc.filter(items = [0,1,2,'Caso Optimo III'])
                df_Caso4 = df_porc.filter(items = [0,1,2,'Caso Optimo IV'])

                ValI = []
                for i in df_Caso1['Caso Optimo I']:
                    inde = categorizainv(i)
                    ValI.append(Vaadim_Soc[inde])

                ValII = []
                for i in df_Caso2['Caso Optimo II']:
                    inde = categorizainv(i)
                    ValII.append(Vaadim_Tech[inde])
                    
                ValIII = []
                for i in df_Caso3['Caso Optimo III']:
                    inde = categorizainv(i)
                    ValIII.append(Vaadim_LCC[inde])
                    
                ValIV = []
                for i in df_Caso4['Caso Optimo IV']:
                    inde = categorizainv(i)
                    ValIV.append(Vaadim_LCA[inde])

                df_Caso1['ValI'] = ValI
                df_Caso2['ValII'] = ValII
                df_Caso3['ValIII'] = ValIII
                df_Caso4['ValIV'] = ValIV

                t1 = df_Caso1[0].to_numpy()
                l1 = df_Caso1[1].to_numpy()
                r1 = df_Caso1[2].to_numpy()
                v1 = df_Caso1['ValI'].to_numpy()

                t2= df_Caso2[0].to_numpy()
                l2 = df_Caso2[1].to_numpy()
                r2 = df_Caso2[2].to_numpy()
                v2 = df_Caso2['ValII'].to_numpy()

                t3 = df_Caso3[0].to_numpy()
                l3 = df_Caso3[1].to_numpy()
                r3 = df_Caso3[2].to_numpy()
                v3 = df_Caso3['ValIII'].to_numpy()

                t4 = df_Caso4[0].to_numpy()
                l4 = df_Caso4[1].to_numpy()
                r4 = df_Caso4[2].to_numpy()
                v4 = df_Caso4['ValIV'].to_numpy()
                

                # Definimos los valores de los gráficos, ejemplo para `grafico-1`
                fig1 = create_ternary_contour(np.array([t1,l1,r1]), v1, valor_comp=valor_com1,
                                            pole_labels=['Ambiental', 'Económico', 'Técnico', 'Social'],
                                            colorscale="RdBu",
                                            interp_mode='cartesian',
                                            showscale=True)

                # Crear los otros tres gráficos de manera similar
                fig2 = create_ternary_contour(np.array([t2,l2,r2]), v2, valor_comp=valor_com2,
                                            pole_labels=['Ambiental', 'Económico', 'Social', 'Técnico'],
                                            colorscale="RdBu",
                                            interp_mode='cartesian',
                                            showscale=True)

                fig3 = create_ternary_contour(np.array([t3,l3,r3]), v3, valor_comp=valor_com3,
                                            pole_labels=['Ambiental', 'Técnico', 'Social', 'Económico'],
                                            colorscale="RdBu",
                                            interp_mode='cartesian',
                                            showscale=True)

                fig4 = create_ternary_contour(np.array([t4,l4,r4]), v4, valor_comp=valor_com4,
                                            pole_labels=['Económico', 'Técnico', 'Social', 'Ambiental'],
                                            colorscale="RdBu",
                                            interp_mode='cartesian',
                                            showscale=True)

                # Devolver las figuras
                return fig1,fig2,fig3,fig4
        return{}
    @app.callback(
        Output('description-table','data'),
        Input('submit-button', 'n_clicks'),
        State('table-data-store','data')
    )
    def update_descriptions(n_clicks, data):
        if data and 'Descrip' in data:
            return [{'Descripcion': desc} for desc in data['Descrip']]
        return []