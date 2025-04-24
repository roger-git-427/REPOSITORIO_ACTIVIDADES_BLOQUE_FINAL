# Actividad 3

Este repositorio ilustra un flujo de _end-to-end_ para crear, versionar y desplegar un modelo de **Random Forest** en Azure ML empleando un único **pipeline** de _scikit-learn_.  
El objetivo es mostrar cómo:

1. Preprocesar y entrenar localmente.  
2. Empaquetar el preprocesador + modelo en un solo artefacto (`pipeline.pkl`).  
3. Subir y desplegar ese artefacto como un servicio web escalable en Azure ML.  
4. Validar el servicio mediante llamadas a la API.

---

## Estructura del proyecto

```
.
├── model/
│   └── build_pipeline.ipynb      # Preprocesado + entrenamiento + exportación .pkl
├── notebooks/
│   ├── get_data.ipynb            # Extracción de datos desde Azure SQL
│   └── upload_model.ipynb        # Creación de Workspace y despliegue
├── api/
│   └── test_endpoint.ipynb       # Consumo de la API publicada
├── requirements.txt
└── README.md
```

| Carpeta / archivo                  | Descripción breve |
| ---------------------------------- | ----------------- |
| **model**                          | Entrenamiento y generación del `pipeline.pkl`, que combina el preprocesador y el clasificador `RandomForestClassifier`. Con esto evitamos registrar dos modelos independientes. |
| **notebooks/get_data.ipynb**       | Conecta a una base de datos **Azure SQL** que contiene la base de ejemplo _AdventureWorks_, extrae tablas de ventas y guarda los datos limpiados en formato Parquet/CSV. |
| **notebooks/upload_model.ipynb**   | “Deployer”: crea (o reutiliza) un Workspace de Azure ML, sube el `pipeline.pkl`, define el entorno de ejecución con sus dependencias, configura la inferencia (CPU/cores, imagen base, entry script) y publica el servicio. |
| **api/test_endpoint.ipynb**        | Ejemplo de cómo llamar al endpoint REST (token, cabeceras, _payload_, parseo de respuesta) para comprobar que todo funcione. |

---

## Requisitos previos

| Herramienta / servicio       | Recomendado            |
| ---------------------------- | ---------------------- |
| **Python**                   | = 3.11.9 |
| **Azure CLI**                | ≥ 2.60 |
| **Extensión Azure ML**       | `az extension add -n ml` |
| **Bibliotecas**              | ver `requirements.txt` |
| **URI**                      | {"URI": ["URL"]}|
| **Suscripción de Azure**     | rol _Contributor_ sobre el _Resource Group_ de destino |
| **Base de datos Azure SQL**  | Acceso de lectura y cadena de conexión válidos |

---

## 🚀 Pasos para reproducir

1. **Clona el repo y crea el entorno:**

   ```bash
   git clone https://github.com/tu-usuario/nombre-repo.git
   cd nombre-repo
   python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Obtén los datos** (opcional si ya los tienes):

   1. Abre `notebooks/get_data.ipynb`.  
   2. Introduce la cadena de conexión de Azure SQL.  
   3. Ejecuta el notebook; generará un archivo `SalesLT.csv`.

3. **Entrena y crea el pipeline:**

   1. Abre `model/Modelo.ipynb`.  
   2. Ajusta hiperparámetros si lo deseas (n_estimators, max_depth, etc.).  
   3. Ejecuta todo; al final tendrás `model/RandomForest_BestModel.pkl` listo.

4. **Despliega en Azure ML:**

   1. Abre `notebooks/upload_model.ipynb`.  
   2. Completa los valores de: suscripción, grupo de recursos, nombre de Workspace, nombre del _compute_ target, etc.  
   3. Ejecuta cada celda. El notebook:  
      - Crea/reutiliza el Workspace.  
      - Registra el artefacto `RandomForest_BestModel.pkl` como **modelo**.  
      - Define el `Environment` (versión de Python + librerías).  
      - Configura la inferencia (`InferenceConfig` + `AciWebservice/AksWebservice`).  
      - Despliega y devuelve la **URL del endpoint** + **clave de acceso**.

5. **Valida el servicio:**

   1. Abre `api/test_endpoint.ipynb`.  
   2. Pega la URL y la clave.  
   3. Ejecuta; verás la predicción JSON en la salida.


## Limpieza

Cuando termines, elimina los recursos para no incurrir en costos:

```bash
az ml workspace delete \
   --name $AZ_WORKSPACE_NAME \
   --resource-group $AZ_RESOURCE_GROUP \
   --yes
```



