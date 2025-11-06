
# Taller MLOps: MLflow Tracking, TensorFlow y Ollama

## 👥 Autores

* Anderson Bornachera
* Juan Mosquera


Este repositorio documenta un taller integral de MLOps centrado en el seguimiento de experimentos. El objetivo es aprender a rastrear, comparar y gestionar modelos de Machine Learning utilizando MLflow y, finalmente, interpretar los resultados con un LLM local a través de Ollama.

## 🧰 Herramientas Utilizadas

* **MLflow**: Para el seguimiento de experimentos (Tracking).
* **Scikit-learn**: Para el modelo base (Regresión Logística).
* **TensorFlow/Keras**: Para el modelo de Deep Learning (Red Neuronal).
* **Ollama**: Para la interpretación de resultados con un LLM local (`tinyllama`).
* **Pandas & Numpy**: Para la manipulación y preprocesamiento de datos.
* **Jupyter Notebook**: Como entorno de desarrollo interactivo.

## 🤔 ¿Cómo Empezar desde Cero?

Sigue estos pasos para configurar y ejecutar el proyecto en un nuevo entorno.

### 1. Prerrequisitos

* [Python 3.9+](https://www.python.org/downloads/)
* [Git](https://www.google.com/search?q=https://git-scm.com/downloads&authuser=2)

### 2. Clonar el Repositorio

```
git clone git@github.com:Abornachera/MLOps.git
cd MlFlow-Tracking/
```

### 3. Configurar el Entorno Virtual

Usaremos la carpeta `MLFlowTracking` como nuestro entorno virtual.

```
# Crear el entorno virtual
python3 -m venv MLFlowTracking

# Activar el entorno (macOS/Linux)
source MLFlowTracking/bin/activate
```

### 4. Instalar Dependencias

```
# Instalar todas las librerías necesarias
pip install -r requirements.txt
```

### 5. Iniciar la Interfaz de MLflow

En tu terminal, ejecuta el servidor de MLflow. Este comando creará una carpeta llamada `mlruns`.

```
mlflow ui --port 5000
```

Abre tu navegador y ve a `http://127.0.0.1:5000` para ver la interfaz.


## 📖 Resumen del Taller (Paso a Paso)

Este es un resumen de lo que se construyó en el notebook `mlflowtracking.ipynb`.

### Paso 1 & 2: Carga y Preparación de Datos

* Se cargó el dataset `qsar-biodeg.csv` con Pandas.
* La variable objetivo `class` se convirtió a formato binario (0/1).
* Los datos se dividieron en `X_train`, `X_test`, `y_train`, `y_test`.
* Se aplicó `StandardScaler` a las *features* para normalizar los datos.

### Paso 3: Creación del Experimento

* Se configuró el experimento en MLflow usando `mlflow.set_experiment("QSAR_Biodegradation_Experiment")`.

### Paso 4: Modelo 1 - Regresión Logística (Registro Manual)

* Se entrenó un modelo `LogisticRegression` de Scikit-learn.
* Se utilizó **registro manual** para guardar la información:
  * `mlflow.log_params()` para guardar hiperparámetros (ej. `C`, `solver`).
  * `mlflow.log_metrics()` para guardar métricas de evaluación (ej. `accuracy`, `f1_score`).
  * `mlflow.log_artifact()` para guardar una Matriz de Confusión como imagen.
  * `mlflow.log_text()` para guardar una descripción.

### Paso 5: Modelo 2 - Red Neuronal (Autologging)

* Se construyó una Red Neuronal simple con TensorFlow/Keras.
* Se activó el **autologging** con `mlflow.tensorflow.autolog()`.
* MLflow registró automáticamente todos los parámetros, métricas por época (ej. `val_loss`, `val_accuracy`) y el modelo final sin código adicional.

### Paso 6: Comparación de Modelos

* Se utilizó la **interfaz de MLflow** (`http://127.0.0.1:5000`) para seleccionar y comparar los dos  *runs* .
* Se analizaron los gráficos de Coordenadas Paralelas y la tabla de métricas para determinar qué modelo tenía mejor rendimiento (`f1_score` vs `val_accuracy`).

### Paso 7: Interpretación con Ollama

* Se utilizó un LLM local (Ollama con `tinyllama`) para analizar los resultados.
* Se le hicieron preguntas como "¿Qué significa un F1-score de 0.89?" y "¿Por qué la NN tendría un F1 más bajo pero un accuracy más alto?".
* La conversación se guardó en `interpretacion_ollama.txt` y se subió a MLflow como un artefacto con `mlflow.log_artifact()`.

### Paso 8: Runs Anidados y Autologging Combinado

* Se activó el autologging general con `mlflow.autolog()`.
* **Anidamiento (Nested Runs):** Se demostró cómo agrupar experimentos, creando un "Run Padre" (`LR_Hyperparameter_Search`) que contenía múltiples "Runs Hijos" (cada prueba de un valor `C` diferente).
* **Combinado:** Se demostró que `mlflow.autolog()` capturó tanto el `fit` de Scikit-learn (en el run anidado) como el `fit` de TensorFlow (en un run separado), probando su capacidad para manejar múltiples frameworks.


## 🤖 Guía de Instalación de Ollama (macOS)

### A. Si NO tienes Ollama instalado:

1. **Descargar:** Ve al sitio web oficial: `https://ollama.com/`
2. **Instalar:** Haz clic en "Download for macOS". Se descargará un archivo `.zip`. Descomprímelo y ejecuta la aplicación "Ollama".
3. **Mover a Aplicaciones:** Arrastra el ícono de Ollama a tu carpeta de Aplicaciones.
4. **Verificar:** Abre tu Terminal. Ollama se ejecuta como un servicio en segundo plano.
5. **Descargar un Modelo:** Para este taller, `tinyllama` es ligero y suficiente (ya que `llama2` puede requerir más RAM de la disponible).
   **Bash**

   ```
   ollama pull tinyllama
   ```
6. **Ejecutar:** Una vez descargado, inicia el chat:
   **Bash**

   ```
   ollama run tinyllama
   ```
7. ¡Listo! Ya puedes chatear con el modelo. Escribe `/bye` para salir.

### B. Si YA tienes Ollama instalado:

1. **Abrir Terminal:** Abre tu terminal.
2. **Verificar Modelos:** Revisa qué modelos tienes descargados localmente.
   **Bash**

   ```
   ollama list
   ```
3. **Descargar Modelo (si es necesario):** Si no ves `tinyllama:latest` (o el modelo que deseas) en la lista, descárgalo:
   **Bash**

   ```
   ollama pull tinyllama
   ```
4. **Ejecutar:** Inicia el chat con el modelo que desees:
   **Bash**

   ```
   ollama run tinyllama
   ```


## 📂 Estructura del Proyecto

```
.
├── MLFlowTracking/	       # (Entorno virtual - Ignorado)
├── mlruns/		       # (Datos de MLflow - Ignorado)
├── ScreenshotsMLFlow/         # (Capturas de pantalla)
├── Informe.docx.              # (Informe breve del proyecto)
├── interpretacion_ollama.txt  # (Chat con tinyllama)
├── mlflowtracking.ipynb       # (Notebook con todo el código)
├── qsar-biodeg.csv	       # (Dataset usado)
├── requirements.txt           # (Dependencias utilizadas)
└── .gitignore
```
