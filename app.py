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
                            value=int(steen_A) if steen_A else 210, step=1)
        B = st.number_input("B – Lengte (mm)", min_value=0,
                            value=int(steen_B) if steen_B else 1000, step=1)
        C = st.number_input("C – Hoogte (mm)", min_value=0,
                            value=int(steen_C) if steen_C else 65, step=1)
    with col2:
        D = st.number_input("D – Diepte (mm)",           min_value=0, value=22,  step=1)
        X = st.number_input("X – Zaagsnede voor (mm)",   min_value=0, value=300, step=1,
                            help="Afstand zaagsnede vanaf de voorkant")
        Y = st.number_input("Y – Zaagsnede achter (mm)", min_value=0, value=0,   step=1,
                            help="Afstand zaagsnede vanaf de achterkant (0 = geen Y-snede)")

    # Validatie
    if X > 0 and Y > 0 and B > 0 and (X + Y) >= B:
        st.error("⚠️ X + Y mag niet groter zijn dan of gelijk zijn aan B.")
    elif X > 0 and B > 0 and X >= B:
        st.warning("⚠️ X mag niet groter zijn dan of gelijk zijn aan B.")

    st.markdown("---")
    opmerkingen = st.text_area("Opmerkingen", height=70,
                               placeholder="Eventuele extra informatie…")

    if st.button("📄 Genereer PDF-formulier", use_container_width=True, type="primary"):
        data = dict(
            bedrijf=bedrijf, contactpersoon=contactpers, project=project,
            sortering=sortering, stuks=stuks,
            leverdatum=str(leverdatum), opmerkingen=opmerkingen,
            steenformaat=gekozen if steen_A else "",
            A=A, B=B, C=C, D=D, X=X, Y=Y,
        )
        pdf_bytes = generate_pdf(data)
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_bytes,
            file_name=f"deko_steenstrip_{project or 'order'}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

with col_vis:

    st.markdown('<div class="section-title">🎨 Visuele weergave</div>', unsafe_allow_html=True)

    fig = draw_strip_diagram(A=A, B=B, C=C, D=D, X=X, Y=Y)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("---")
    st.markdown('<div class="section-title">📊 Maatoverzicht</div>', unsafe_allow_html=True)

    benodigd = B - X - Y if Y > 0 else X
    restant  = B - benodigd

    labels = ["A", "B", "C", "D", "X", "Y"] if Y > 0 else ["A", "B", "C", "D", "X"]
    values = [A,   B,   C,   D,   X,   Y]   if Y > 0 else [A,   B,   C,   D,   X]
    descs  = ["Breedte","Lengte","Hoogte","Diepte","Zaagsnede voor","Zaagsnede achter"] \
             if Y > 0 else ["Breedte","Lengte","Hoogte","Diepte","Zaagsnede"]

    cols = st.columns(len(labels))
    for i, (lbl, val, desc) in enumerate(zip(labels, values, descs)):
        with cols[i]:
            color = "#e84545" if lbl in ("X", "Y") else "#1a1a2e"
            st.markdown(f"""
            <div style="background:{color};color:white;border-radius:8px;
                        padding:0.6rem;text-align:center;margin-bottom:0.3rem">
              <div style="font-size:1.3rem;font-weight:700">{val}</div>
              <div style="font-size:0.6rem;opacity:0.8">mm</div>
              <div style="font-size:0.65rem;font-weight:600;margin-top:2px">{lbl} – {desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;
                padding:0.8rem 1rem;margin-top:0.8rem;font-size:0.88rem">
      ✂️ <b>Benodigd stuk:</b> {B - X - Y if Y > 0 else X} mm &nbsp;|&nbsp;
      🗑️ <b>Totaal restant:</b> {X + Y if Y > 0 else B - X} mm
      {"&nbsp;(X: " + str(X) + " mm + Y: " + str(Y) + " mm)" if Y > 0 else ""}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#9ca3af;font-size:0.8rem;padding:0.5rem">
  Deko B.V. · Peppelenbos 16, 6662 WB Elst (Gld) ·
  T +31 (0) 481 – 366 466 ·
  <a href="mailto:sales@deko.nu" style="color:#9ca3af">sales@deko.nu</a>
</div>
""", unsafe_allow_html=True)
