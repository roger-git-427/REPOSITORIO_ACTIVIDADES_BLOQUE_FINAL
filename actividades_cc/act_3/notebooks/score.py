scorepy = """
import json 
import joblib
import pandas as pd
import numpy as np
import traceback
import sklearn
from azureml.core.model import Model

def embbed(d):
    try:
        required_columns = ['CustomerID', 'NameStyle', 'Title', 'FirstName', 'MiddleName',
       'LastName', 'Suffix', 'CompanyName', 'SalesPerson', 'EmailAddress',
       'Phone', 'PasswordHash', 'PasswordSalt', 'rowguid', 'ModifiedDate']
         
        missing_columns = [col for col in required_columns if col not in d.columns]
        if missing_columns:
            raise KeyError(f"Missing columns: {missing_columns}")

        return d[required_columns]

    except Exception as e:
        print(f"[ERROR] Unexpected error in embbed(): {e}")
        traceback.print_exc()
        return None

def init():
    global model

    try:
        print("[INFO] Loading model...")
        print(f"[INFO] NumPy version: {np.__version__}")
        print(f"[INFO] Scikit-learn version: {sklearn.__version__}")

        # Reemplaza 'model_name_here' por el nombre real de tu modelo registrado en Azure ML.
        model_dir  = Model.get_model_path('model2')          # ← apunta al directorio
        model_path = os.path.join(model_dir, 'RandomForest_BestModel.pkl')    # ← apunta al fichero
        
        print(f"[INFO] Loading model from {model_path}")
        model = joblib.load(model_path)
        print(f"[INFO] Loaded model from {model_path}!!")

        print("[INFO] Model loaded successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        traceback.print_exc()
        model = None  # Aseguramos que sean None si falla la carga

def run(raw_data):
    global model

    try:
        if model is None:
            raise RuntimeError("[ERROR] Model not initialized. Check logs for errors.")

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

        result_finals = model.predict(embedded_data)
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
"""