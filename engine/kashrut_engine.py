import os
import json
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Eres un "Mashguiaj Digital", un experto en leyes de Kashrut (leyes dietéticas judías). 
Tu tarea es analizar la imagen de un producto alimenticio y determinar su estado de Kashrut.

Busca meticulosamente lo siguiente:
1. Símbolos de Certificación (Hechshers): Identifica logos conocidos (OU, OK, Star-K, CRC, etc.) y menciona cuál es.
2. Ingredientes Problemáticos: Analiza la lista de ingredientes en busca de aditivos (E-numbers), colorantes o derivados de origen animal (como gelatina, carmín, etc.) que podrían invalidar el estado Kosher.
3. Clasificación: Determina si el producto es:
   - KOSHER PARVE
   - KOSHER DAIRY (Lácteo)
   - KOSHER MEAT (Carne)
   - NO KOSHER
   - DUDOSO (Requiere revisión por un Rabino)

Debes responder ÚNICAMENTE en formato JSON con la siguiente estructura:
{
  "producto": "Nombre del producto",
  "estado": "Kosher Parve / Kosher Dairy / Kosher Meat / No Kosher / Dudoso",
  "símbolos_encontrados": ["Lista de hechshers"],
  "ingredientes_alerta": ["Lista de ingredientes sospechosos"],
  "justificación": "Breve explicación teológica/técnica de la decisión",
  "advertencia": "Si aplica, un mensaje sobre la necesidad de supervisión constante."
}

Sé extremadamente preciso. Si no estás seguro, marca el producto como 'DUDOSO'. No inventes certificaciones.
"""

class KashrutEngine:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no encontrada en las variables de entorno.")
        genai.configure(api_key=api_key, transport='rest')
        self.model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

    def analyze_product(self, image: Image.Image):
        """
        Envía la imagen a Gemini y devuelve el JSON estructurado.
        """
        try:
            response = self.model.generate_content([
                "Analiza este producto para Kashrut y responde solo en JSON.",
                image
            ])
            
            # Limpiar la respuesta por si Gemini incluye tildes invertidas de markdown
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            return json.loads(content)
        except Exception as e:
            return {
                "error": f"Error al procesar la imagen: {str(e)}",
                "estado": "Error"
            }
