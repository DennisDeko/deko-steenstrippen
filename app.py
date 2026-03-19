import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from datetime import date
from io import BytesIO

from utils.visualizer import draw_strip_diagram
from utils.pdf_generator import generate_pdf

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deko – Steenstrippen Configurator",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] {
      font-family: 'DM Sans', sans-serif;
  }
  .block-container { padding-top: 1.5rem; }

  /* Header */
  .deko-header {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
      color: white;
      padding: 1.8rem 2.2rem;
      border-radius: 12px;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      gap: 1rem;
  }
  .deko-header h1 {
      font-family: 'DM Serif Display', serif;
      font-size: 2rem;
      margin: 0;
      letter-spacing: -0.5px;
  }
  .deko-header p {
      margin: 0.2rem 0 0 0;
      opacity: 0.75;
      font-size: 0.9rem;
  }
  .deko-badge {
      background: #e84545;
      color: white;
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
  }

  /* Section cards */
  .section-card {
      background: #f8f9fb;
      border: 1px solid #e8eaed;
      border-radius: 10px;
      padding: 1.2rem 1.4rem;
      margin-bottom: 1rem;
  }
  .section-title {
      font-weight: 600;
      font-size: 0.8rem;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #6b7280;
      margin-bottom: 0.8rem;
  }

  /* Dimension badges */
  .dim-badge {
      display: inline-block;
      background: #1a1a2e;
      color: white;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      text-align: center;
      line-height: 26px;
      font-weight: 700;
      font-size: 0.85rem;
      margin-right: 6px;
  }
  .dim-badge.x { background: #e84545; }

  /* Summary box */
  .summary-box {
      background: linear-gradient(135deg, #1a1a2e, #0f3460);
      color: white;
      border-radius: 10px;
      padding: 1.2rem 1.4rem;
  }
  .summary-box h4 {
      margin: 0 0 0.8rem 0;
      font-family: 'DM Serif Display', serif;
      font-size: 1.1rem;
  }
  .summary-row {
      display: flex;
      justify-content: space-between;
      padding: 0.3rem 0;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      font-size: 0.87rem;
  }
  .summary-row:last-child { border-bottom: none; }
  .summary-label { opacity: 0.7; }
  .summary-value { font-weight: 600; }

  /* Sticker */
  [data-testid="stSidebar"] {
      background: #f0f2f8;
  }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="deko-header">
  <div>
    <span class="deko-badge">Geveloplossingen</span>
    <h1>🧱 Steenstrippen – Afgekorte Strip</h1>
    <p>Deko B.V. · Peppelenbos 16, 6662 WB Elst (Gld) · sales@deko.nu</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Layout: two columns ────────────────────────────────────────────────────────
col_form, col_vis = st.columns([1, 1.4], gap="large")

# ═══════════════════════════════════════════════════════════════════════════════
# LEFT: Form
# ═══════════════════════════════════════════════════════════════════════════════
with col_form:

    # — Klantgegevens —
    st.markdown('<div class="section-title">📋 Klantgegevens</div>', unsafe_allow_html=True)
    bedrijf      = st.text_input("Bedrijfsnaam",     placeholder="bijv. Bouwbedrijf De Vries")
    contactpers  = st.text_input("Contactpersoon",   placeholder="Naam contactpersoon")
    project      = st.text_input("Project",          placeholder="Projectnaam of -nummer")
    col_s, col_d = st.columns(2)
    with col_s:
        sortering = st.text_input("Sortering",       placeholder="bijv. WF, DF…")
    with col_d:
        stuks     = st.number_input("Stuks", min_value=1, value=100, step=1)
    leverdatum   = st.date_input("Gewenste leverdatum", value=date.today())

    st.markdown("---")

    # — Afmetingen —
    st.markdown('<div class="section-title">📐 Afmetingen (mm)</div>', unsafe_allow_html=True)

    st.markdown("""
    <small style="color:#6b7280">
    Vul de gewenste afmetingen in. Gebruik <b>X</b> voor de afkorting (zaagsnede-positie).
    </small>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        A = st.number_input("A – Breedte voorzijde (mm)", min_value=0, value=210, step=1,
                            help="Breedte van de voorzijde van de strip")
        B = st.number_input("B – Lengte strip (mm)",      min_value=0, value=1000, step=1,
                            help="Totale lengte van de strip")
        C = st.number_input("C – Hoogte strip (mm)",      min_value=0, value=65, step=1,
                            help="Hoogte (dikte) van de strip")
    with col2:
        D = st.number_input("D – Diepte strip (mm)",      min_value=0, value=22, step=1,
                            help="Diepte (terug) van de strip")
        X = st.number_input("X – Zaagsnede positie (mm)", min_value=0, value=300, step=1,
                            help="Afstand van het kortste uiteinde tot de zaagsnede")

    # Validation warning
    if X > 0 and B > 0 and X >= B:
        st.warning("⚠️ X (zaagsnede) mag niet groter zijn dan of gelijk zijn aan B (totale lengte).")

    st.markdown("---")

    # — Opmerkingen —
    opmerkingen = st.text_area("Opmerkingen / bijzonderheden", height=80,
                               placeholder="Eventuele extra informatie…")

    # — PDF knop —
    if st.button("📄 Genereer PDF-formulier", use_container_width=True, type="primary"):
        data = dict(
            bedrijf=bedrijf, contactpersoon=contactpers, project=project,
            sortering=sortering, stuks=stuks,
            leverdatum=str(leverdatum), opmerkingen=opmerkingen,
            A=A, B=B, C=C, D=D, X=X
        )
        pdf_bytes = generate_pdf(data)
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_bytes,
            file_name=f"deko_steenstrip_{project or 'order'}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# ═══════════════════════════════════════════════════════════════════════════════
# RIGHT: Visualization
# ═══════════════════════════════════════════════════════════════════════════════
with col_vis:

    st.markdown('<div class="section-title">🎨 Visuele weergave</div>', unsafe_allow_html=True)

    fig = draw_strip_diagram(A=A, B=B, C=C, D=D, X=X)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # — Live maatoverzicht —
    st.markdown("---")
    st.markdown('<div class="section-title">📊 Maatoverzicht</div>', unsafe_allow_html=True)

    rest = B - X if B > X else 0
    cols = st.columns(5)
    metrics = [
        ("A", A, "Breedte"),
        ("B", B, "Lengte"),
        ("C", C, "Hoogte"),
        ("D", D, "Diepte"),
        ("X", X, "Zaagsnede"),
    ]
    for i, (lbl, val, desc) in enumerate(metrics):
        with cols[i]:
            color = "#e84545" if lbl == "X" else "#1a1a2e"
            st.markdown(f"""
            <div style="background:{color};color:white;border-radius:8px;
                        padding:0.6rem;text-align:center;margin-bottom:0.3rem">
              <div style="font-size:1.4rem;font-weight:700">{val}</div>
              <div style="font-size:0.65rem;opacity:0.8">mm</div>
              <div style="font-size:0.7rem;font-weight:600;margin-top:2px">{lbl} – {desc}</div>
            </div>
            """, unsafe_allow_html=True)

    if B > 0 and X > 0:
        st.markdown(f"""
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;
                    padding:0.8rem 1rem;margin-top:0.8rem;font-size:0.88rem">
          ✂️ <b>Benodigd stuk:</b> {X} mm &nbsp;|&nbsp;
          🗑️ <b>Restant:</b> {rest} mm
          &nbsp;&nbsp;<span style="color:#6b7280;font-size:0.8rem">
            (totale lengte B = {B} mm)
          </span>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#9ca3af;font-size:0.8rem;padding:0.5rem">
  Deko B.V. · Peppelenbos 16, 6662 WB Elst (Gld) · 
  T +31 (0) 481 – 366 466 · 
  <a href="mailto:sales@deko.nu" style="color:#9ca3af">sales@deko.nu</a>
</div>
""", unsafe_allow_html=True)
