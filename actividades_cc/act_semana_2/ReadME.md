```markdown
# Proyecto de Clasificación en Azure

Este repositorio contiene el código y los archivos necesarios para entrenar, seleccionar y desplegar un modelo de clasificación en Azure. El despliegue puede realizarse de dos formas:

1. **Editando y ejecutando el archivo `deployment.py`**  
2. **Ejecutando el notebook `deployment.ipynb`**

## Requisitos Previos

- **Python 3.11.9**
- **pip 24.0** (Asegúrate de actualizar pip antes de instalar dependencias)
- **Azure Subscription** (Credenciales configuradas en `id_CONFIDENTIAL.json`)

## Pasos de Instalación

1. **Clonar o Forkear el Repositorio**  
   Clona o haz un fork de este repositorio para tenerlo en tu propio entorno local.

2. **Crear y Activar un Entorno Virtual**  
   ```bash
   python -m venv venv
   # En Linux/Mac
   source venv/bin/activate
   # En Windows
   venv\Scripts\activate
   ```

3. **Actualizar pip a la Versión 24.0 (o superior)**  
   ```bash
   pip install --upgrade pip==24.0
   ```

4. **Instalar Dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

## Entrenamiento y Selección del Modelo

1. **Ejecutar el Notebook de Entrenamiento en la Carpeta `models`**  
   Dentro de la carpeta `models` encontrarás un notebook (por ejemplo, `train_model.ipynb`) que se encarga de:
   - Preparar los datos.
   - Entrenar varios modelos de clasificación.
   - Guardar el mejor modelo resultante en un archivo (ej. `best_model.pkl`).

2. **Verificar que `best_model.pkl` y `scaler.pkl` estén en la Carpeta `Model`**  
   Estos archivos son necesarios para el despliegue posterior.

## Despliegue del Modelo en Azure

Existen **dos formas** de realizar el despliegue:

### Opción 1: Usar el archivo `deployment.py`

1. Abre `deployment.py` y ajusta los parámetros que necesites (nombre del workspace, grupo de recursos, ubicación, etc.).
2. Asegúrate de contar con el archivo `id_CONFIDENTIAL.json` configurado con tu **subscription_id** u otros datos de acceso.
3. Ejecuta el script:
   ```bash
   python deployment.py
   ```
4. Este script:
   - Registra el modelo y el escalador en Azure.
   - Genera el archivo `score.py` con la lógica de inferencia.
   - Despliega el servicio en Azure y crea el archivo `uri.json` con la URL del endpoint.

### Opción 2: Usar el notebook `Deployment.ipynb`

1. Abre y ejecuta el notebook `Deployment.ipynb`.
2. Asegúrate de actualizar los parámetros (workspace, resource group, etc.) dentro del notebook.
3. Al finalizar, también se generará el archivo `uri.json` con la URL de tu servicio en Azure.

## Inferencia y Consumo de la API

1. **Archivo `API.py`**  
   - Antes de ejecutar `API.py`, edita o reemplaza el archivo `prueba.csv` con los datos que quieras enviar al modelo.
   - Ejecuta:
     ```bash
     python API.py
     ```
   - Este script:
     - Lee el archivo `prueba.csv`.
     - Carga la URI del servicio desde `uri.json`.
     - Envía los datos al endpoint de Azure.
     - Imprime por pantalla las predicciones recibidas.

2. **Nota Importante**  
   Si no deseas consumir la API desde Azure, también puedes hacer inferencias de manera local, pero asegúrate de tener la ruta correcta del modelo y del escalador.

## Equipo y Roles

- **Nombre del Equipo:** Dockercitos 
- **Departamento:** Departamento de Data Science  
- **Roles Desempeñados:**
  - Victor Garza : Departamento de Nube
  - Avril Ruiz: Departamento de Nube
  - Adrián Pineda: Departamento de Modelos
  - Rogelio Lizarraga: Departamento de datos 

## Requisitos Mínimos de Hardware y Sistema

- **Sistema Operativo:** MacOS Classic, OS: System 1 (1984)
- **Memoria RAM:** 256 kb
- **Ancho de Banda:** Dos latas conectadas por una cuerda de fibra óptica
```