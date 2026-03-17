import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

app = Flask(__name__)

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    return genai.Client()

@app.route("/")
def index():
    """Ruta principal que sirve la interfaz HTML."""
    return render_template('index.html')

@app.route("/api/corregir", methods=["POST"])
def corregir_texto():
    """
    Endpoint (API) que recibe texto y el nivel de corrección,
    construye un prompt, consulta a Gemini y devuelve la respuesta.
    """
    try:
        client = get_gemini_client()
    except Exception as e:
         print(f"Error al inicializar cliente: {e}")
         return jsonify({"error": "Error de configuración de API de Gemini en el servidor. Verifica las variables de entorno de Vercel."}), 500

    # 1. Obtener datos JSON del frontend (fetch)
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400

    texto_original = data.get("texto", "")
    nivel_correccion = data.get("nivel_correccion", "ortografia")

    # 2. Validaciones básicas
    if not texto_original or len(texto_original.strip()) == 0:
        return jsonify({"error": "El texto proporcionado está vacío"}), 400
    
    niveles_validos = ["ortografia", "estilo", "formal", "informal"]
    if nivel_correccion not in niveles_validos:
        return jsonify({"error": "Nivel de corrección no válido"}), 400

    # 3. Construcción del Prompt dinámico para la IA
    system_instruction = (
        "Eres un experto editor y corrector de textos en español. "
        "Tu tarea es corregir el texto provisto por el usuario basándote en el nivel de corrección solicitado. "
        "Devuelve la respuesta estrictamente en formato JSON válido con las siguientes claves: "
        "'texto_corregido' (string con la versión final) y "
        "'explicacion' (string detallando los cambios importantes realizados)."
    )
    
    prompt_usuario = (
        f"Texto original:\n\"{texto_original}\"\n\n"
        f"Nivel de corrección deseado: {nivel_correccion}.\n"
        f"Aplica las correcciones necesarias según el nivel solicitado."
    )

    # 4. Llamada a la API del modelo gemini-2.5-flash usando google-genai
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_usuario,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json", # Forzamos a Gemini a devolver JSON puro
            ),
        )
        
        # Ocasionalmente el modelo podría empaquetar el json en bloques ```json ... ```,
        # pero la config response_mime_type ayuda a mitigar eso en las versiones nuevas.
        texto_respuesta = response.text
        
        # En caso de que el modelo retorne texto crudo que pueda ser parseado como JSON en el frontend
        # Pasamos el string directamente (que ya es formato json gracias a response_mime_type)
        import json
        try:
             # Validamos que sea un JSON válido desde backend
             resultado_json = json.loads(texto_respuesta)
             return jsonify(resultado_json)
        except json.JSONDecodeError:
             # Si no es un JSON válido por algún motivo, armamos nosotros la respuesta
             return jsonify({
                 "texto_corregido": texto_respuesta, 
                 "explicacion": "No se pudo parsear el formato esperado."
             })
             
    except Exception as e:
        # 5. Manejo de Errores de la API
        print(f"Error de llamada a la API de Gemini: {e}")
        return jsonify({"error": f"Error del servidor al procesar la solicitud con la IA: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
