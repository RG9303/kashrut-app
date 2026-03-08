import os
import json
import time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

try:
    import numpy as np
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    np = None
    cv2 = None

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

ESCÁNER DE BICHOS (Detección de insectos vía imágenes):
- Objetivo: Detectar insectos visibles, fragmentos, huevos o restos macroscópicos que puedan afectar el estatus de Kashrut.
- Requisitos de salida: Si el análisis proviene de imágenes, incluye una clave `insect_scanner` en el JSON con la estructura:
    {
        "detecciones": [{"bbox": [x,y,w,h], "descripcion": "fragmento/whole_insect/egg", "especie_aproximada": "ej. 'ácaro'/'polilla'/'otros' or 'desconocido'", "confianza": "0-100%", "severidad": "Alta/Media/Baja", "accion_recomendada": "Desechar/Inspección humana/Conservar y revisar"}],
        "resumen": "Texto corto sobre presencia de insectos o fragmentos",
        "confianza_global": "0-100%",
        "nota_falsos_positivos": "Ejemplos comunes de falsos positivos: semillas, granos, pigmentos, especias"
    }

- Lógica de decisión mínima:
    - Si se detecta un insecto entero o múltiples fragmentos con confianza >=90% -> marcar como `No Kosher` y `alertas` debe incluir "Insectos visibles - requiere descarte o inspección".
    - Si hay detección con confianza 70-89% -> marcar como `Dudoso` y recomendar "Inspección humana especializada".
    - Si confianza <70% -> etiquetar detección como "Baja confianza" y pedir imágenes de mayor resolución/macro.

- Guía de captura de imágenes para el escáner de bichos:
    - Tomar foto macro (si es posible) con iluminación uniforme y fondo neutro.
    - Incluir una referencia de escala (regla) y varias tomas desde distintos ángulos.
    - Fotografiar el contenido externo y el empaque abierto si procede.

- Consideraciones para evitar falsos positivos: comparar la textura y reflectancia, pedir crops (recortes) del área sospechosa, y contrastar con la lista de ingredientes (semillas/especias que se confunden frecuentemente).

RECOMENDACIONES FUNCIONALES (para la app):
- Interfaz y flujo:
    - Mostrar bounding boxes y una barra de `confianza` por detección; permitir que el usuario marque manualmente como "confirmado" o "falso positivo".
    - Botón para "Solicitar revisión por Mashgiach" que envía imágenes, recortes y metadata (timestamp, user id) a un buzón de revisión.
    - Historial de casos con exportación a PDF con evidencia visual y veredicto.

- Pipeline y modelos:
    - Usar un ensemble: modelo de detección de objetos (insectos/fragmentos) + detector de anomalías de textura y un clasificador especializado.
    - Permitir subida de crop de alta resolución a un modelo especializado offline/servidor.
    - Mantener un fallback local ligero para chequeos rápidos sin conexión.

- Ajustes y QA:
    - Permitir niveles de rigurosidad (ej. `estándar`, `estricto`, `experimental`) que ajusten umbrales de confianza.
    - Registrar métricas (precision/recall, falsos positivos/negativos) y permitir re-etiquetado para aprendizaje activo.

- Datos y privacidad:
    - Pedir consentimiento para almacenar imágenes; almacenar metadatos de forma segura para auditoría rabínica.

- Integraciones útiles:
    - Búsqueda por código de barras + coincidencia en bases (OpenFoodFacts) para validar ingredientes.
    - Pasarela para exportar casos a un sistema de certificación rabínica externo.

Formato JSON Estricto (actualizado):
{
    "resultado": "Kosher / No Kosher / Dudoso",
    "confianza_analisis": "0-100%",
    "sello_detectado": "Nombre de la agencia o 'Ninguno'",
    "categoria": "Parve / Dairy / Meat / DE",
    "caracteristicas_basicas": {"vegano": true/false, "sin_gluten": true/false, "sin_lacteos": true/false},
    "ingredientes_detectados": [{"nombre": "Ingrediente", "estatus": "Kosher/No Kosher/Dudoso/Precaución"}],
    "alertas": ["Lista de alertas"],
    "insect_scanner": {"detecciones": [{"bbox": [x,y,w,h], "descripcion": "", "especie_aproximada": "", "confianza": "0-100%", "severidad": "", "accion_recomendada": ""}], "resumen": "", "confianza_global": "0-100%", "nota_falsos_positivos": ""},
    "recomendaciones_funcionales": ["Lista corta de recomendaciones técnicas y de UX"],
    "explicacion_halajica": "Justificación técnica basada en el glosario"
}

Formato JSON Estricto:
{
  "resultado": "Kosher / No Kosher / Dudoso",
  "confianza_analisis": "0-100%",
  "sello_detectado": "Nombre de la agencia o 'Ninguno'",
  "categoria": "Parve / Dairy / Meat / DE",
  "caracteristicas_basicas": {"vegano": true/false, "sin_gluten": true/false, "sin_lacteos": true/false},
  "ingredientes_detectados": [{"nombre": "Ingrediente", "estatus": "Kosher/No Kosher/Dudoso/Precaución"}],
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

    def _try_generate_content(self, model, content_list, _unused_arg=None, max_retries=2):
        """
        Try to generate content with retry logic and exponential backoff.
        """
        print(f"[Engine] Starting content generation. Input items: {len(content_list)}")
        for attempt in range(max_retries):
            try:
                print(f"[Engine] Calling Gemini API (attempt {attempt + 1}/{max_retries})...")
                start_time = time.time()
                response = model.generate_content(content_list)
                print(f"[Engine] Gemini API call successful in {time.time() - start_time:.2f}s")
                return response
            except Exception as e:
                print(f"[Engine] Gemini call failed on attempt {attempt + 1}: {e}")
                # Exponential backoff
                if attempt < max_retries - 1:
                    sleep_time = 2 ** attempt
                    print(f"[Engine] Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                else:
                    print(f"[Engine] Exhausted all attempts.")
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
            print("[Engine] Attempting primary model (flash)...")
            response = self._try_generate_content(self.primary_model, content)
            return self._parse_response(response)
        except Exception as e:
            print(f"[Engine] Primary model exhausted: {e}")
            try:
                # Try fallback model
                print("[Engine] Attempting fallback model (pro)...")
                response = self._try_generate_content(self.fallback_model, content, max_retries=1)
                return self._parse_response(response)
            except Exception as e2:
                print(f"[Engine] Fallback model exhausted: {e2}")
                return {"error": f"Error en análisis de imágenes: {str(e2)}"}

    def _parse_response(self, response):
        try:
            # Limpiar la respuesta por si Gemini incluye tildes invertidas de markdown
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            parsed = json.loads(content)
            # Normalizar campo `insect_scanner` si existe
            try:
                parsed = self.normalize_insect_scanner(parsed)
            except Exception:
                # No fallar por normalización; devolver raw si algo va mal
                pass

            return parsed
        except Exception as e:
            return {
                "error": f"Error al parsear la respuesta: {str(e)}",
                "estado": "Error"
            }

    @staticmethod
    def normalize_insect_scanner(parsed_result: dict) -> dict:
        """
        Normaliza y valida la estructura `insect_scanner` dentro del resultado generado.
        - Asegura tipos: bbox como ints, confianza como int 0-100, severidad normalizada.
        - Rellena campos faltantes y valida acciones recomendadas.
        - No lanza excepciones en caso de entrada inesperada; devuelve el dict original o enriquecido.
        """
        if not isinstance(parsed_result, dict):
            return parsed_result

        isc = parsed_result.get('insect_scanner')
        if not isc or not isinstance(isc, dict):
            # Garantizar estructura mínima
            parsed_result['insect_scanner'] = {
                'detecciones': [],
                'resumen': '',
                'confianza_global': '0%',
                'nota_falsos_positivos': ''
            }
            return parsed_result

        detecciones = isc.get('detecciones', [])
        norm_detecciones = []
        for d in detecciones:
            try:
                bbox = d.get('bbox', [0, 0, 0, 0])
                # Convertir a ints y asegurar longitud 4
                bbox = [int(round(float(x))) for x in (bbox[:4] + [0, 0, 0, 0])[:4]]

                descripcion = d.get('descripcion', '') or ''
                especie = d.get('especie_aproximada', '') or 'desconocido'

                # Normalizar confianza
                conf_raw = d.get('confianza', 0)
                if isinstance(conf_raw, str):
                    conf_raw = conf_raw.replace('%', '').strip()
                try:
                    confianza = int(max(0, min(100, int(float(conf_raw)))))
                except Exception:
                    confianza = 0

                # Severidad mapping
                sev = (d.get('severidad') or '').lower()
                if sev in ['alta', 'high']:
                    severidad = 'Alta'
                elif sev in ['media', 'medium', 'med']:
                    severidad = 'Media'
                elif sev in ['baja', 'low']:
                    severidad = 'Baja'
                else:
                    # Inferir por confianza
                    if confianza >= 90:
                        severidad = 'Alta'
                    elif confianza >= 70:
                        severidad = 'Media'
                    else:
                        severidad = 'Baja'

                # Acción recomendada validación
                accion = (d.get('accion_recomendada') or '').strip()
                valid_actions = ['Desechar', 'Inspección humana', 'Conservar y revisar', 'Inspección humana especializada']
                if accion not in valid_actions:
                    # Inferir acción por severidad
                    if severidad == 'Alta':
                        accion = 'Desechar'
                    elif severidad == 'Media':
                        accion = 'Inspección humana especializada'
                    else:
                        accion = 'Conservar y revisar'

                norm_detecciones.append({
                    'bbox': bbox,
                    'descripcion': descripcion,
                    'especie_aproximada': especie,
                    'confianza': f"{confianza}%",
                    'severidad': severidad,
                    'accion_recomendada': accion
                })
            except Exception:
                # Omitir detección inválida
                continue

        # Confianza global: promedio de detecciones
        if norm_detecciones:
            total = 0
            for nd in norm_detecciones:
                total += int(str(nd.get('confianza', '0%')).replace('%', ''))
            confianza_global = int(total / len(norm_detecciones))
            isc['confianza_global'] = f"{confianza_global}%"
        else:
            isc['confianza_global'] = '0%'

        isc['detecciones'] = norm_detecciones
        parsed_result['insect_scanner'] = isc
        return parsed_result

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
          "caracteristicas_basicas": {"vegano": true/false, "sin_gluten": true/false, "sin_lacteos": true/false},
          "ingredientes_detectados": [{"nombre": "Ingrediente", "estatus": "Kosher/No Kosher/Dudoso/Precaución"}],
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

    def analyze_insects(self, images, extra_context=None, preferences=None):
        """
        Análisis específico para detectar insectos en frutas, verduras y cereales.
        Devuelve un JSON con la estructura extendida `insect_scanner` y descripciones detalladas.
        """
        prompt = (
            "Analiza estas imágenes enfocándote exclusivamente en detectar insectos, fragmentos, huevos o signos de infestación "
            "en frutas, verduras o cereales. Para cada hallazgo, proporciona: bbox, especie_aproximada (si es posible), "
            "etapa de vida (larva, adulto, huevo), una 'descripcion_detallada' (apariencia, tamaño estimado, color), "
            "nivel de confianza (0-100%), severidad (Alta/Media/Baja) y acción recomendada (Desechar/Inspección humana/Conservar y revisar)."
        )

        if extra_context:
            prompt += f"\n\nCONTEXTO ADICIONAL: {extra_context}"

        if preferences:
            prompt += f"\n\nPREFERENCIAS: {json.dumps(preferences, ensure_ascii=False)}"

        prompt += (
            "\n\nEntrega la respuesta en JSON con clave principal 'insect_scanner' tal como se define en la documentación del sistema. "
            "Si no hay insectos visibles, devuelve 'insect_scanner' con lista vacía y 'confianza_global': '0%'."
        )

        if not isinstance(images, list):
            images = [images]

        content = [prompt] + images

        try:
            response = self._try_generate_content(self.primary_model, content)
            return self._parse_response(response)
        except Exception as e:
            print(f"Error en analyze_insects (primario): {e}")
            try:
                response = self._try_generate_content(self.fallback_model, content)
                return self._parse_response(response)
            except Exception as e2:
                return {"error": f"Error en análisis de insectos: {str(e2)}"}

    def generate_color_heatmap(self, pil_image: Image.Image, preset: str = 'auto', sensitivity: int = 50) -> Image.Image:
        """
        Genera un heatmap basándose en color y zonas afectadas.
        - `preset`: 'auto', 'manzana', 'platano', 'cereal', 'custom'
        - `sensitivity`: 0-100 ajusta la agresividad del detector (mayor = más sensible)
        Devuelve una imagen PIL con el overlay del heatmap sobre la imagen original.
        """
        if not HAS_CV2:
            # Fallback: si no hay cv2, devolver imagen sin procesamiento
            return pil_image

        try:
            # Convert PIL to BGR numpy
            img_rgb = pil_image.convert('RGB')
            img = np.array(img_rgb)[:, :, ::-1].copy()  # RGB->BGR

            # Convert to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)

            # Preset-based thresholds (H in degrees scaled 0-179 in OpenCV)
            presets = {
                'auto': {'h_low': 35, 'h_high': 85, 's_th': 60, 'v_th': 110},
                'manzana': {'h_low': 25, 'h_high': 95, 's_th': 50, 'v_th': 110},
                'platano': {'h_low': 15, 'h_high': 40, 's_th': 40, 'v_th': 120},
                'cereal': {'h_low': 10, 'h_high': 40, 's_th': 40, 'v_th': 100},
            }

            cfg = presets.get(preset, presets['auto'])

            # Adjust thresholds by sensitivity: sensitivity 0 -> conservative, 100 -> aggressive
            # We'll linearly scale saturation and value thresholds
            s_th = max(10, int(cfg['s_th'] * (1 - (sensitivity - 50) / 200)))
            v_th = max(40, int(cfg['v_th'] * (1 - (sensitivity - 50) / 200)))
            h_low = int(cfg['h_low'] * (1 - (sensitivity - 50) / 300))
            h_high = int(cfg['h_high'] * (1 + (sensitivity - 50) / 300))

            lower_green = max(0, h_low)
            upper_green = min(179, h_high)

            mask_not_green = (h < lower_green) | (h > upper_green)
            mask_low_sat = s < s_th
            mask_dark = v < v_th

            damage_mask = (mask_not_green & (mask_low_sat | mask_dark)) | (mask_dark & (s < (s_th + 50)))

            # Convert boolean mask to uint8
            mask_u8 = (damage_mask.astype(np.uint8) * 255)

            # Smooth mask
            k = 21 if sensitivity >= 50 else 11
            mask_blur = cv2.GaussianBlur(mask_u8, (k, k), 0)

            # Normalize to 0-255
            norm = cv2.normalize(mask_blur, None, 0, 255, cv2.NORM_MINMAX)

            # Apply colormap
            heatmap = cv2.applyColorMap(norm, cv2.COLORMAP_JET)

            # Blend heatmap with original
            alpha = 0.6 + (sensitivity / 250)
            overlay = cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)

            # Convert back to PIL (RGB)
            overlay_rgb = overlay[:, :, ::-1]
            pil_overlay = Image.fromarray(overlay_rgb)
            return pil_overlay
        except Exception as e:
            print(f"Error generando heatmap: {e}")
            return pil_image
