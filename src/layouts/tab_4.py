from dash import html, dcc, Input, Output, State, dash_table
import numpy as np
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Layout de la pestaña 2
def render_tab_4():
    return html.Div([
        dcc.Markdown("""El eje “y” del diagrama de barras muestra el índice de sostenibilidad entre 0 y 1, 
                     dividido en intervalos de 1 y las barras el número de veces que cada escenario se ubicó 
                     en el rango correspondiente. El índice de sostenibilidad se obtiene asignando el nivel 
                     de importancia en porcentaje a cada dimensión. El índice de sostenibilidad dependerá del 
                     nivel de importancia asignado por los responsables de la toma de decisiones. 
                     En este diagrama se estiman todos los índices de sostenibilidad posibles haciendo la 
                     composición de los pesos por dimensión en intervalos del 1%."""),
        html.P("Aquí se mostrará la gráfica."),
        html.Button("Enviar", id="submit-button", n_clicks=0),
                # Contenedor para la primera fila de gráficas
        dcc.Graph(id='bar-plot'),
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
def register_callbacks_tab_4(app):
    @app.callback(
        Output('bar-plot', 'figure'),
        [Input('table-data-store', 'data'),
         Input("submit-button", "n_clicks")],  # Accedemos a los datos guardados
    )
    def create_graph(data,n_clicks):
        if n_clicks > 0:
            if data:
                Porc_1f = []
                Porc_2f = []
                Porc_3f = []
                Porc_4f = []

                # Generamos valores de 0 a 1 en incrementos de 0.1
                valores = np.round(np.linspace(0, 1, 21), 2)

                # Bucle anidado para generar todas las combinaciones de cuatro porcentajes que sumen 1
                for p1 in valores:
                    for p2 in valores:
                        for p3 in valores:
                            p4 = np.round(1 - (p1 + p2 + p3), 2)  # Calculamos el cuarto valor para que la suma sea 1
                            # Aseguramos que el cuarto valor está dentro del rango [0,1]
                            if 0 <= p4 <= 1:
                                Porc_4f.append(p1)
                                Porc_3f.append(p2)
                                Porc_2f.append(p3)
                                Porc_1f.append(p4)

                # Crear el DataFrame final con las combinaciones que suman 1
                df_porc = pd.DataFrame({
                    "Porc_1": Porc_1f,
                    "Porc_2": Porc_2f,
                    "Porc_3": Porc_3f,
                    "Porc_4": Porc_4f
                })

                ## ADMINESIONALIZACIONES

                Val_LCA = np.array(data['LCA'],dtype=np.float64)
                Val_LCC = np.array(data['LCC'],dtype=np.float64)
                Val_Tech = np.array(data['Tech'],dtype=np.float64)
                Val_Social = np.array(data['SLCA'],dtype=np.float64)

                ## Maximos y minimos
                minVal_LCA = np.amin(Val_LCA)
                minVal_LCC = np.amin(Val_LCC)
                maxVal_Tech = np.amax(Val_Tech)
                maxVal_Soc = np.amax(Val_Social)

                # Adimensionalizados
                Vaadim_LCA = minVal_LCA/Val_LCA
                Vaadim_LCC = minVal_LCC/Val_LCC
                Vaadim_Tech = Val_Tech/maxVal_Tech
                Vaadim_Soc = Val_Social/maxVal_Soc


                ## VALORES
                valA = []
                valB = []
                valC = []
                valD = []
                valE = []
                valF = []


                for i in range(len(Porc_1f)):
                    for j in range(len(Vaadim_LCA)):
                        ValA_t = Porc_1f[i] * Vaadim_LCA[j]
                        ValB_t = Porc_2f[i] * Vaadim_LCC[j]
                        ValC_t = Porc_3f[i] * Vaadim_Tech[j]
                        ValD_t = Porc_4f[i] * Vaadim_Soc[j]
                        suma = ValA_t+ValB_t+ValC_t+ValD_t
                        
                        if j == 0:
                            valA.append(suma)
                        elif j == 1:
                            valB.append(suma)
                        elif j == 2:
                            valC.append(suma)
                        elif j == 3:
                            valD.append(suma)  
                        elif j == 4:
                            valE.append(suma)
                        elif j == 5:
                            valF.append(suma)
                    


                dicc = {'valA': valA, 'valB': valB, 'valC': valC, 'valD': valD, 'valE': valE, 'valF': valF}

                ran1 = 0
                ran2 = 0
                ran3 = 0
                ran4 = 0
                ran5 = 0
                ran6 = 0
                ran7 = 0
                ran8 = 0
                ran9 = 0
                ran10 = 0

                mat = []

                for elemento, lista in dicc.items():
                    ran1 = 0
                    ran2 = 0
                    ran3 = 0
                    ran4 = 0
                    ran5 = 0
                    ran6 = 0
                    ran7 = 0
                    ran8 = 0
                    ran9 = 0
                    ran10 = 0
                    for i in lista:
                        if  round(i,2) <= 0.10:
                            ran1 += 1
                        elif round(i,2) <= 0.20:
                            ran2 += 1
                        elif round(i,2) <= 0.30:
                            ran3 += 1
                        elif round(i,2) <= 0.40:
                            ran4 += 1
                        elif round(i,2) <= 0.50:
                            ran5 += 1
                        elif round(i,2) <= 0.60:
                            ran6 += 1
                        elif round(i,2) <= 0.70:
                            ran7 += 1
                        elif round(i,2) <= 0.80:
                            ran8 += 1
                        elif round(i,2) <= 0.90:
                            ran9 += 1
                        else:
                            ran10 += 1
                    
                    fil = [ran1,ran2,ran3,ran4,ran5,ran6,ran7,ran8,ran9,ran10]
                    mat.append(fil)
                    

                sumas = [sum(Columnas) for Columnas in zip(*mat)]
                        
                        
                porcentajes = [
                    [round((valor / suma * 100),1) if suma != 0 else 0 for valor, suma in zip(fila, sumas)]
                    for fila in mat
                ]

                transpuesta = list(zip(*porcentajes))
                transpuesta = [list(col) for col in transpuesta]





                # Datos corregidos
                x_data = transpuesta
                y_data = [
                    "0 - 0.1", "0.1 - 0.2", "0.2 - 0.3", "0.3 - 0.4",
                    "0.4 - 0.5", "0.5 - 0.6", "0.6 - 0.7", "0.7 - 0.8",
                    "0.8 - 0.9", "0.9 - 1.0"
                ]

                categories = ["Caso A", "Caso B", "Caso C", "Caso D", "Caso E", "Caso F"]  # Etiquetas para cada columna
                colors = ['#2980b9','#a569bd','#5dade2','#45b39d','#58d68d','#f5b041']
                # Crear la figura
                fig = go.Figure()

                # Control de categorías ya añadidas a la leyenda
                categories_in_legend = set()

                # Crear datos ajustados para incluir ceros
                adjusted_x_data = []
                for yd, xd in zip(y_data, x_data):
                    for (val, category), color in zip(zip(xd, categories), colors):
                        if val != 0:  # Solo incluir valores diferentes de 0
                            show_in_legend = category not in categories_in_legend
                            if show_in_legend:
                                categories_in_legend.add(category)
                            fig.add_trace(go.Bar(
                                x=[val],
                                y=[yd],
                                orientation='h',
                                marker=dict(
                                    color=color
                                ),
                                name=category,
                                hovertemplate=f"{category}: {val}%<extra></extra>",
                                showlegend=show_in_legend  # Incluir categoría solo una vez en la leyenda
                            ))
                        else:
                            # Para los valores cero, agregamos barras vacías con el mismo color, pero no mostrar en la leyenda
                            fig.add_trace(go.Bar(
                                x=[0],  # Barra vacía para el valor cero
                                y=[yd],
                                orientation='h',
                                marker=dict(
                                    color=color,
                                    line=dict(color='rgba(0,0,0,0)', width=0)  # Barra completamente invisible
                                ),
                                name=category,
                                showlegend=False  # No agregar a la leyenda
                            ))

                # Personalizar diseño
                fig.update_layout(
                    barmode='stack',
                    xaxis=dict(showgrid=False, showline=False, showticklabels=True, zeroline=False),
                    yaxis=dict(showgrid=False, showline=False, showticklabels=True, zeroline=False),
                    paper_bgcolor='rgb(248, 248, 255)',
                    plot_bgcolor='rgb(248, 248, 255)',
                    margin=dict(l=150, r=10, t=40, b=80),
                    showlegend=True,
                    legend=dict(traceorder="normal")  # Orden de categorías en la leyenda (A a F, inverso)
)
                return fig
        return{}
    @app.callback(
        Output('description-table','data2'),
        Input('submit-button', 'n_clicks'),
        State('table-data-store','data')
    )
    def update_descriptions(n_clicks, data):
        if data and 'Descrip' in data:
            return [{'Descripcion': desc} for desc in data['Descrip']]
        return []