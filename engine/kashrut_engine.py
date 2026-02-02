import os
import json
import time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Rol: Actúas como un experto en certificación de alimentos Kosher ("Mashguiaj Digital") con capacidades avanzadas de visión por computadora y análisis de texto.

Objetivo: Analizar fotos de productos o descripciones textuales para determinar su estatus de Kashrut de forma precisa, rápida y segura.

Instrucciones de Análisis:
1. Identificación de Hechsher (Símbolos): Escanea la imagen meticulosamente en busca de símbolos de certificación (OU, OK, Star-K, KMD, Kehilah, etc.). Identifica cuál es y si es reconocido internacionalmente. Ten cuidado con logos que parecen sellos pero no lo son (veganos, gluten-free).
2. Clasificación de Categoría: Clasifica el producto en una de estas categorías:
   - Lácteo (Dairy): Contiene leche o derivados.
   - Cárnico (Meat): Contiene carne o derivados.
   - Parve: Neutral (ni carne ni leche).
   - Pesaj: Indica si es apto para Pesaj.
3. Análisis de Ingredientes (OCR): Si hay lista de ingredientes, busca aditivos críticos (gelatina, carmín, E120, manteca, emulsificantes no kosher, etc.).
4. El Factor "Duda": Si no estás 100% seguro de un ingrediente o sello, tu dictamen debe ser "DUDOSO" o "REQUIERE REVISIÓN". En temas de Halajá, ante la duda, somos estrictos. DEBES decir: "No se puede determinar con certeza, consulte a su Rabino local".
5. Advertencias Especiales: Busca si aplica "Leche no supervisada" (Jalav Stam) o "Pat Israel".

Formato de Respuesta (JSON Estricto):
Debes responder ÚNICAMENTE en este formato JSON (sin markdown extra):
{
  "producto": "Nombre del producto",
  "estado": "Kosher Parve / Kosher Dairy / Kosher Meat / No Kosher / Dudoso (o Requiere Revisión)",
  "símbolos_encontrados": ["Lista de hechshers detectados o 'Ninguno'"],
  "ingredientes_alerta": ["Lista de ingredientes problemáticos o 'Ninguno'"],
  "justificación": "Explicación técnica/teológica. Menciona si es apto para Pesaj o si hay duda.",
  "advertencia": "Alertas especiales (Jalav Stam, Pat Israel, o si requiere supervisión constante)."
}
"""

class KashrutEngine:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no encontrada en las variables de entorno.")
        genai.configure(api_key=api_key, transport='rest')
        
        # Primary model - using stable flash model
        self.primary_model = genai.GenerativeModel('gemini-flash-latest', system_instruction=SYSTEM_PROMPT)
        # Fallback model - using pro model
        self.fallback_model = genai.GenerativeModel('gemini-pro-latest', system_instruction=SYSTEM_PROMPT)

    def _is_quota_error(self, error):
        """Check if the error is a quota/rate limit error."""
        error_str = str(error).lower()
        return '429' in error_str or 'quota' in error_str or 'rate limit' in error_str

    def _try_generate_content(self, model, prompt, image, max_retries=3):
        """
        Try to generate content with retry logic and exponential backoff.
        """
        for attempt in range(max_retries):
            try:
                response = model.generate_content([prompt, image])
                return response
            except Exception as e:
                if self._is_quota_error(e):
                    if attempt < max_retries - 1:
                        # Exponential backoff: 2^attempt seconds
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue
                    else:
                        # Last attempt failed, raise the error
                        raise
                else:
                    # Non-quota error, raise immediately
                    raise
        return None

    def analyze_product(self, image: Image.Image):
        """
        Envía la imagen a Gemini y devuelve el JSON estructurado.
        Implements retry logic and fallback model support.
        """
        prompt = "Analiza este producto para Kashrut y responde solo en JSON."
        
        try:
            # Try primary model first
            response = self._try_generate_content(self.primary_model, prompt, image)
            
        except Exception as e:
            # If quota error, try fallback model
            if self._is_quota_error(e):
                try:
                    response = self._try_generate_content(self.fallback_model, prompt, image, max_retries=2)
                except Exception as fallback_error:
                    return {
                        "error": "Límite de cuota de API excedido. Por favor, intenta de nuevo más tarde o verifica tu plan de API.",
                        "estado": "Error",
                        "detalles": str(fallback_error)
                    }
            else:
                return {
                    "error": f"Error al procesar la imagen: {str(e)}",
                    "estado": "Error"
                }
        
        try:
            # Limpiar la respuesta por si Gemini incluye tildes invertidas de markdown
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            return json.loads(content)
        except Exception as e:
            return {
                "error": f"Error al parsear la respuesta: {str(e)}",
                "estado": "Error"
            }

    def analyze_text(self, text: str):
        """
        Analiza una lista de ingredientes en texto.
        """
        prompt = f"""
        Analiza la siguiente lista de ingredientes y detalles del producto para determinar su estatus de Kashrut.
        
        TEXTO DEL PRODUCTO:
        "{text}"
        
        Responde ÚNICAMENTE en el formato JSON especificado en las instrucciones del sistema.
        """
        
        try:
            # Try primary model first
            response = self._try_generate_content(self.primary_model, prompt, None) # Image is None
            
        except Exception as e:
             # If quota error, try fallback model
            if self._is_quota_error(e):
                try:
                    response = self._try_generate_content(self.fallback_model, prompt, None, max_retries=2)
                except Exception as fallback_error:
                    return {
                        "error": "Límite de cuota de API excedido.",
                        "estado": "Error",
                        "detalles": str(fallback_error)
                    }
            else:
                 return {
                    "error": f"Error al procesar el texto: {str(e)}",
                    "estado": "Error"
                }

        try:
            # Clean response
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            return json.loads(content)
        except Exception as e:
            return {
                "error": f"Error al parsear la respuesta: {str(e)}",
                "estado": "Error"
            }
