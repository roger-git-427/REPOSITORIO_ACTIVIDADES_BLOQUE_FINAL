
# Actividad 4

# 🧠 Aprendizaje Federado con MNIST

Este proyecto implementa un sistema de **aprendizaje federado** para la clasificación de dígitos manuscritos utilizando el dataset **MNIST**. La arquitectura se basa en un enfoque distribuido, donde múltiples clientes entrenan modelos localmente con sus propios datos y un modelo global central se encarga de coordinar el proceso de agregación de los modelos.

## 🧩 Componentes del sistema

* **Modelo central (global)** que coordina el proceso de aprendizaje federado.
* **Clientes (locales)** que entrenan sus modelos de manera independiente.
* **Tres estrategias de agregación** que combinan los modelos locales para actualizar el modelo global.

---

## 🚀 Comenzando

### 📋 Prerrequisitos

* Python 3.11+
* `pip`
* `virtualenv` (recomendado)

### 🔧 Instalación

1. Clona el repositorio.

2. Crea y activa el entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## 🧮 Métodos de Agregación

1. **Promedio (Federated Averaging)**
   Combina los modelos locales promediando los pesos de cada uno. Es el método estándar en aprendizaje federado.

2. **Mediana (Federated Median)**
   Agrega los modelos tomando la mediana de los pesos en cada capa, lo que hace al modelo más robusto ante valores atípicos.

3. **Media Recortada (Trimmed Mean)**
   Se eliminan los extremos (25% inferior y 25% superior) en los valores de cada peso y se promedian los valores restantes. Esto reduce el impacto de outliers.

---

## 📂 Estructura de Archivos

| Archivo                        | Descripción                                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| `final_file_cc_4.ipynb`        | Script principal que coordina el modelo global y aplica las tres estrategias de agregación. |
| `local_train_<nombre>.ipynb`   | Entrenamiento local con los datos de cada cliente.                                          |
| `my_model_<nombre>.keras`      | Pesos del modelo entrenado por cada cliente.                                                |
| `TheModel.py`                  | Define la arquitectura de red neuronal utilizada para todos los clientes.                   |
| `requirements.txt`             | Lista de dependencias necesarias para ejecutar el proyecto.                                 |

---

## 👥 Equipo

* Avril Ruiz
* Adrian Pineda
* Rogelio Lizárraga
* Victor Garza
* Fernando Varela

---

