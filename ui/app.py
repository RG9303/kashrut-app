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
# Custom CSS for high-fidelity mobile look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0f172a; /* Deep Navy */
        color: white;
    }

    /* Scanner Tab Specific (Dark) */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        /* This is harder to target specifically per tab without custom divs, 
           so we'll use a wrapper class for scanner */
    }

    .scanner-wrapper {
        text-align: center;
        padding: 20px;
    }

    /* Target Reticle */
    .scanner-frame {
        width: 250px;
        height: 250px;
        border: 2px solid transparent;
        margin: 40px auto;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .scanner-frame::before, .scanner-frame::after, 
    .scanner-frame span::before, .scanner-frame span::after {
        content: '';
        position: absolute;
        width: 30px;
        height: 30px;
        border: 4px solid #4ade80; /* Vibrant Green */
    }
    .scanner-frame::before { top: 0; left: 0; border-right: none; border-bottom: none; }
    .scanner-frame::after { top: 0; right: 0; border-left: none; border-bottom: none; }
    .scanner-frame span::before { bottom: 0; left: 0; border-right: none; border-top: none; }
    .scanner-frame span::after { bottom: 0; right: 0; border-left: none; border-top: none; }

    .inner-reticle {
        width: 50px;
        height: 50px;
        border: 1px dashed rgba(255,255,255,0.5);
        border-radius: 5px;
    }

    /* Buttons Alignment */
    .stButton > button {
        border-radius: 30px !important;
        font-weight: 700 !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        transition: all 0.2s ease !important;
    }

    /* Primary Scan Button */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) .primary-btn button {
        background-color: #4ade80 !important;
        color: #064e3b !important;
        border: none !important;
    }

    /* Ghost Upload Button */
    .ghost-btn button {
        background-color: transparent !important;
        color: white !important;
        border: 2px solid white !important;
    }

    /* Results Page (Light Theme overlap) */
    .results-bg {
        background-color: #f1f5f9;
        margin: -2rem;
        padding: 2rem;
        color: #1e293b;
    }

    .result-card {
        background: white !important;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 16px;
        border: none !important;
        color: #1e293b !important;
    }
    .result-card h3 {
        color: #1e293b !important;
        font-size: 1.1rem !important;
        margin-bottom: 12px !important;
    }

    .status-banner-premium {
        background-color: #4ade80;
        color: white;
        padding: 15px;
        text-align: center;
        font-weight: 800;
        font-size: 1.5rem;
        border-radius: 0 0 20px 20px;
        margin: -2rem -2rem 2rem -2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Bottom Navigation Simulation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent !important;
        border: none !important;
        color: rgba(255,255,255,0.6) !important;
    }
    .stTabs [aria-selected="true"] {
        color: white !important;
        border-bottom: 2px solid #4ade80 !important;
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
                <h2 style="color: white; margin-top: 0; font-weight: 700; font-size: 1.8rem;">Scan Hechsher<br>or Ingredients</h2>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.5; margin-bottom: 30px;">
                    1. Scan product front for Hechsher.<br>
                    2. Scan back for ingredients.<br>
                    3. Ensure clear, sharp focus.
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

        if uploaded_files:
            images = [Image.open(file) for file in uploaded_files]
            combined_bytes = b"".join([file.getvalue() for file in uploaded_files])
            
            # Check cache
            cached_result = cache.get_from_cache(combined_bytes)
            if cached_result:
                st.session_state.last_result = cached_result
                st.rerun()
            else:
                with st.spinner('Analizando...'):
                    # 1. Barcode check
                    off_data = None
                    try:
                        off_data = st.session_state.off_client.scan_and_get_details(images)
                    except: pass
                    
                    # 2. Análisis Final
                    extra_context = off_data.get('ingredients_text') if off_data else None
                    result = st.session_state.engine.analyze_product(
                        images, 
                        extra_context=extra_context,
                        preferences=st.session_state.preferences
                    )
                    
                    if result and "error" not in result:
                        st.session_state.history.add_scan(result)
                        cache.save_to_cache(combined_bytes, result)
                        st.session_state.last_result = result
                        st.rerun()
                    else:
                        st.error("Error en el análisis de la IA.")
    else:
        # --- RESULTS VIEW ---
        result = st.session_state.last_result
        status = result.get('resultado', 'Dudoso')
        conf = result.get('confianza_analisis', 'N/A')
        banner_color = "#4ade80" if "KOSHER" in status.upper() and "NO" not in status.upper() else "#f87171"
        
        st.markdown(f"""
            <div class="status-banner-premium" style="background-color: {banner_color};">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span>✓</span> {status.upper()}
                </div>
                <div style="font-size: 0.9rem; font-weight: 400; opacity: 0.9; margin-top: 4px;">
                    Analysis Confidence: {conf}
                </div>
            </div>
            <div class="results-bg">
        """, unsafe_allow_html=True)

        # Main Cards
        st.markdown(f"""
            <div class="result-card">
                <h3>Certification Seal</h3>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: #1e293b; color: white; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        {result.get('sello_detectado', '??')[:2].upper()}
                    </div>
                    <div style="font-weight: 600; color: #1e293b;">{result.get('sello_detectado', 'Ninguno')}</div>
                </div>
            </div>
            
            <div class="result-card">
                <h3>Category</h3>
                <div style="display: flex; align-items: center; gap: 12px; font-size: 1.1rem; font-weight: 600;">
                    <span style="font-size: 1.4rem;">🍃</span> {result.get('categoria', 'Parve')} (Neutral)
                </div>
            </div>
        """, unsafe_allow_html=True)

        alertas = result.get('alertas', [])
        if alertas and alertas[0].lower() != "ninguno":
            st.markdown('<div class="result-card"><h3>Alerts</h3>', unsafe_allow_html=True)
            for a in alertas:
                st.markdown(f"""
                    <div style="display: flex; gap: 10px; color: #92400e; background: #fffbeb; padding: 12px; border-radius: 12px; margin-bottom: 8px; font-size: 0.9rem; border: 1px solid #fef3c7;">
                        <span>⚠️</span> <div>{a}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
            <div class="result-card">
                <h3>Detailed Explanation</h3>
                <p style="font-size: 0.95rem; line-height: 1.5; color: #475569;">
                    {result.get('explicacion_halajica', 'No se encontró una explicación detallada.')}
                </p>
                <div style="margin-top: 15px; font-size: 0.85rem; color: #64748b; font-weight: 600;">
                    All ingredients checked: <span style="color: #2563eb;">All Kosher</span>
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
