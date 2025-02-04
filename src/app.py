# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Importar las pestañas
from layouts.tab_1 import render_tab_1, register_callbacks_tab_1
from layouts.tab_2 import render_tab_2, register_callbacks_tab_2
from layouts.tab_3 import render_tab_3, register_callbacks_tab_3
from layouts.tab_4 import render_tab_4, register_callbacks_tab_4
# Crear la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Análisis de sostenibilidad"),
    
    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label="Formulario Dinámico", value="tab-1"),
        dcc.Tab(label="Diagramas Ternarios", value="tab-2"),
        dcc.Tab(label="Diagrama Radar", value="tab-3"),
        dcc.Tab(label="Diagrama de Barras", value="tab-4")
    ]),
    
    html.Div(id="tabs-content"),

    # Aquí agregamos el dcc.Store a nivel global
    dcc.Store(id="table-data-store", data=None)
])

# Callback para cambiar el contenido según la pestaña seleccionada
@app.callback(
    Output("tabs-content", "children"),
    [Input("tabs", "value")]
)
def render_content(tab):
    if tab == "tab-1":
        return render_tab_1()
    elif tab == "tab-2":
        return render_tab_2()
    elif tab == "tab-3":
        return render_tab_3()
    elif tab == "tab-4":
        return render_tab_4()



# Registrar los callbacks específicos de cada pestaña
register_callbacks_tab_1(app)
register_callbacks_tab_2(app)
register_callbacks_tab_3(app)
register_callbacks_tab_4(app)


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
