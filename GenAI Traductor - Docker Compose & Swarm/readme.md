---
# 🌐 Traductor Gen-AI: Orquestación con Docker Compose & Swarm

Este proyecto es una aplicación de traducción de texto impulsada por Inteligencia Artificial Generativa (Google Gemini 2.5 Flash). La solución implementa un ciclo completo de MLOps y DevOps, desde el desarrollo local orquestado con Docker Compose, hasta un despliegue escalable y resiliente en Docker Swarm, con seguimiento de experimentos integrado mediante MLflow.

## ✨ Características

- **Frontend Interactivo:** Interfaz construida con **Gradio** para una experiencia de usuario fluida.
- **Motor de Traducción:** Utiliza el modelo `gemini-2.5-flash` para traducciones rápidas y precisas.
- **Trazabilidad (MLOps):** Integración con **MLflow** para registrar cada traducción, métricas de latencia, parámetros de configuración y artefactos (archivos de texto entrada/salida).
- **Orquestación Dual:**
  - **Desarrollo:** `docker-compose.yml` para pruebas locales rápidas.
  - **Producción:** `docker-stack.yml` para despliegue en clúster Swarm con réplicas y alta disponibilidad.
- **Escalabilidad:** Capacidad de escalar horizontalmente el servicio de traducción sin interrupciones.
---
## 📸 Vistas Previas (Screenshots)

A continuación se muestran algunas capturas de pantalla de la aplicación en funcionamiento. Todos los screenshots utilizados en este documento se encuentran en la carpeta `/ScreenshotsTraductor`.

---

## 🏗️ Arquitectura del Sistema

La aplicación se compone de dos microservicios principales que se comunican a través de una red privada:

1. **`app-traductor`**: Contenedor Stateless que aloja la aplicación Python/Gradio. En modo Swarm, este servicio se escala para manejar múltiples peticiones (balanceado por el *Routing Mesh* de Docker).
2. **`mlflow-server`**: Servidor centralizado para el seguimiento de experimentos. Utiliza volúmenes persistentes para almacenar la base de datos de ejecuciones (`mlflow.db`) y los artefactos generados.

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
git clone <URL_del_repositorio>
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

### **Modo 2: Ejecución con Docker Compose 🛠️**

Utiliza este modo para construir la imagen localmente y verificar la integración.

```
# Levantar el entorno de desarrollo
docker-compose up --build
```

* **App de Traducción:** [http://localhost:7860](https://www.google.com/search?q=http://localhost:7860&authuser=2)
* **MLflow UI:** [http://localhost:5001](https://www.google.com/search?q=http://localhost:5001&authuser=2)

Para detener el entorno: `docker-compose down`

### **Modo 2.1: Producción (Docker Swarm) 🚀**

Simula un entorno de producción real utilizando la imagen publicada en Docker Hub (`reaper001/traductor-genai:1.0.0`).

**Paso 1: Inicializar el Clúster**

```
docker swarm init
```

**Paso 2: Cargar Variables y Desplegar**

```
# Cargar la API KEY en la sesión actual (necesario para Swarm)
export $(xargs < .env)

# Desplegar el stack
docker stack deploy -c docker-stack.yml traductor_stack
```

**Paso 3: Verificar y Escalar**

```
# Ver el estado de los servicios
docker stack services traductor_stack

# Escalar la aplicación a 3 réplicas (Load Balancing)
docker service scale traductor_stack_app-traductor=3
```

* **Acceso:** La aplicación sigue disponible en el puerto `7860` y Docker balanceará automáticamente la carga entre las 3 réplicas.

**Paso 4: Limpiar**

```
docker stack rm traductor_stack
```

## 📦 Docker Hub

La imagen de producción está disponible públicamente:
👉 [reaper001/traductor-genai](https://hub.docker.com/r/reaper001/traductor-genai)

## 📝 Estructura del Proyecto

```
.
├── ScreenshotsTraductor/  # Imágenes y evidencias del funcionamiento
├── .dockerignore          # Exclusiones para la construcción de la imagen
├── .gitignore             # Archivos ignorados por Git
├── Taller - Traductor.docx # Informe y documentación del taller
├── app.py                 # Código fuente principal de la aplicación
├── docker-compose.yml     # Orquestación para Desarrollo Local
├── docker-stack.yml       # Orquestación para Producción (Swarm)
├── Dockerfile             # Receta de construcción de la imagen
├── dockerHub-link.txt     # Enlace al repositorio de la imagen
├── readme.md              # Este archivo
└── requirements.txt       # Dependencias del proyecto
```

## 👨‍💻 Autores

* **Anderson Bornachera Balaguera** - *Desarrollador del Proyecto* - `reaper001` (Docker Hub)
* **Juan Andrés Mosquera Núñez** - *Desarrollador del Proyecto*
