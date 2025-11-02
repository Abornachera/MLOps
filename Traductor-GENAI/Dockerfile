# 1. Usamos una imagen base de Python oficial y ligera.
FROM python:3.10-slim

# 2. Establecemos el directorio de trabajo dentro del contenedor.
WORKDIR /app

# 3. Copiamos el archivo de requerimientos primero
COPY requirements.txt .

# 4. Instalamos todas las dependencias del proyecto.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el código del proyecto al contenedor.
COPY . .

# 6. Se expone el puerto que Gradio usa para que sea accesible desde fuera.
EXPOSE 7860

# 7. El comando que se ejecutará para iniciar la aplicación.
CMD ["python", "app.py"]