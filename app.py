import streamlit as st
import matplotlib.pyplot as plt
from datetime import date

from utils.visualizer import draw_strip_diagram
from utils.pdf_generator import generate_pdf

# ── Steenformaten ──────────────────────────────────────────────────────────────
STEENFORMATEN = {
    "— Kies een steenformaat —":          (None, None, None),
    "Brabantse steen":                    (180,  88,  53),
    "Deens formaat":                      (228, 108,  54),
    "Dikformaat / waaldikformaat":        (210, 100,  65),
    "Dordtse steen":                      (180,  88,  43),
    "Dubbel waalformaat":                 (210, 100, 110),
    "Dunnformat (DF)":                    (240, 115,  52),
    "Engels formaat":                     (210, 103,  65),
    "Euroformat":                         (188,  90,  88),
    "F5":                                 (230, 110,  57),
    "Friese drieling":                    (184,  80,  40),
    "Friese mop":                         (217, 103,  45),
    "Goudse steen":                       (155,  72,  53),
    "Groninger steen":                    (240, 120,  60),
    "Hilversums formaat":                 (240,  90,  40),
    "IJsselformaat":                      (160,  78,  41),
    "Juffertje":                          (175,  82,  40),
    "Kathedraal I":                       (240, 115,  65),
    "Kathedraal II":                      (270, 105,  55),
    "Klampmuur-dikformaat":               (100,  65, 210),
    "Kloostermop I":                      (280, 105,  80),
    "Kloostermop II":                     (320, 130,  80),
    "Lilliput I":                         (160,  75,  35),
    "Lilliput II":                        (150,  70,  30),
    "Limburgse steen":                    (240, 120,  65),
    "Moduul 190-140-90":                  (190, 140,  90),
    "Moduul 190-90-40":                   (190,  90,  40),
    "Moduul 190-90-50":                   (190,  90,  50),
    "Moduul 190-90-90":                   (190,  90,  90),
    "Moduul 240-90-90":                   (240,  90,  90),
    "Moduul 290-115-190":                 (290, 115, 190),
    "Moduul 290-115-90":                  (290, 115,  90),
    "Moduul 290-90-190":                  (290,  90, 190),
    "Moduul 290-90-90":                   (290,  90,  90),
    "Normalformat (NF)":                  (240, 115,  71),
    "Oldenburgerformat (OF)":             (210, 105,  52),
    "Reichsformat (RF)":                  (240, 115,  61),
    "Rijnformaat":                        (180,  87,  41),
    "Romeins formaat":                    (240, 115,  42),
    "Utrechts plat":                      (215, 102,  38),
    "Vechtformaat":                       (210, 100,  40),
    "Verblender (2DF)":                   (240, 115, 113),
    "Waalformaat":                        (210, 100,  50),
}

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deko – Steenstrippen Configurator",
    page_icon="🧱",
    layout="wide",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .block-container { padding-top: 1.5rem; }
  .deko-header {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
      color: white; padding: 1.8rem 2.2rem; border-radius: 12px;
      margin-bottom: 1.5rem;
  }
  .deko-header h1 { font-family: 'DM Serif Display', serif; font-size: 2rem; margin: 0; }
  .deko-header p  { margin: 0.2rem 0 0 0; opacity: 0.75; font-size: 0.9rem; }
  .deko-badge {
      background: #e84545; color: white; padding: 0.25rem 0.75rem;
      border-radius: 20px; font-size: 0.75rem; font-weight: 600;
      letter-spacing: 1px; text-transform: uppercase;
  }
  .section-title {
      font-weight: 600; font-size: 0.8rem; letter-spacing: 1.5px;
      text-transform: uppercase; color: #6b7280; margin-bottom: 0.8rem;
  }
  .steen-info {
      background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px;
      padding: 0.7rem 1rem; margin-bottom: 0.8rem; font-size: 0.88rem;
  }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="deko-header">
  <span class="deko-badge">Geveloplossingen</span>
  <h1>🧱 Steenstrippen – Afgekorte Strip</h1>
  <p>Deko B.V. · Peppelenbos 16, 6662 WB Elst (Gld) · sales@deko.nu</p>
</div>
""", unsafe_allow_html=True)

col_form, col_vis = st.columns([1, 1.4], gap="large")

with col_form:

    st.markdown('<div class="section-title">📋 Klantgegevens</div>', unsafe_allow_html=True)
    bedrijf     = st.text_input("Bedrijfsnaam",   placeholder="bijv. Bouwbedrijf De Vries")
    contactpers = st.text_input("Contactpersoon", placeholder="Naam contactpersoon")
    project     = st.text_input("Project",        placeholder="Projectnaam of -nummer")
    col_s, col_d = st.columns(2)
    with col_s:
        sortering = st.text_input("Sortering", placeholder="bijv. WF, DF…")
    with col_d:
        stuks = st.number_input("Stuks", min_value=1, value=100, step=1)
    leverdatum = st.date_input("Gewenste leverdatum", value=date.today())

    st.markdown("---")

    st.markdown('<div class="section-title">🧱 Steenformaat</div>', unsafe_allow_html=True)
    gekozen = st.selectbox(
        "Kies een steensoort (vult A, B en C automatisch in)",
        options=list(STEENFORMATEN.keys()),
    )
    steen_B, steen_A, steen_C = STEENFORMATEN[gekozen]
    if steen_A is not None:
        st.markdown(f"""
        <div class="steen-info">
          📐 <b>{gekozen}</b> &nbsp;—&nbsp;
          Lengte <b>{steen_B} mm</b> &nbsp;|&nbsp;
          Breedte <b>{steen_A} mm</b> &nbsp;|&nbsp;
          Hoogte <b>{steen_C} mm</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">📐 Afmetingen (mm)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        A = st.number_input("A – Breedte (mm)", min_value=0,
                            value=int(steen_A) if steen_A el
