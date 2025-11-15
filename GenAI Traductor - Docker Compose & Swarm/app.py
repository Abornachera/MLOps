# app.py
import os
import gradio as gr
import time
import mlflow
from openai import OpenAI 
from dotenv import load_dotenv


# Cargar la API key de Google
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") 
if not api_key:
    raise ValueError("Falta la variable de entorno GOOGLE_API_KEY.")

# Configuración de MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5001")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Nombre del experimento
mlflow.set_experiment("Traductor-GENAI")


# Configurar el cliente de OpenAI para usar Gemini
client = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
  api_key=api_key,
)

# Idiomas disponibles
LANGUAGES = [
    "English", "Spanish", "French", "German", "Italian",
    "Portuguese", "Dutch", "Russian", "Japanese", "Chinese (Simplified)"
]

def translate_text(text, target_language):
    """
    Traduce un texto y registra la interacción como un "run" en MLflow.
    """
    if not text.strip():
        return "Por favor ingresa un texto."

    with mlflow.start_run():
        start_time = time.time()

        prompt = f"Traduce el siguiente texto al {target_language}:\n\n{text}\n\nResponde solo con la traducción."
        
        mlflow.log_param("idioma_objetivo", target_language)
        mlflow.log_param("longitud_original", len(text))
        mlflow.log_param("modelo_usado", "gemini-2.5-flash")

        try:
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=800
            )
            translation = response.choices[0].message.content.strip()

            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000

            mlflow.log_metric("latencia_ms", round(latency_ms, 2))
            mlflow.log_metric("longitud_respuesta", len(translation))

            # --- NUEVAS LÍNEAS PARA GUARDAR ARTEFACTOS ---
            # Guarda el texto original en un archivo y lo registra
            mlflow.log_text(text, "input_text.txt")
            
            # Guarda la traducción en otro archivo y lo registra
            mlflow.log_text(translation, "output_translation.txt")

            return translation
            
        except Exception as e:
            mlflow.log_param("error", str(e))
            return f"Error: {e}"
        
# Interfaz con Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Traductor Gen-AI")
    input_text = gr.Textbox(label="Texto a traducir", lines=6, placeholder="Escribe aquí el texto...")
    target_lang = gr.Dropdown(choices=LANGUAGES, label="Idioma destino", value="English")
    translate_btn = gr.Button("Traducir")
    output = gr.Textbox(label="Traducción", lines=6)

    translate_btn.click(translate_text, inputs=[input_text, target_lang], outputs=output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)