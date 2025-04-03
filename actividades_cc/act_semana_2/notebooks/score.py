
import json
import joblib
import pandas as pd
from azureml.core.model import Model
from zorrouno import processor


def init():
    global model
    global scaler
    # Obtener la ruta de los modelos
    model_path = Model.get_model_path('model')
    model = joblib.load(model_path)

    scaler_path = Model.get_model_path('model_scaler')
    scaler = joblib.load(scaler_path)


def run(raw_data):
    try:
        # Cargar los datos de entrada
        data = json.loads(raw_data)['data'][0]
        data = pd.DataFrame(data)

        # Procesar los datos (embeddings o transformaciones previas)
        embedded_data = processor.embbed(data)

        # Escalar los datos utilizando el scaler
        scaled_data = scaler.transform(embedded_data)

        # Realizar la predicción con el modelo
        result_finals = model.predict(scaled_data)

        # Devolver el resultado en formato JSON
        return json.dumps(result_finals.tolist())  # Convertir a lista para serialización
    except Exception as e:
        return json.dumps(str(e))

