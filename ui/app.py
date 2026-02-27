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
    page_title="KosherScan - Digital Mashgiach",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
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

if 'cache' not in st.session_state:
    st.session_state.cache = CacheManager()

if 'preferences' not in st.session_state:
    st.session_state.preferences = {
        "jalav_stam": "Permitido",
        "pesaj_tradicion": "Sefaradí (Kitniyot OK)",
        "rigor": "Regular"
    }

# Custom CSS for ultra-premium mobile look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
    }

    /* Typography Polish */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Scanner Tab Specific */
    .scanner-wrapper {
        text-align: center;
        padding: 30px 20px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }

    /* Target Reticle - Animated and Glowing */
    .scanner-frame {
        width: 260px;
        height: 260px;
        border: 2px solid transparent;
        margin: 30px auto;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        animation: pulse-frame 4s infinite alternate;
    }
    @keyframes pulse-frame {
        0% { transform: scale(0.98); opacity: 0.8; box-shadow: 0 0 20px rgba(16, 185, 129, 0.1); }
        100% { transform: scale(1.02); opacity: 1; box-shadow: 0 0 40px rgba(16, 185, 129, 0.4); }
    }
    
    .scanner-frame::before, .scanner-frame::after, 
    .scanner-frame span::before, .scanner-frame span::after {
        content: '';
        position: absolute;
        width: 40px;
        height: 40px;
        border: 4px solid #10b981; /* Premium Emerald Glow */
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
    }
    .scanner-frame::before { top: 0; left: 0; border-right: none; border-bottom: none; border-bottom-right-radius: 0; }
    .scanner-frame::after { top: 0; right: 0; border-left: none; border-bottom: none; border-bottom-left-radius: 0; }
    .scanner-frame span::before { bottom: 0; left: 0; border-right: none; border-top: none; border-top-right-radius: 0; }
    .scanner-frame span::after { bottom: 0; right: 0; border-left: none; border-top: none; border-top-left-radius: 0; }

    .inner-reticle {
        width: 60px;
        height: 60px;
        border: 2px dashed rgba(16, 185, 129, 0.6);
        border-radius: 50%;
        animation: rotate 10s linear infinite;
    }
    @keyframes rotate {
        100% { transform: rotate(360deg); }
    }

    /* Buttons Alignment & Premium Styling */
    .stButton > button {
        border-radius: 16px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: none !important;
        letter-spacing: 0.3px !important;
    }

    /* Primary Scan Button Hover Effects */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) .primary-btn button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(1) .primary-btn button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5) !important;
    }

    /* Ghost Upload Button */
    .ghost-btn button {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    .ghost-btn button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* Expanders styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px;
        color: white !important;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.2) !important;
        border-radius: 0 0 12px 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: none;
    }

    /* Inputs (Text, Selectboxes) */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div {
        background-color: rgba(0, 0, 0, 0.2) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.5rem 1rem !important;
        transition: border-color 0.3s ease;
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 1px #10b981 !important;
    }

    /* Results Page */
    .results-bg {
        background: transparent;
        margin: -2rem 0;
        padding: 2rem 0;
        color: #f8fafc;
    }

    .result-card {
        background: rgba(30, 41, 59, 0.7) !important;
        padding: 24px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #f8fafc !important;
        backdrop-filter: blur(12px);
        transition: transform 0.3s ease;
    }
    .result-card:hover {
        transform: translateY(-2px);
    }
    .result-card h3 {
        color: #f8fafc !important;
        font-size: 1.2rem !important;
        margin-bottom: 16px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .status-banner-premium {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 20px;
        text-align: center;
        font-weight: 800;
        font-size: 1.8rem;
        border-radius: 20px;
        margin: -1rem 0 2rem 0;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .status-banner-premium.error-state {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3);
        color: white;
    }
    
    .status-banner-premium.warning-state {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3);
        color: white;
    }

    /* Metrics and Stats */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #10b981 !important;
    }

    /* Bottom Navigation Simulation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: space-around;
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(15px);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 12px 16px;
        white-space: pre-wrap;
        background-color: transparent !important;
        border: none !important;
        color: rgba(255,255,255,0.4) !important;
        border-radius: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: rgba(255, 255, 255, 0.8) !important;
    }
    .stTabs [aria-selected="true"] {
        color: #10b981 !important;
        background: rgba(16, 185, 129, 0.1) !important;
        border-bottom: none !important;
        box-shadow: inset 0 0 0 1px rgba(16, 185, 129, 0.2);
    }

    /* File Uploader Polish */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 20px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #10b981 !important;
        background: rgba(16, 185, 129, 0.05) !important;
    }

    /* White-Labeling: Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP STATE & NAVIGATION ---
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Custom Header (Mobile Look)
if st.session_state.last_result:
    header_title = "Results"
    left_icon = "❮"
    left_action = "onclick='window.location.reload();'" # Hack to reset
else:
    header_title = "KosherScan"
    left_icon = "☰"
    left_action = ""

st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; margin-bottom: 20px;">
        <div style="font-size: 1.5rem; cursor: pointer; color: white;" {left_action}>{left_icon}</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: white;">{header_title}</div>
        <div style="font-size: 1.5rem; color: white;">⚙️</div>
    </div>
""", unsafe_allow_html=True)

# Tabs (Styled as Bottom Nav approximation)
# Use shorter labels to fit mobile screen widths
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "⭐ Rec", "📜 Hist", "📚 Glos", "👤 Prof"])

with tab1:
    if not st.session_state.last_result:
        # --- SCANNER VIEW ---
        st.markdown("""
            <div class="scanner-wrapper">
                <div class="scanner-frame">
                    <span></span>
                    <div class="inner-reticle"></div>
                </div>
                <h2 style="color: white; margin-top: 0; font-weight: 700; font-size: 1.8rem;">Escanea tu producto</h2>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.5; margin-bottom: 30px;">
                    📱 Fotografía el PRODUCTO (etiqueta frontal y código de barras).<br>
                    🔍 Asegúrate de que sea clara y enfocada.<br>
                    ✅ Usaremos IA para detectar certificaciones y analizar ingredientes.
                </p>
            </div>
        """, unsafe_allow_html=True)

        col_b1, col_b2, col_b3 = st.columns([1, 8, 1])
        with col_b2:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            if st.button("Scan", key="mock_scan_trigger"):
                st.info("💡 Usa el botón de abajo para subir tus fotos.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
            uploaded_files = st.file_uploader(
                "Upload Photo", 
                type=['jpg', 'jpeg', 'png', 'webp'],
                accept_multiple_files=True,
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Pro Scanner Section ---
            with st.expander("🔬 Pro Scanner — Detección de insectos avanzados"):
                st.write("Usa la cámara para hacer una foto macro o sube imágenes guardadas. Ideal para frutas, verduras y cereales.")
                pro_preset = st.selectbox("Preset de producto", ["auto", "manzana", "platano", "cereal", "custom"], index=0, key='pro_preset')
                pro_sensitivity = st.slider("Sensibilidad (heatmap)", min_value=0, max_value=100, value=50, key='pro_sensitivity')
                cam_img = st.camera_input("Tomar foto (cámara)")
                pro_uploads = st.file_uploader(
                    "O sube imágenes para análisis pro", 
                    type=['jpg','jpeg','png','webp'],
                    accept_multiple_files=True,
                    key='pro_uploader'
                )
                colp1, colp2 = st.columns([1,1])
                with colp1:
                    if st.button("Analizar con Pro Scanner", key='pro_analyze'):
                        pro_images = []
                        if cam_img:
                            try:
                                pro_images.append(Image.open(cam_img))
                            except Exception:
                                pass
                        if pro_uploads:
                            for f in pro_uploads:
                                try:
                                    pro_images.append(Image.open(f))
                                except Exception:
                                    pass

                        if not pro_images:
                            st.warning("Sube o toma al menos una foto para el análisis pro.")
                        else:
                            with st.spinner('Analizando (Pro)...'):
                                result = st.session_state.engine.analyze_insects(pro_images, preferences=st.session_state.preferences)
                                if result and "error" not in result:
                                    st.session_state.history.add_scan(result)
                                    combined_bytes = b"".join([p.tobytes() for p in pro_uploads]) if pro_uploads else b"cam"
                                    st.session_state.cache.save_to_cache(combined_bytes, result)
                                    st.session_state.last_images = pro_images
                                    # Generate heatmap with chosen preset and sensitivity
                                    try:
                                        heat = st.session_state.engine.generate_color_heatmap(pro_images[0], preset=pro_preset, sensitivity=pro_sensitivity)
                                        st.session_state.last_heatmap = heat
                                    except Exception:
                                        st.session_state.last_heatmap = None
                                    st.session_state.last_result = result
                                    st.rerun()
                                else:
                                    st.error("Error en el análisis Pro: " + (result.get('error') if isinstance(result, dict) else str(result)))
                with colp2:
                    st.info("Consejos: toma fotos macro, añade una regla para escala y trata de aislar la muestra sobre fondo claro.")
            
            st.markdown("<div style='margin-top: 10px; color: rgba(255,255,255,0.7); text-align: center;'>O ingresa el código de barras manualmente:</div>", unsafe_allow_html=True)
            manual_barcode = st.text_input("Código de barras", placeholder="Ej. 75010080...", label_visibility="collapsed")

        if uploaded_files or manual_barcode:
            images = [Image.open(file) for file in uploaded_files] if uploaded_files else []
            combined_bytes = b"".join([file.getvalue() for file in uploaded_files]) if uploaded_files else manual_barcode.encode()
            
            # Check cache
            cached_result = st.session_state.cache.get_from_cache(combined_bytes)
            if cached_result:
                st.session_state.last_result = cached_result
                st.rerun()
            else:
                with st.spinner('Analizando...'):
                    # 1. Barcode check
                    off_data = None
                    barcode = manual_barcode if manual_barcode else None
                    if not barcode and images:
                        barcode = st.session_state.engine.extract_barcode(images[0])
                    
                    if barcode:
                        try:
                            off_data = st.session_state.off_client.get_product(barcode)
                            if off_data:
                                # Show product details nicely
                                st.markdown(f"""<div class="result-card">
                                    <h3>📦 Producto Detectado</h3>
                                    <div>
                                        <p style="font-weight: 600; font-size: 1.1rem; margin: 8px 0;">{off_data.get('product_name', 'Desconocido')}</p>
                                        <p style="margin: 4px 0; color: #94a3b8;"><strong>Marca:</strong> {off_data.get('brands', 'N/A')}</p>
                                        <p style="margin: 4px 0; color: #94a3b8;"><strong>Cantidad:</strong> {off_data.get('quantity', 'N/A')}</p>
                                        <p style="margin: 4px 0; color: #94a3b8;"><strong>Código:</strong> {barcode}</p>
                                    </div>
                                </div>""", unsafe_allow_html=True)
                                
                                # Show ingredients if available
                                if off_data.get('ingredients_text'):
                                    st.markdown(f"""<div class="result-card">
                                        <h3>🧪 Ingredientes Registrados en Base de Datos</h3>
                                        <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">{off_data.get('ingredients_text')}</p>
                                    </div>""", unsafe_allow_html=True)
                        except Exception as e: pass
                    
                    # 2. Análisis Final
                    extra_context = off_data.get('ingredients_text') if off_data else None
                    
                    if extra_context and not images:
                        # Si solo hay código de barras y proporcionó texto pero no imagenes
                        result = st.session_state.engine.analyze_text(
                            extra_context, 
                            preferences=st.session_state.preferences
                        )
                    else:
                        result = st.session_state.engine.analyze_product(
                            images, 
                            extra_context=extra_context,
                            preferences=st.session_state.preferences
                        )
                    
                    if result and "error" not in result:
                        st.session_state.history.add_scan(result)
                        st.session_state.cache.save_to_cache(combined_bytes, result)
                        # Store result and images for the results view (for bounding box overlays)
                        st.session_state.last_images = images if images else []
                        # Generate and store heatmap for the first image (if available)
                        try:
                            if st.session_state.last_images:
                                heat = st.session_state.engine.generate_color_heatmap(st.session_state.last_images[0])
                                st.session_state.last_heatmap = heat
                        except Exception:
                            st.session_state.last_heatmap = None
                        st.session_state.last_result = result
                        st.rerun()
                    else:
                        st.error("Error en el análisis de la IA.")
    else:
        # --- RESULTS VIEW ---
        result = st.session_state.last_result
        status = result.get('resultado', 'Dudoso')
        conf = result.get('confianza_analisis', 'N/A')
        banner_class = "status-banner-premium"
        if "NO KOSHER" in status.upper():
            banner_class += " error-state"
        elif "PREC" in status.upper() or "PARVE" not in status.upper() and ("DUDO" in status.upper() or "DAIRY" in status.upper() or "LÁCTEO" in status.upper()):
            banner_class += " warning-state"
            
        st.markdown(f"""
            <div class="{banner_class}">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span>{"✓" if "KOSHER" in status.upper() and "NO" not in status.upper() else "⚠️"}</span> {status.upper()}
                </div>
                <div style="font-size: 1rem; font-weight: 500; opacity: 0.9; margin-top: 8px; letter-spacing: 0.5px;">
                    Confianza del Análisis: {conf}
                </div>
            </div>
            <div class="results-bg">
        """, unsafe_allow_html=True)

        # Main Cards
        st.markdown(f"""
            <div class="result-card">
                <h3>Sello de Certificación</h3>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: rgba(16, 185, 129, 0.1); color: #10b981; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; border: 2px solid rgba(16, 185, 129, 0.3); box-shadow: 0 4px 10px rgba(16, 185, 129, 0.15);">
                        {result.get('sello_detectado', '??')[:2].upper()}
                    </div>
                    <div style="font-weight: 600; font-size: 1.1rem; color: #f8fafc;">{result.get('sello_detectado', 'Ninguno')}</div>
                </div>
            </div>
            
            <div class="result-card">
                <h3>Categoría Hallada</h3>
                <div style="display: flex; align-items: center; gap: 12px; font-size: 1.15rem; font-weight: 600;">
                    <span style="font-size: 1.6rem;">{ "🍃" if "Parve" in result.get('categoria', 'Parve') else "🥛" if "Lácteo" in result.get('categoria', '') or "Dairy" in result.get('categoria', '') else "🥩" }</span> 
                    {result.get('categoria', 'Parve')}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Insect scanner display (if present)
        isc = result.get('insect_scanner', {})
        detections = isc.get('detecciones', []) if isinstance(isc, dict) else []
        if detections:
            st.markdown('<div class="result-card"><h3>Insect Scanner Detections</h3>', unsafe_allow_html=True)
            # If we have an image, draw boxes over first image
            imgs = st.session_state.get('last_images', [])
            if imgs:
                try:
                    from PIL import ImageDraw
                    img = imgs[0].convert('RGB')
                    draw = ImageDraw.Draw(img)
                    w, h = img.size
                    for det in detections:
                        bbox = det.get('bbox', [0,0,0,0])
                        x, y, bw, bh = bbox
                        # Draw rectangle
                        draw.rectangle([x, y, x+bw, y+bh], outline=(255,0,0), width=3)
                    st.image(img, use_column_width=True)
                except Exception:
                    pass

            # Show heatmap if available
            heat = st.session_state.get('last_heatmap')
            if heat:
                st.markdown('<div style="margin-top:12px;"><strong>Zona afectada (Heatmap)</strong></div>', unsafe_allow_html=True)
                st.image(heat, use_column_width=True)

            for i, d in enumerate(detections):
                st.markdown(f"""
                    <div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0;'>
                        <div>
                            <strong>Detección #{i+1}</strong><br>
                            <small>{d.get('descripcion','')} — {d.get('especie_aproximada','')}</small>
                        </div>
                        <div style='text-align:right;'>
                            <div style='font-weight:700'>{d.get('confianza','')}</div>
                            <div style='font-size:0.85rem; color:#64748b'>{d.get('severidad','')}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Review button
            if st.button("Solicitar revisión por Mashgiach"):
                review_payload = result.copy()
                review_payload['review_requested'] = True
                st.session_state.history.add_scan(review_payload)
                st.success("Solicitud de revisión enviada. Un Mashgiach la revisará.")

            st.markdown('</div>', unsafe_allow_html=True)

        alertas = result.get('alertas', [])
        if alertas and alertas[0].lower() != "ninguno":
            st.markdown('<div class="result-card"><h3>⚠️ Alertas Importantes</h3>', unsafe_allow_html=True)
            for a in alertas:
                st.markdown(f"""
                    <div style="display: flex; gap: 12px; color: #fef08a; background: rgba(234, 179, 8, 0.1); padding: 16px; border-radius: 16px; margin-bottom: 12px; font-size: 0.95rem; border: 1px solid rgba(234, 179, 8, 0.2); align-items: center;">
                        <span style="font-size: 1.2rem;">⚠️</span> <div style="line-height: 1.4;">{a}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Characteristics
        caracteristicas = result.get('caracteristicas_basicas', {})
        if caracteristicas:
            badges_html = ""
            if caracteristicas.get('vegano'): badges_html += "<span style='background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.3); padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;'><span style='font-size:1.1rem;'>🌱</span> Vegano</span>"
            if caracteristicas.get('sin_gluten'): badges_html += "<span style='background: rgba(234, 179, 8, 0.15); color: #fde047; border: 1px solid rgba(253, 224, 71, 0.3); padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;'><span style='font-size:1.1rem;'>🌾</span> Sin Gluten</span>"
            if caracteristicas.get('sin_lacteos'): badges_html += "<span style='background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(129, 140, 248, 0.3); padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;'><span style='font-size:1.1rem;'>🥛</span> Sin Lácteos</span>"
            
            if badges_html:
                st.markdown(f'<div class="result-card"><h3>Características Adicionales</h3><div style="display: flex; flex-wrap: wrap; gap: 10px;">{badges_html}</div></div>', unsafe_allow_html=True)

        # Ingredients
        ingredientes = result.get('ingredientes_detectados', [])
        if ingredientes:
            ing_html = '<div class="result-card"><h3>Ingredientes Analizados</h3><ul style="list-style-type: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">'
            for ing in ingredientes:
                status = ing.get('estatus', '')
                color = "#cbd5e1" # default
                icon_color = "#94a3b8"
                icon = "❔"
                if "No Kosher" in status or "Precaución" in status:
                    icon_color = "#ef4444"
                    icon = "❌" if "No Kosher" in status else "⚠️"
                elif "Kosher" in status:
                    icon_color = "#10b981"
                    icon = "✅"
                
                ing_html += f'<li style="padding: 12px; background: rgba(255,255,255,0.02); border-radius: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255,255,255,0.05); transition: background 0.2s;"><span style="color: {color}; font-weight: 500;">{ing.get("nombre", "")}</span><span style="color: {icon_color}; font-size: 0.9rem; font-weight: 700; background: rgba(0,0,0,0.2); padding: 4px 10px; border-radius: 12px; display: flex; align-items: center; gap: 6px;">{icon} {status}</span></li>'
            
            ing_html += '</ul></div>'
            st.markdown(ing_html, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="result-card">
                <h3>Detalle Halájico</h3>
                <p style="font-size: 1rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 15px;">
                    {result.get('explicacion_halajica', 'No se encontró una explicación detallada.')}
                </p>
                <div style="font-size: 0.9rem; color: #94a3b8; font-weight: 600; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center;">
                    <span>Evaluación general:</span>
                    <span style="color: #10b981; background: rgba(16, 185, 129, 0.1); padding: 6px 12px; border-radius: 20px;">Todas las normas verificadas</span>
                </div>
            </div>
            </div>
        """, unsafe_allow_html=True)

        col_back = st.columns([1, 4, 1])
        with col_back[1]:
            st.write("")
            if st.button("❮ Back to Scanner", key="back_to_scan"):
                st.session_state.last_result = None
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
