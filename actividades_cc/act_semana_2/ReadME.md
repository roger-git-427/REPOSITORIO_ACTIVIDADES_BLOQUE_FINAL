```markdown
```

# (CLOUD COMPUTING) Actividad de la semana 2

# Inferencia y Consumo de la API

## Pasos de Instalación

1. **Clonar o Forkear el Repositorio**  
   Clona o haz un fork de este repositorio para tenerlo en tu propio entorno local.

2. **Crear y Activar un Entorno Virtual** 
   Para crear un ambiente virtual y activarlo debes correr los siguientes comandos en tu terminal:

   #### En Linux/Mac/Windows
   ```bash
   python -m venv .venv
   ```

   #### En Linux/Mac
   ```bash
   . .venv/bin/activate
   ```

   #### En Windows
   ```bash
   .venv\Scripts\activate
   ```


3. **Actualizar pip a la Versión 24.0 (o superior)**  
   ```bash
   pip install --upgrade pip==24.0
   ```

4. **Instalar Dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

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
     - Imprime las predicciones.

   
# Proyecto de Clasificación en Azure

Este repositorio contiene el código y los archivos necesarios para entrenar, seleccionar y desplegar un modelo de clasificación en Azure. 

## Requisitos Previos si se quiere hacer su propio despliegue

- **Python 3.11.9**
- **pip 24.0** (Asegúrate de actualizar pip antes de instalar dependencias)
- **Azure Subscription** (Tener credenciales configuradas en un archivo`id_CONFIDENTIAL.json`)


## Entrenamiento y Selección del Modelo

1. **Ejecutar el Notebook de Entrenamiento en la Carpeta `models`**  
   Dentro de la carpeta `models` encontrarás un notebook que se encarga de:
   - Preparar los datos.
   - Entrenar varios modelos de clasificación.
   - Guardar el mejor modelo resultante en un archivo (ej. `best_model.pkl`).


## Despliegue del Modelo en Azure

Existen **dos formas** de realizar el despliegue:

### Opción 1: Usar el archivo `deployment.py`

1. Abre `deployment.py` y ajusta los parámetros que necesites (nombre del workspace, grupo de recursos, ubicación, etc.).
2. Asegúrate de contar con el archivo `id_CONFIDENTIAL.json` configurado con tu **subscription_id**.
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