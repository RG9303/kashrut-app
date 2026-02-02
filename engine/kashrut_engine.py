import os
import json
import time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Rol: Actúas como un experto en certificación de alimentos Kosher ("Mashguiaj Digital") con capacidades avanzadas de visión por computadora y análisis de texto.

Objetivo: Analizar fotos de productos o descripciones textuales para determinar su estatus de Kashrut bajo estándares rigurosos, utilizando el glosario técnico adjunto.

GLOSARIO DE REFERENCIA:
- Kosher: Apto para el consumo según la ley dietética judía (Halajá).
- No Kosher (Taref): No apto para el consumo.
- Heisher (Hashgajá): Sello de certificación rabínica.
- Parve: Neutro (sin carne ni leche).
- DE (Dairy Equipment): Parve procesado en equipo lácteo. No consumir con carne, pero no requiere espera de 6 horas.
- Lácteo (Dairy / Jalav): Alimento que contiene leche o derivados.
- Jalav Stam: Leche regular (supervisión no constante).
- Jalav Yisrael: Leche supervisada por un judío desde el ordeño.
- Cárnico (Meat / Basar): Contiene carne o derivados.
- Pesaj Kosher: Apto para la Pascua Judía (libre de Jametz).
- Jametz: Granos leudados (prohibidos en Pesaj).
- Kitniyot: Legumbres (prohibidas para Ashkenazim en Pesaj, permitidas para Sefardíes).
- Glatt Kosher: Nivel estricto de kashrut para carne.
- Bishul Israel: Cocinado por un judío. Previene "Bishul Akum".
- Pat Israel: Pan horneado o supervisado por un judío.
- Mevushal: Vino cocinado que mantiene estatus si lo toca un no-judío.
- Non-Mevushal: Vino no cocinado.
- Aditivos Críticos: Gelatina (animal), Carmín (insecto), Glicerina/Mono/Diglicéridos (posible animal), L-Cisteína (plumas/cabello), Emulsificantes.

Instrucciones de Análisis:
1. Identificación de Hechsher: Busca sellos reconocidos. Si solo hay una "K" sin logo, advierte que no está verificado.
2. Detección de Alérgenos: Si es Parve pero dice "Trazas de leche", clasifícalo como "DE".
3. Rigor Halájico: Aplica los términos del glosario para explicar detalladamente el veredicto en 'explicacion_halajica'.
4. Personalización: Ajusta tu respuesta si el usuario indica preferencias específicas (ej. Jalav Yisrael estricto).

Formato JSON Estricto:
{
  "resultado": "Kosher / No Kosher / Dudoso",
  "confianza_analisis": "0-100%",
  "sello_detectado": "Nombre de la agencia o 'Ninguno'",
  "categoria": "Parve / Dairy / Meat / DE",
  "alertas": ["Lista de alertas"],
  "explicacion_halajica": "Justificación técnica basada en el glosario"
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

    def analyze_product(self, images, extra_context=None, preferences=None):
        """
        Analiza una o varias imágenes de un producto.
        Args:
            images: Puede ser una sola imagen (PIL.Image) o una lista de imágenes.
            extra_context: Texto adicional para ayudar al análisis (ej. ingredientes de OpenFoodFacts).
            preferences: Dict con preferencias de kashrut (ej. {"jalav_stam": "strict", "kitniyot": "ashkenazi"}).
        """
        prompt = "Analiza estas imágenes del producto. Busca sellos en el frente y revisa ingredientes al reverso."
        
        if extra_context:
            prompt += f"\n\nCONTEXTO ADICIONAL (De base de datos externa):\n{extra_context}"
            prompt += "\nUsa esta lista de ingredientes para mayor precisión si las fotos no son claras."

        if preferences:
            prompt += f"\n\nPREFERENCIAS DEL USUARIO:\n{json.dumps(preferences, ensure_ascii=False)}"
            prompt += "\nAjusta tu veredicto según estas preferencias (ej. si el usuario es estricto en Jalav Yisrael y el producto es Jalav Stam, indícalo)."

        prompt += "\nSi no se ve bien, avisa en 'alertas'."
        
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

    def analyze_text(self, text: str, preferences=None):
        """
        Analiza una lista de ingredientes en texto.
        """
        prompt = f"""
        Analiza la siguiente lista de ingredientes y detalles del producto para determinar su estatus de Kashrut bajo estándares rigurosos (Deep Analysis).
        
        TEXTO DEL PRODUCTO:
        "{text}"
        """

        if preferences:
            prompt += f"\n\nPREFERENCIAS DEL USUARIO:\n{json.dumps(preferences, ensure_ascii=False)}"
            prompt += "\nAjusta tu veredicto según estas preferencias."

        prompt += """
        Instrucciones especiales para texto:
        - Si no se mencionan sellos en el texto, asume que NO tiene sello (Sello: 'Ninguno').
        - Aplica estricta revisión de ingredientes (E-numbers, gelatina, cochinilla/carmín).
        - Si es un producto procesado sin sello explícito, el resultado debe ser NO KOSHER o DUDOSO.
        
        Usa el mismo formato JSON estricto que para las imágenes:
        {
          "resultado": "Kosher / No Kosher / Dudoso",
          "confianza_analisis": "0-100%",
          "sello_detectado": "Nombre o 'Ninguno'",
          "categoria": "Parve / Dairy / Meat / DE",
          "alertas": ["Lista de alertas"],
          "explicacion_halajica": "Explicación breve"
        }
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

    def extract_barcode(self, image: Image.Image):
        """
        Intenta leer el código de barras numérico de una imagen usando Gemini.
        """
        prompt = "Identifica los dígitos del código de barras (EAN/UPC) en esta imagen. Responde SOLO con el número, sin texto extra. Si no hay código legible, responde '0'."
        
        try:
            # We use flash for speed
            response = self.primary_model.generate_content([prompt, image])
            text = response.text.strip().replace(" ", "").replace("\n", "")
            # Filter only digits
            digits = "".join(filter(str.isdigit, text))
            return digits if len(digits) > 7 else None
        except Exception as e:
            print(f"Error extrayendo barcode: {e}")
            return None
