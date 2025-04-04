import json 
import joblib
import pandas as pd
import numpy as np
import traceback
import sklearn
from azureml.core.model import Model

def embbed(d):
    try:
        d.columns = d.columns.str.strip()  # Limpiar nombres de columnas
        required_columns = [
            'Net Income to Total Assets', 'ROA(A) before interest and % after tax',
            'ROA(B) before interest and depreciation after tax',
            'ROA(C) before interest and depreciation before interest',
            'Net worth/Assets', 'Debt ratio %',
            'Persistent EPS in the Last Four Seasons',
            'Retained Earnings to Total Assets',
            'Net profit before tax/Paid-in capital',
            'Per Share Net profit before tax (Yuan �)',
            'Current Liability to Assets', 'Working Capital to Total Assets',
            "Net Income to Stockholder's Equity", 'Borrowing dependency',
            'Current Liability to Current Assets', 'Liability to Equity',
            'Net Value Per Share (A)', 'Net Value Per Share (B)',
            'Net Value Per Share (C)', 'Current Liability to Equity'
        ]

        missing_columns = [col for col in required_columns if col not in d.columns]
        if missing_columns:
            raise KeyError(f"Missing columns: {missing_columns}")

        return d[required_columns]

    except Exception as e:
        print(f"[ERROR] Unexpected error in embbed(): {e}")
        traceback.print_exc()
        return None

def init():
    global model, scaler

    try:
        print("[INFO] Loading model and scaler...")
        print(f"[INFO] NumPy version: {np.__version__}")
        print(f"[INFO] Scikit-learn version: {sklearn.__version__}")

        # Reemplaza 'model_name_here' por el nombre real de tu modelo registrado en Azure ML.
        model_path = Model.get_model_path('model')
        scaler_path = Model.get_model_path('model_scaler')

        print(f"[INFO] Loading model from {model_path}")
        model = joblib.load(model_path)
        print(f"[INFO] Loaded model from {model_path}!!")

        print(f"[INFO] Loading scaler from {scaler_path}")
        scaler = joblib.load(scaler_path)
        print(f"[INFO] Loaded scaler from {scaler_path}!!")

        print("[INFO] Model and scaler loaded successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to load model or scaler: {e}")
        traceback.print_exc()
        model, scaler = None, None  # Aseguramos que sean None si falla la carga

def run(raw_data):
    global model, scaler

    try:
        if model is None or scaler is None:
            raise RuntimeError("[ERROR] Model or scaler not initialized. Check logs for errors.")

        data_dict = json.loads(raw_data)
        if "data" not in data_dict:
            raise ValueError("[ERROR] Input JSON must contain a 'data' key.")

        data = data_dict["data"]
        if not isinstance(data, list):
            raise ValueError("[ERROR] Expected 'data' to be a list of feature dictionaries.")

        df = pd.DataFrame(data)

        print("[INFO] Received data shape:", df.shape)
        print("[INFO] Data columns:", df.columns.tolist())

        embedded_data = embbed(df)
        if embedded_data is None:
            raise ValueError("[ERROR] Data embedding failed due to missing columns.")

        # Verificar si hay valores NaN antes de transformar
        if embedded_data.isnull().values.any():
            raise ValueError("[ERROR] Input data contains NaN values. Please clean your input.")

        scaled_data = scaler.transform(embedded_data)
        print("[INFO] Scaled data shape:", scaled_data.shape)

        result_finals = model.predict(scaled_data)
        print("[INFO] Model prediction output:", result_finals)

        return json.dumps({"predictions": result_finals.tolist()})

    except json.JSONDecodeError as e:
        error_msg = f"[ERROR] Invalid JSON input: {e}"
    except ValueError as e:
        error_msg = str(e)
    except Exception as e:
        error_msg = f"[ERROR] Unexpected error in run(): {e} {traceback.format_exc()}"

    print(error_msg)
    return json.dumps({"error": error_msg})
