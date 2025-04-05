import pandas as pd
import json
import requests

# Cargar los datos
data = pd.read_csv("prueba.csv").drop(["Unnamed: 0", "Bankrupt?"], axis=1)

data_dict = data.to_dict(orient='records') 
data_json = json.dumps({"data": data_dict})  

# Cargar el URI
with open("uri.json", "r") as suri:
    scoring_uri = json.load(suri)["URI"][0]

# Llamar a la API
headers = {"Content-Type": "application/json"}
response = requests.post(scoring_uri, data=data_json, headers=headers)

# Manejar la respuesta
if response.status_code == 200:
    result = json.loads(response.json())  # Asegurar que la respuesta es JSON
    print(result)
    data["Predictions"] = result["predictions"]  
    print("Data first 10 rows with predictions: ")
    print(data.head(10))
else:
    print(f"Error: {response.text}")
