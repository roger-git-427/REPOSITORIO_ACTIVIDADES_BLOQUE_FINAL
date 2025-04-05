import json

#GETTING MY ID:
id = open('../id_CONFIDENTIAL.json', 'r')
mi = json.load(id)
my_id = mi["my_id"]

## STEP 1: Set up the workspace.
from azureml.core import Workspace

ws = Workspace.create(name="workspace_final_final_final",
                      subscription_id = my_id,
                      resource_group = "resource_group_bank_1_2_3_4",
                      location = "centralindia")

from azureml.core.model import Model

mname = "model"
registered_model = Model.register(model_path="../best_model3.pkl",
                                  model_name=mname,
                                  workspace=ws)

from azureml.core.model import Model

mname_scaler = "model_scaler"
registered_scaler = Model.register(model_path="../scaler2.pkl",
                                  model_name=mname_scaler,
                                  workspace=ws)

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
        required_columns =  [' Net Income to Total Assets', ' ROA(A) before interest and % after tax', ' ROA(B) before interest and depreciation after tax']
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
        model_path = Model.get_model_path('model3')
        scaler_path = Model.get_model_path('model_scaler3')

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
"""

# Guardar el script en un archivo
file_score = open("score.py", "w")
# Guardar el script en un archivo con codificación UTF-8
with open("score.py", "w", encoding="utf-8") as file_score:
    file_score.write(scorepy)

file_score.close()

## STEP 2: Inference configuration: the blueprints for the German carpenter about how to build your furniture.

from azureml.core.environment import Environment
virtual_env = Environment("env-for-bank-1-3")


from azureml.core.conda_dependencies import CondaDependencies
virtual_env.python.conda_dependencies = CondaDependencies.create(
    conda_packages=['numpy==1.23.5','scikit-learn=1.4.2', 'joblib', 'pandas']
)


from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice
inference_config = InferenceConfig(
                                environment=virtual_env,
                                entry_script="score.py",
                                )
aci_config = AciWebservice.deploy_configuration(cpu_cores=0.5, memory_gb=1) ## ASEGÚRENSE DE ASIGNAR SUFICIENTE MADERA PARA SUS MUEBLES.

service = Model.deploy(workspace=ws,
                       name='service',
                       models=[registered_model, registered_scaler],
                       inference_config=inference_config,
                       deployment_config=aci_config,
                       overwrite=True,
                       )

service.wait_for_deployment()

scoring_uri = service.scoring_uri

scoreuri = json.dumps({"URI": [scoring_uri]})
file = open("uri.json", "w")
file.write(scoreuri)
file.close()