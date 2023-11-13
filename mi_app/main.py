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

def write_to_firestore(request):
    # Inicializa el cliente de Firestore
    db = firestore.Client()

    # Nombre de la colección y documento en Firestore
    collection_name = "mi-coleccion"
    document_name = "mi-documento"

    # Datos a escribir en Firestore (puedes personalizar esto según tus necesidades)
    data = {
        'campo1': 'valor1',
        'campo2': 'valor2',
        'campo3': 'valor3'
    }

    # Escribe los datos en Firestore
    doc_ref = db.collection(collection_name).document(document_name)
    doc_ref.set(data)

    return 'Datos escritos en Firestore correctamente.'

