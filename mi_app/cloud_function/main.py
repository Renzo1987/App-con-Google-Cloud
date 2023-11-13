from google.cloud import storage
import json

def upload_json_to_bucket(bucket_name, local_json_data, destination_blob_name):
    """Sube datos JSON al bucket de GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convierte los datos JSON en una cadena y carga en el blob
    json_data_str = json.dumps(local_json_data, indent=2)
    blob.upload_from_string(json_data_str, content_type='application/json')

    print(f'Datos JSON subidos a {destination_blob_name} en el bucket {bucket_name}.')

# Ejemplo de uso
bucket_name = 'bucket_ejercicio_gcp'
local_json_data = {'nombre': 'John', 'edad': 30, 'ciudad': 'Ejemplo'}
destination_blob_name = 'datos.json'

upload_json_to_bucket(bucket_name, local_json_data, destination_blob_name)
