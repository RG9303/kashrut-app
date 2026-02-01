import streamlit as st
from PIL import Image
import io
import sys
import os

# Add parent directory to path to import engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.kashrut_engine import KashrutEngine
from engine.cache_manager import CacheManager

st.set_page_config(
    page_title="Digital Mashgiach - Kashrut Checker",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS for premium feel
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
    }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .kosher-parve { background-color: #e8f5e9; border: 2px solid #2e7d32; }
    .kosher-dairy { background-color: #e3f2fd; border: 2px solid #1976d2; }
    .kosher-meat { background-color: #ffebee; border: 2px solid #c62828; }
    .no-kosher { background-color: #fafafa; border: 2px solid #616161; }
    .dudoso { background-color: #fffde7; border: 2px solid #fbc02d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Digital Mashgiach")
st.subheader("Identificación Inteligente de Kashrut")

st.markdown("""
Escanea o sube una foto de un producto para analizar sus **Hechshers** e **Ingredientes**.
""")

# Initialize components
if 'engine' not in st.session_state:
    try:
        st.session_state.engine = KashrutEngine()
    except Exception as e:
        st.error(f"Error de configuración: {e}")
        st.info("Asegúrate de tener la variable GOOGLE_API_KEY en tu archivo .env")

cache = CacheManager()

uploaded_file = st.file_uploader("Elige una imagen del producto...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen subida', use_container_width=True)
    
    # Get image bytes for caching
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format if image.format else 'PNG')
    img_bytes = img_byte_arr.getvalue()

    if st.button("Analizar Producto"):
        with st.spinner('Analizando con IA...'):
            # Check cache first
            result = cache.get_cached_result(img_bytes)
            
            if result:
                st.info("⚡ Respuesta instantánea (desde caché)")
            else:
                if 'engine' in st.session_state:
                    result = st.session_state.engine.analyze_product(image)
                    cache.save_to_cache(img_bytes, result)
                else:
                    st.error("Engine no inicializado.")
                    result = None

            if result:
                if "error" in result:
                    # Display error with more context
                    st.error(f"❌ {result['error']}")
                    
                    # If there are additional details, show them in an expander
                    if "detalles" in result:
                        with st.expander("Ver detalles técnicos"):
                            st.code(result["detalles"])
                    
                    # Provide helpful suggestions
                    if "cuota" in result["error"].lower() or "quota" in result["error"].lower():
                        st.info("""
                        💡 **Sugerencias:**
                        - Espera unos minutos e intenta de nuevo
                        - Verifica tu plan de API en [Google AI Studio](https://aistudio.google.com/app/apikey)
                        - Considera actualizar a un plan de pago si usas la app frecuentemente
                        """)
                else:
                    # Display results in a nice UI
                    estado = result.get("estado", "Dudoso")
                    css_class = ""
                    if "PARVE" in estado.upper(): css_class = "kosher-parve"
                    elif "DAIRY" in estado.upper() or "LÁCTEO" in estado.upper(): css_class = "kosher-dairy"
                    elif "MEAT" in estado.upper() or "CARNE" in estado.upper(): css_class = "kosher-meat"
                    elif "NO KOSHER" in estado.upper(): css_class = "no-kosher"
                    else: css_class = "dudoso"

                    st.markdown(f"""
                        <div class="status-box {css_class}">
                            <h2 style="text-align: center;">{estado}</h2>
                            <p><strong>Producto:</strong> {result.get('producto', 'N/A')}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("### 🏷️ Hechshers")
                        symbols = result.get("símbolos_encontrados", [])
                        if symbols:
                            for s in symbols:
                                st.success(s)
                        else:
                            st.write("No se detectaron símbolos claros.")

                    with col2:
                        st.write("### 🔍 Alertas")
                        alerts = result.get("ingredientes_alerta", [])
                        if alerts:
                            for a in alerts:
                                st.warning(a)
                        else:
                            st.write("Sin alertas de ingredientes.")

                    st.info(f"**Justificación:** {result.get('justificación', 'N/A')}")
                    
                    if result.get("advertencia"):
                        st.warning(f"⚠️ {result.get('advertencia')}")

st.sidebar.markdown("---")
st.sidebar.write("### Instrucciones")
st.sidebar.info("Asegúrate de que la foto sea clara y se vean tanto los logos de certificación como la lista de ingredientes.")
st.sidebar.warning("Esta herramienta es un apoyo informativo. Consulta siempre con tu Rabino local.")
