def funcion_gcp(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print("hola mundo")
    print(f"Processing file: {file['name']}.")
