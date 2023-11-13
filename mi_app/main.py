import json
from google.cloud import storage

def funcion_gcp(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print("hola mundo")

def print_json_content(event, context):
    # Obtén información sobre el archivo desde el evento de Cloud Storage
    bucket_name = event['bucket']
    file_name = event['name']

    # Inicializa el cliente de Cloud Storage y descarga el archivo JSON
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    json_data = blob.download_as_text()

    # Parsea el JSON
    data = json.loads(json_data)

    # Imprime los datos en los registros de la función
    print(f'Datos del archivo {bucket_name}/{file_name}:')
    print(json.dumps(data, indent=2))

    # Puedes agregar más lógica según tus necesidades

    return 'Proceso completado'
