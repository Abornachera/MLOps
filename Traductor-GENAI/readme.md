# Traductor Gen-AI 🌐

Este proyecto es una aplicación web de traducción de texto, completamente contenedorizada con Docker. La aplicación utiliza una interfaz de Gradio, se conecta a la API de Google Gemini para realizar traducciones y registra cada operación como un experimento en un servidor de MLflow para su trazabilidad y análisis.

---

## ✨ Características

- **Interfaz Web Interactiva:** Interfaz de usuario simple y limpia construida con Gradio.
- **Traducción con IA Generativa:** Utiliza el modelo `gemini-2.5-flash` de Google para traducciones rápidas y de alta calidad.
- **Seguimiento de Experimentos:** Cada traducción se registra en MLflow, guardando parámetros (idioma), métricas (latencia) y artefactos (texto de entrada y salida).
- **Contenedorizada con Docker:** La aplicación y sus dependencias están empaquetadas en imágenes de Docker, garantizando un entorno de ejecución consistente y portable.
- **Manejo Seguro de Secretos:** La clave API nunca se incluye en la imagen de Docker, se pasa de forma segura como una variable de entorno en tiempo de ejecución.

---

## 📸 Vistas Previas (Screenshots)

A continuación se muestran algunas capturas de pantalla de la aplicación en funcionamiento. Todos los screenshots utilizados en este documento se encuentran en la carpeta `/ScreenshotsTraductor`.

---

## 🏗️ Arquitectura del Sistema

La solución se basa en una arquitectura de dos contenedores Docker que se comunican a través de una red virtual, siguiendo las mejores prácticas de microservicios.

1. **Contenedor `app-traductor`:**

   - **Función:** Ejecuta la aplicación principal de Python con la interfaz de Gradio.
   - **Comunicación:** Recibe las peticiones del usuario, se comunica con la API de Google Gemini y envía los resultados del experimento al contenedor de MLflow.
   - **Puerto Expuesto:** `7860`
2. **Contenedor `mlflow-server`:**

   - **Función:** Ejecuta un servidor de seguimiento de MLflow para recibir y almacenar los datos de los experimentos.
   - **Comunicación:** Escucha las peticiones de registro provenientes del contenedor de la aplicación.
   - **Puerto Expuesto:** `5001` (para la UI de MLflow).
3. **Red Docker `traductor-net`:**

   - Una red virtual que permite a los contenedores comunicarse entre sí utilizando sus nombres como si fueran dominios (ej. `http://mlflow-server:5000`).

---

## ⚙️ Requisitos Previos

Para ejecutar este proyecto, necesitarás tener instalado lo siguiente:

- [Python 3.9+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop/) y Docker Desktop.
- [Git](https://git-scm.com/) (para clonar el repositorio).
- Una **Clave API de Google** para la API de Gemini.

---

## 🚀 Cómo Empezar (Dos Modos)

Puedes ejecutar este proyecto de dos maneras: localmente para desarrollo o con Docker para una ejecución aislada y reproducible.

### **Modo 1: Desarrollo Local (Sin Docker) 🐍**

Este modo es ideal para hacer cambios en el código y probar rápidamente. Se utiliza un **entorno virtual** para mantener las dependencias del proyecto aisladas de tu sistema global.

**1. Clonar el Repositorio**

```bash
git clone <URL_de_tu_repositorio>
cd <nombre_del_repositorio>
```

**2. Crear y Activar el Entorno Virtual**
Un entorno virtual es una carpeta que contiene una instalación de Python específica para tu proyecto.

Crear el entorno (solo se hace una vez)

`python3 -m venv venv`

Activar el entorno (se hace cada vez que abres una nueva terminal)

**En macOS / Linux:**

`source venv/bin/activate`

**En Windows:**

`.\venv\Scripts\activate`

Una vez activado, verás `(venv)` al principio de la línea de tu terminal.

**3. Configurar Variables de Entorno**
Crea un archivo llamado `.env` en la raíz del proyecto. Este archivo guardará tu clave API y será ignorado por Git para mantenerla segura.

`GOOGLE_API_KEY="aqui_va_tu_clave_api_de_google"`

**4. Instalar Dependencias**
Este comando instala todas las librerías necesarias (Gradio, MLflow, etc.) **dentro** de tu entorno virtual.

`pip install -r requirements.txt`

**5. Ejecutar la Aplicación y el Servidor MLflow**
Necesitarás dos terminales, ambas con el entorno virtual activado.

```
# En la Terminal 1, inicia el servidor MLflow:
mlflow server --host 127.0.0.1 --port 5001

# En la Terminal 2, inicia la aplicación Gradio:
python app.py
```

**6. Acceder a los Servicios**

* **Aplicación de Traducción:** [http://localhost:7860](http://localhost:7860)
* **Interfaz de MLflow:** [http://localhost:5001](http://localhost:5001)

### **Modo 2: Ejecución con Docker (Recomendado) 🐳**

Este es el método preferido para una ejecución limpia y reproducible, ya que todo funciona dentro de contenedores aislados.

**Paso 1: Crear la red virtual**

`docker network create traductor-net`

**Paso 2: Construir la imagen de la aplicación**

`docker build -t traductor-genai .`

**Paso 3: Iniciar el servidor de MLflow**

```
docker run -d --name mlflow-server --network traductor-net -p 5001:5000 ghcr.io/mlflow/mlflow:v2.13.0 mlflow server --host 0.0.0.0 --port 5000
```

**Paso 4: Iniciar la aplicación, pasando la API Key de forma segura**

```
docker run -d --name app-traductor --network traductor-net -p 7860:7860 -e GOOGLE_API_KEY="tu_api_key_aqui" -e MLFLOW_TRACKING_URI="http://mlflow-server:5000" traductor-genai
```

## ☁️ Ejecutar desde Docker Hub

Esta aplicación también está disponible como una imagen pre-construida en Docker Hub.

```
# Asegúrate de haber creado la red 'traductor-net' e iniciado el contenedor 'mlflow-server' como se indica arriba.
docker run -d --name app-traductor --network traductor-net -p 7860:7860 -e GOOGLE_API_KEY="tu_api_key_aqui" -e MLFLOW_TRACKING_URI="http://mlflow-server:5000" reaper001/traductor-genai:1.0.0
```

## 📝 Estructura del Proyecto

```
.
├── .dockerignore          # Ignora archivos al construir la imagen de Docker (¡muy importante!)
├── .env                   # Archivo local para guardar secretos (ignorado por Git y Docker)
├── .gitignore             # Ignora archivos para el control de versiones de Git
├── Dockerfile             # Receta para construir la imagen de la aplicación
├── ScreenshotsTraductor/  # Capturas de pantalla de la aplicación en funcionamiento
├── app.py                 # El código fuente principal de la aplicación Gradio y MLflow
└── requirements.txt       # Dependencias de Python
```

## 👨‍💻 Autores

* **Anderson Bornachera Balaguera** - *Desarrollador del Proyecto* - `reaper001` (Docker Hub)
* **Juan Andrés Mosquera Núñez** - *Desarrollador del Proyecto*
