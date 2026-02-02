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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    /* Primary Button - Gold/Premium */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    /* Cards */
    .status-box {
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
    }
    
    /* Status Colors */
    .kosher-parve { 
        background-color: rgba(232, 245, 233, 0.9); 
        border-left: 6px solid #2e7d32; 
        color: #1b5e20;
    }
    .kosher-dairy { 
        background-color: rgba(227, 242, 253, 0.9); 
        border-left: 6px solid #1565c0; 
        color: #0d47a1;
    }
    .kosher-meat { 
        background-color: rgba(255, 235, 238, 0.9); 
        border-left: 6px solid #c62828; 
        color: #b71c1c;
    }
    .no-kosher { 
        background-color: rgba(250, 250, 250, 0.9); 
        border-left: 6px solid #424242; 
        color: #212121;
    }
    .dudoso { 
        background-color: rgba(255, 253, 231, 0.9); 
        border-left: 6px solid #fbc02d; 
        color: #f57f17;
    }

    /* Headers */
    h1, h2, h3 {
        color: #1a237e;
    }
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


# Tabs for navigation
tab1, tab2 = st.tabs(["📸 Escáner", "⭐ Recomendados"])

with tab1:
    col_mode1, col_mode2 = st.columns([2, 1])
    with col_mode1:
        st.subheader("🔍 Analizar Producto")
    with col_mode2:
        mode = st.radio("Modo", ["📷 Foto", "📝 Texto"], horizontal=True, label_visibility="collapsed")

    result = None

    if mode == "📷 Foto":
        uploaded_file = st.file_uploader("Elige una imagen del producto...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Imagen subida', use_container_width=True)
            
            # Get image bytes for caching
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format if image.format else 'PNG')
            img_bytes = img_byte_arr.getvalue()

            if st.button("Analizar Imagen"):
                with st.spinner('Analizando imagen...'):
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

    else: # Mode Text
        st.info("📝 Ingresa la lista de ingredientes o descripción del producto si la foto no es clara.")
        text_input = st.text_area("Ingredientes / Detalles", height=150, placeholder="Ejemplo: Lay's Clásicas. Ingredientes: Papas, aceite vegetal, sal.")
        
        if st.button("Analizar Texto"):
            if text_input:
                with st.spinner('Analizando texto...'):
                    if 'engine' in st.session_state:
                         result = st.session_state.engine.analyze_text(text_input)
                    else:
                        st.error("Engine no inicializado.")
            else:
                st.warning("⚠️ Por favor ingresa texto para analizar.")

    # Results Display (Shared)
    if result:
        if "error" in result:
            st.error(f"❌ {result['error']}")
            if "detalles" in result:
                with st.expander("Ver detalles técnicos"):
                    st.code(result["detalles"])
            
            if "cuota" in result["error"].lower() or "quota" in result["error"].lower():
                st.info("💡 **Sugerencia:** Tu plan gratuito de Gemini puede haberse agotado. Intenta de nuevo en unos minutos.")
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
                    <h2 style="text-align: center; margin-bottom: 5px;">{estado}</h2>
                    <p style="text-align: center; font-size: 1.1em; opacity: 0.8;">{result.get('producto', 'Producto Detectado')}</p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🏷️ Hechshers")
                symbols = result.get("símbolos_encontrados", [])
                if symbols:
                    for s in symbols:
                        st.success(f"✅ {s}")
                else:
                    st.info("No se detectaron símbolos.")

            with col2:
                st.markdown("### 🔍 Alertas")
                alerts = result.get("ingredientes_alerta", [])
                if alerts:
                    for a in alerts:
                        st.error(f"⚠️ {a}")
                else:
                    st.success("✅ Sin ingredientes sospechosos.")

            st.markdown("---")
            st.markdown(f"**💡 Dictamen:** {result.get('justificación', 'Sin justificación')}")
            
            if result.get("advertencia"):
                st.warning(f"⚠️ **Nota:** {result.get('advertencia')}")

with tab2:
    st.subheader("⭐ Productos Recomendados")
    st.info("Esta sección está en construcción. Aquí encontrarás productos verificados popularmente.")
    
    st.markdown("### 🥤 Bebidas")
    st.write("- Coca-Cola (Regular, Zero, Diet) - OUP")
    st.write("- Pepsi (Regular, Black) - OK")
    
    st.markdown("### 🍫 Snacks")
    st.write("- Lays Clásicas - OU")
    st.write("- Pringles Original - OU")

st.sidebar.markdown("---")
st.sidebar.write("### Instrucciones")
st.sidebar.info("Asegúrate de que la foto sea clara y se vean tanto los logos de certificación como la lista de ingredientes.")
st.sidebar.warning("Esta herramienta es un apoyo informativo. Consulta siempre con tu Rabino local.")
