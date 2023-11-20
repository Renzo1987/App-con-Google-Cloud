import dash
from dash import dcc
from dash import html
from dash import dash_table
import random
import datetime
import json
from google.cloud import firestore, storage


# Inicializa Storage
client = storage.Client()
bucket_name = 'bucket_ejercicio_gcp'

today = datetime.date.today().strftime('%Y-%m-%d')

# Inicializa Firestore
db = firestore.Client()
tabla_usuarios = db.collection('bbdd-gcp')


# Creacion de funcion para obtener datos de la firestore
def obtener_datos_firesore():
    docs = tabla_usuarios.stream()
    items = [doc.to_dict() for doc in docs]
    return items

# Configura la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('Menú de Navegación'),  # Título de la página

    # Menú de navegación
    dcc.Link('Formulario de Usuarios', href='/formulario'),  # Enlace al formulario
    html.Br(),  # Salto de línea
    dcc.Link('Tabla de Usuarios', href='/tabla_usuarios'),  # Enlace a la tabla de usuarios
    html.Br(),  # Salto de línea

     # Aquí se mostrará el contenido de las páginas
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

 # Callback para cargar el contenido de las páginas
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/formulario':
        # Si el usuario navega al formulario, muestra el contenido del formulario
        return html.Div([
            html.H1('Formulario de Usuarios'),
            dcc.Input(id='nombre', type='text', placeholder='Nombre', value=''),
            dcc.Input(id='email', type='email', placeholder='Email', value=''),
            html.Button('Enviar', id='submit-button', n_clicks=0),
            html.Div(id='output-container-button', children='Hit the button to update.')
        ])
    elif pathname == '/tabla_usuarios':
        # Si el usuario navega a la tabla de usuarios, muestra el contenido de la tabla
        data = obtener_datos_firesore()
        return html.Div([
            html.H1('Tabla de Usuarios'),
            dash_table.DataTable(
                columns=[{'name': key, 'id': key} for key in data[0].keys()],
                data=data
            )
        ])

# Ruta para manejar la subida de datos del formulario
@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.Input('submit-button', 'n_clicks'),
    dash.State('nombre', 'value'),
    dash.State('email', 'value')]
)

def submit_form(n_clicks, nombre, email):
    if n_clicks > 0:  # Verifica si se hizo clic en el botón "Enviar"
        # Obtenemos los datos del formulario
        usuario = {
            'ID': random.randint(100000, 999999),
            'Nombre': nombre,
            'Correo electrónico': email,
            'Fecha de registro': today
        }
        # Guarda los datos en un archivo JSON en S3
        json_data = json.dumps(usuario)
        file_name = f'{usuario["ID"]}_usuario.json'
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(json_data)
        return f'Datos guardados correctamente'  #
    else:
        return 'Aún no se ha hecho clic en el botón "Enviar"'

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)