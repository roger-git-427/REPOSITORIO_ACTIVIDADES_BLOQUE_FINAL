
import json
import joblib
import pandas as pd
import traceback
from azureml.core.model import Model

def embbed(d):
    d.columns = d.columns.str.strip()  # Clean column names

    try:
        d = d[['Net Income to Total Assets', 'ROA(A) before interest and % after tax',
               'ROA(B) before interest and depreciation after tax',
               'ROA(C) before interest and depreciation before interest',
               'Net worth/Assets', 'Debt ratio %',
               'Persistent EPS in the Last Four Seasons',
               'Retained Earnings to Total Assets',
               'Net profit before tax/Paid-in capital',
               'Per Share Net profit before tax (Yuan ¥)',
               'Current Liability to Assets', 'Working Capital to Total Assets',
               "Net Income to Stockholder's Equity", 'Borrowing dependency',
               'Current Liability to Current Assets', 'Liability to Equity',
               'Net Value Per Share (A)', 'Net Value Per Share (B)',
               'Net Value Per Share (C)', 'Current Liability to Equity',
               'Bankrupt?']]
    except KeyError as e:
        print(f"[ERROR] Missing columns: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error in embbed(): {e}")
        return None
    return d

def init():
    global model
    global scaler
    try:
        # Obtener la ruta de los modelos
        model_path = Model.get_model_path('model')
        model = joblib.load(model_path)

        scaler_path = Model.get_model_path('model_scaler')
        scaler = joblib.load(scaler_path)

        print("[INFO] Model and scaler successfully loaded.")
    except Exception as e:
        print(f"[ERROR] Failed to load model or scaler: {e}")
        traceback.print_exc()

def run(raw_data):
    try:
        # Cargar los datos de entrada
        data_dict = json.loads(raw_data)
        if "data" not in data_dict:
            raise ValueError("[ERROR] Input JSON must contain a 'data' key.")

        data = data_dict["data"][0]
        if not isinstance(data, list):
            raise ValueError("[ERROR] Expected 'data' to be a list of feature dictionaries.")

        df = pd.DataFrame(data)

        # Procesar los datos (embeddings o transformaciones previas)
        embedded_data = embbed(df)
        if embedded_data is None:
            raise ValueError("[ERROR] Data embedding failed due to missing columns.")

        # Escalar los datos utilizando el scaler
        scaled_data = scaler.transform(embedded_data)

        # Realizar la predicción con el modelo
        result_finals = model.predict(scaled_data)

        # Devolver el resultado en formato JSON
        return json.dumps({"predictions": result_finals.tolist()})  # Convertir a lista para serialización

    except json.JSONDecodeError as e:
        error_msg = f"[ERROR] Invalid JSON input: {e}"
    except ValueError as e:
        error_msg = str(e)
    except Exception as e:
        error_msg = f"[ERROR] Unexpected error in run(): {e} {traceback.format_exc()}"

    print(error_msg)  # Loguear error para depuración
    return json.dumps({"error": error_msg})
