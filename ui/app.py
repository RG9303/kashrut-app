import streamlit as st
from PIL import Image
import io
import sys
import os

# Add parent directory to path to import engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.kashrut_engine import KashrutEngine
from engine.cache_manager import CacheManager
from engine.agency_registry import check_agency
from engine.history_manager import HistoryManager
from engine.off_client import OpenFoodFactsClient

st.set_page_config(
    page_title="Digital Mashgiach - Kashrut Checker",
    page_icon="🛡️",
    layout="centered"
)

# Initialize components in session state
if 'engine' not in st.session_state:
    try:
        st.session_state.engine = KashrutEngine()
    except Exception as e:
        st.error(f"Error de configuración: {e}")

if 'history' not in st.session_state:
    st.session_state.history = HistoryManager()

if 'off_client' not in st.session_state:
    st.session_state.off_client = OpenFoodFactsClient()

if 'preferences' not in st.session_state:
    st.session_state.preferences = {
        "jalav_stam": "Permitido",
        "pesaj_tradicion": "Sefaradí (Kitniyot OK)",
        "rigor": "Regular"
    }

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

    .result-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #eee;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .status-banner {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📸 Escáner", "⭐ Recomendados", "📜 Mi Alacena", "📚 Glosario", "👤 Perfil"])

with tab1:
    col_mode1, col_mode2 = st.columns([2, 1])
    with col_mode1:
        st.subheader("🔍 Analizar Producto")
    with col_mode2:
        mode = st.radio("Modo", ["📷 Foto", "📝 Texto"], horizontal=True, label_visibility="collapsed")

    result = None

    if mode == "📷 Foto":
        uploaded_files = st.file_uploader("Sube fotos (Frente y Reverso recomendado)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if uploaded_files:
            images = []
            # Display images in a grid
            cols = st.columns(min(len(uploaded_files), 3))
            
            img_bytes_list = []

            for i, uploaded_file in enumerate(uploaded_files):
                image = Image.open(uploaded_file)
                images.append(image)
                
                # Display in column (wrap around if more than 3)
                col_idx = i % 3
                with cols[col_idx]:
                    st.image(image, caption=f'Imagen {i+1}', use_container_width=True)
                
                # Bytes for cache key
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format if image.format else 'PNG')
                img_bytes_list.append(img_byte_arr.getvalue())

            # Create a combined cache key from all images
            combined_bytes = b"".join(img_bytes_list)

            if st.button("Analizar Imágenes"):
                with st.spinner('Analizando con IA (Deep Analysis)...'):
                    # Check cache first
                    result = cache.get_cached_result(combined_bytes)
                    
                    if result:
                        st.info("⚡ Respuesta instantánea (desde caché)")
                    else:
                        if 'engine' in st.session_state:
                            # 1. Intentar extraer Código de Barras
                            barcode = st.session_state.engine.extract_barcode(images[0])
                            off_data = None
                            if barcode:
                                with st.status(f"Barcode detectado: {barcode}. Consultando base de datos mundial..."):
                                    off_data = st.session_state.off_client.get_product(barcode)
                                    if off_data:
                                        st.success(f"Producto encontrado: {off_data['product_name']}")
                            
                            # 2. Análisis Final
                            extra_context = off_data.get('ingredients_text') if off_data else None
                            result = st.session_state.engine.analyze_product(
                                images, 
                                extra_context=extra_context,
                                preferences=st.session_state.preferences
                            )
                            
                            # 3. Guardar en Historial
                            if result and "error" not in result:
                                st.session_state.history.add_scan(result)
                            
                            cache.save_to_cache(combined_bytes, result)
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
                         result = st.session_state.engine.analyze_text(
                             text_input,
                             preferences=st.session_state.preferences
                         )
                         if result and "error" not in result:
                             st.session_state.history.add_scan(result)
                    else:
                        st.error("Engine no inicializado.")
            else:
                st.warning("⚠️ Por favor ingresa texto para analizar.")

            # Results Display (Shared)
    # --- DISPLAY RESULTS (SHARED) ---
    if result:
        st.markdown("<br>", unsafe_allow_html=True)
        
        if "error" in result:
            st.error(f"❌ {result['error']}")
            if "cuota" in result.get('error', '').lower():
                st.info("💡 Sugerencia: Intenta de nuevo en unos segundos.")
        else:
            # 1. Status Banner
            estado = result.get("resultado", "Dudoso")
            confianza = result.get("confianza_analisis", "N/A")
            categoria = result.get("categoria", "Desconocido")
            sello = result.get("sello_detectado", "Ninguno")

            banner_color = "#777"
            if "KOSHER" in estado.upper() and "NO" not in estado.upper(): banner_color = "#d4af37" # Gold
            elif "NO KOSHER" in estado.upper(): banner_color = "#c62828" # Red
            elif "DUDOSO" in estado.upper(): banner_color = "#ffa000" # Orange

            st.markdown(f"""
                <div class="status-banner" style="background: {banner_color};">
                    <h1 style="margin:0; font-size: 3rem; font-weight: 700;">{estado.upper()}</h1>
                    <p style="margin:10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">Confianza: {confianza}</p>
                </div>
            """, unsafe_allow_html=True)
            # 2. Key Metrics
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                with st.container(border=True):
                    st.markdown("### 🛡️ Certificación")
                    st.write(f"**Detectado:** {sello}")
                    # Agency Check
                    agency_data = check_agency(sello)
                    if agency_data:
                        st.markdown(f"""
                            <a href="{agency_data['website']}" target="_blank" style="text-decoration: none;">
                                <div style="background-color: #f1f8e9; padding: 10px; border-radius: 8px; border: 1px solid #c5e1a5; margin-top: 5px; display: flex; align-items: center;">
                                    <span style="font-size: 1.5em; margin-right: 10px;">{agency_data['icon']}</span>
                                    <div>
                                        <div style="font-weight: bold; color: #33691e;">{agency_data['full_name']}</div>
                                        <div style="font-size: 0.85em; color: #558b2f;">Válido e Internacional ↗</div>
                                    </div>
                                </div>
                            </a>
                        """, unsafe_allow_html=True)
                    elif "K GENÉRICA" in sello.upper():
                         st.error("⚠️ Sello 'K' Genérico (No Confiable)")
                    elif sello and sello.lower() != "ninguno":
                        st.warning(f"⚠️ Agencia '{sello}' no verificada.")
                    else:
                        st.info("No se detectó sello de certificación.")

            with col_res2:
                with st.container(border=True):
                    st.markdown("### 🏷️ Categoría")
                    cat_icons = {"Parve": "🍃", "Dairy": "🥛", "Meat": "🍖", "DE": "⚙️", "Lácteo": "🥛", "Carne": "🍖"}
                    icon = cat_icons.get(categoria, "❓")
                    st.markdown(f"## {icon} {categoria}")

            # 3. Alertas
            alertas = result.get('alertas', [])
            if alertas and alertas[0].lower() != "ninguno":
                with st.container(border=True):
                    st.markdown("### ⚠️ Alertas Halájicas")
                    for alerta in alertas:
                        st.warning(alerta)

            # 4. Explicación Detallada (Card)
            st.markdown(f"""
                <div class="result-card">
                    <h3 style="margin-top:0;">📖 ¿Por qué este resultado?</h3>
                    <p style="font-size: 1.1rem; line-height:1.5;">{result.get('explicacion_halajica', 'No hay explicación disponible.')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Nuevo Análisis"):
                st.rerun()

with tab2:
    st.subheader("⭐ Productos Recomendados")
    st.info("Esta sección está en construcción. Aquí encontrarás productos verificados popularmente.")
    
    st.markdown("### 🥤 Bebidas")
    st.write("- Coca-Cola (Regular, Zero, Diet) - OUP")
    st.write("- Pepsi (Regular, Black) - OK")
    
    st.markdown("### 🍫 Snacks")
    st.write("- Lays Clásicas - OU")
    st.write("- Pringles Original - OU")

with tab3:
    st.subheader("📜 Mi Alacena")
    st.markdown("Revisa tus escaneos guardados.")
    
    history_data = st.session_state.history.get_history()
    
    if not history_data:
        st.info("Aún no tienes productos en tu alacena. ¡Empieza a escanear!")
    else:
        for item in history_data:
            with st.expander(f"{item['timestamp']} - {item['product_name']} ({item['status']})"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Estatus", item['status'])
                with col2:
                    st.write(f"**Categoría:** {item['category']}")
                    st.write(f"**Explicación:** {item['details'].get('explicacion_halajica', 'N/A')}")
                
                if st.button("Eliminar", key=f"del_{item['id']}"):
                    st.session_state.history.delete_scan(item['id'])
                    st.rerun()

    if st.button("Vaciar Alacena"):
        st.session_state.history.clear_history()
        st.rerun()

with tab4:
    st.subheader("📚 Glosario de Kashrut")
    st.markdown("Consulta términos técnicos para entender mejor los resultados.")
    
    glossary_terms = {
        "Kosher": "Apto para el consumo según la ley dietética judía (Halajá).",
        "Parve": "Alimento neutro que no contiene carne ni leche.",
        "DE (Dairy Equipment)": "Producto Parve procesado en equipo lácteo. Se puede comer después de carne (según la mayoría de opiniones) pero no con ella.",
        "Jalav Stam": "Leche cuya producción no fue supervisada constantemente por un judío.",
        "Jalav Yisrael": "Leche supervisada por un judío desde el ordeño.",
        "Bishul Israel": "Alimentos cocinados con la participación de un judío.",
        "Pat Israel": "Pan horneado con la participación de un judío.",
        "Mevushal": "Vino o jugo de uva que ha sido cocinado (hervido).",
        "Kitniyot": "Legumbres (arroz, maíz, etc.) prohibidas en Pésaj para Ashkenazim.",
        "Glatt": "Nivel estricto de supervisión para la carne.",
        "Jametz": "Leudado prohibido en Pésaj (trigo, cebada, etc.)."
    }

    search = st.text_input("Buscar término...", "").lower()
    for term, definition in glossary_terms.items():
        if search in term.lower() or search in definition.lower():
            st.markdown(f"**{term}**: {definition}")

with tab5:
    st.subheader("👤 Tu Perfil de Kashrut")
    st.markdown("Personaliza cómo la IA analiza tus productos.")
    
    with st.container(border=True):
        st.session_state.preferences["jalav_stam"] = st.radio(
            "¿Consumes Jalav Stam?",
            ["Permitido", "Estricto (Solo Jalav Yisrael)"],
            index=0 if st.session_state.preferences["jalav_stam"] == "Permitido" else 1
        )
        
        st.session_state.preferences["pesaj_tradicion"] = st.selectbox(
            "Tradición de Pésaj",
            ["Sefaradí (Kitniyot OK)", "Ashkenazí (No Kitniyot)"],
            index=0 if st.session_state.preferences["pesaj_tradicion"] == "Sefaradí (Kitniyot OK)" else 1
        )
        
        st.session_state.preferences["rigor"] = st.select_slider(
            "Nivel de Rigor General",
            options=["Regular", "Medio", "Estricto"],
            value=st.session_state.preferences["rigor"]
        )
        
        if st.button("Guardar Preferencias"):
            st.success("¡Preferencias actualizadas!")

st.sidebar.markdown("---")
st.sidebar.write("### Instrucciones")
st.sidebar.info("Asegúrate de que la foto sea clara y se vean tanto los logos de certificación como la lista de ingredientes.")
st.sidebar.warning("Esta herramienta es un apoyo informativo. Consulta siempre con tu Rabino local.")
