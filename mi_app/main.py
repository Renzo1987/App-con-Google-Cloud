import json
from google.cloud import storage, firestore

def funcion_gcp(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print(f"Processing file: {file['name']}.")

# Creando instancias de Cloud Storage y Cloud Firestore
storage_client = storage.Client()
firestore_client = firestore.Client()

def gcs_to_firestore(event, context):
    # Obtiene el nombre del bucket y la clave del archivo JSON del evento de GCS
    bucket = event['bucket']
    file_name = event['name']
    print(bucket)
    print(file_name)

    # Descarga el archivo JSON desde Cloud Storage
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(file_name)
    json_data = blob.download_as_text()

    # Parsea el JSON
    data = json.loads(json_data)

    # Inserta los datos en Cloud Firestore
    db = firestore.Client()
    doc_ref = db.collection('bbdd-ejercicio-gcp').document()
    doc_ref.set({
        'ID': data['ID'],
        'Nombre': data['Nombre'],
        'Correo electrónico': data['Correo electrónico'],
        'Fecha de registro': data['Fecha de registro']
    })

    return 'Proceso completado'
