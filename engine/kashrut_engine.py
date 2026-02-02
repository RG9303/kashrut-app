import os
import json
import time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Rol: Actúas como un experto en certificación de alimentos Kosher ("Mashguiaj Digital") con capacidades avanzadas de visión por computadora y análisis de texto.

Objetivo: Analizar fotos de productos o descripciones textuales para determinar su estatus de Kashrut bajo estándares rigurosos.

Instrucciones de Análisis Profundo:

1. Identificación de Hechsher: Escanea la imagen meticulosamente en busca de símbolos de certificación. Identifica cuál es y si es reconocido internacionalmente.
2. Detección de Alérgenos Críticos (Estatus DE):
   - Si el producto dice "Parve" pero en alérgenos indica "Puede contener leche", "Trazas de leche" o "Equipo compartido con leche", el estatus debe ser "DE" (Dairy Equipment).
   - Si contiene suero de leche (whey), caseína o lactosa, clasifícalo automáticamente como "Lácteo (Dairy)", incluso si el sello es confuso.
3. Verificación de "Bishul Akum":
   - En productos con arroz, pasta o legumbres cocidas, busca si el sello especifica "Bishul Israel". Si no lo indica, advierte sobre la precaución de Bishul Akum.
4. Reconocimiento de Sellos Falsos:
   - Distingue entre una "K" genérica y sellos oficiales. Si detectas solo una "K" sin logo/marco de agencia reconocida, responde: "Sello no verificado: La letra K por sí sola no garantiza supervisión".
5. Análisis de Frutas y Verduras (Insectos):
   - Si es un vegetal congelado/enlatado (brócoli, coliflor, fresas, espinacas) y NO tiene sello de revisión de insectos (tipo Bodek), advierte: "Requiere revisión por presencia de insectos".
6. Alcohol y Bebidas:
   - En vinos/jugos de uva, verifica estrictamente "Mevushal" o "Non-Mevushal". Si es vino sin sello reconocido, es "No Kosher".

Formato de Respuesta (JSON Estricto):
Debes responder ÚNICAMENTE en este formato JSON (sin markdown extra):
{
  "resultado": "Kosher / No Kosher / Dudoso",
  "confianza_analisis": "0-100%",
  "sello_detectado": "Nombre de la agencia o 'Ninguno' o 'K Genérica'",
  "categoria": "Parve / Dairy / Meat / DE (Dairy Equipment)",
  "alertas": ["Lista de alertas (ej. 'Contiene alérgenos lácteos', 'Posible Bishul Akum', 'Requiere revisión de insectos')"],
  "explicacion_halajica": "Texto breve y claro justificando el dictamen (ej. 'Producto Parve elaborado en equipo lácteo')."
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

    def _try_generate_content(self, model, content_list, _unused_arg=None, max_retries=3):
        """
        Try to generate content with retry logic and exponential backoff.
        """
        for attempt in range(max_retries):
            try:
                response = model.generate_content(content_list)
                return response
            except Exception as e:
                # Exponential backoff
                time.sleep(2 ** attempt)
                if attempt == max_retries - 1:
                    raise e
        return None

    def analyze_product(self, images):
        """
        Analiza una o varias imágenes de un producto.
        Args:
            images: Puede ser una sola imagen (PIL.Image) o una lista de imágenes.
        """
        prompt = "Analiza estas imágenes (frente y reverso) del producto. Busca sellos en el frente y revisa ingredientes al reverso. Si no se ve bien, avisa en 'alertas'."
        
        # Ensure input is a list
        if not isinstance(images, list):
            images = [images]

        content = [prompt] + images

        try:
            # Try primary model
            response = self._try_generate_content(self.primary_model, content)
            return self._parse_response(response)
        except Exception as e:
            print(f"Error con modelo primario: {e}")
            try:
                # Try fallback model
                response = self._try_generate_content(self.fallback_model, content)
                return self._parse_response(response)
            except Exception as e2:
                return {"error": f"Error en análisis de imágenes: {str(e2)}"}

    def _parse_response(self, response):
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
        Analiza la siguiente lista de ingredientes y detalles del producto para determinar su estatus de Kashrut bajo estándares rigurosos (Deep Analysis).
        
        TEXTO DEL PRODUCTO:
        "{text}"
        
        Instrucciones especiales para texto:
        - Si no se mencionan sellos en el texto, asume que NO tiene sello (Sello: 'Ninguno').
        - Aplica estricta revisión de ingredientes (E-numbers, gelatina, cochinilla/carmín).
        - Si es un producto procesado sin sello explícito, el resultado debe ser NO KOSHER o DUDOSO.
        
        Usa el mismo formato JSON estricto que para las imágenes:
        {{
          "resultado": "Kosher / No Kosher / Dudoso",
          "confianza_analisis": "0-100%",
          "sello_detectado": "Nombre o 'Ninguno'",
          "categoria": "Parve / Dairy / Meat / DE",
          "alertas": ["Lista de alertas"],
          "explicacion_halajica": "Explicación breve"
        }}
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
