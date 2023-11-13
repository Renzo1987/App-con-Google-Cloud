from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage, firestore
import json
import time

app = Flask(__name__)

storage_client = storage.Client()
bucket_name = 'bucket_ejercicio_gcp'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        fecha = request.form['fecha']

        usuario = {
            "Nombre": nombre,
            "Correo electrónico": correo,
            "Fecha de registro": fecha

            timestamp = int(time.time())  # Obtiene la marca de tiempo actual en segundos
            file_name = f'datos{timestamp}.json'  # Nombre del archivo JSON

            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(file_name)
            blob.upload_from_string(json.dumps(usuario), content_type='application/json')

            time.sleep(3)
            # Redirecciona a la misma página para recargar
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error al guardar en Firestore o GCS: {e}")

    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))