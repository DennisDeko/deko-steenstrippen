import streamlit as st
import matplotlib.pyplot as plt
from datetime import date

from utils.visualizer import draw_strip_diagram
from utils.pdf_generator import generate_pdf

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

st.set_page_config(page_title="Deko – Steenstrippen", page_icon="🧱", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .block-container { padding-top: 1.5rem; }
  .deko-header {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
      color: white; padding: 1.8rem 2.2rem; border-radius: 12px; margin-bottom: 1.5rem;
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
      text-transform: uppercase; color: #6b7280; margin-bottom: 0.6rem;
  }
  .steen-info {
      background: #f0f9ff; border: 1px solid #bae6fd;
      border-radius: 8px; padding: 0.7rem 1rem; margin-bottom: 0.8rem; font-size: 0.88rem;
  }
  .cut-x    { background:#fef2f2; border:1px solid #fecaca; border-radius:8px; padding:0.6rem 0.8rem; margin-bottom:0.4rem; }
  .cut-y    { background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:0.6rem 0.8rem; margin-bottom:0.4rem; }
  .cut-zool { background:#faf5ff; border:1px solid #e9d5ff; border-radius:8px; padding:0.6rem 0.8rem; margin-bottom:0.4rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="deko-header">
  <span class="deko-badge">Geveloplossingen</span>
  <h1>🧱 Steenstrippen – Afgekorte Strip</h1>
  <p>Deko B.V. · Peppelenbos 16, 6662 WB Elst (Gld) · sales@deko.nu</p>
</div>
""", unsafe_allow_html=True)

# Session state
for key, default in [("x_cuts",[300]),("y_cuts",[]),("zool_cuts",[])]:
    if key not in st.session_state:
        st.session_state[key] = default

col_form, col_vis = st.columns([1, 1.4], gap="large")

with col_form:

    st.markdown('<div class="section-title">📋 Klantgegevens</div>', unsafe_allow_html=True)
    bedrijf     = st.text_input("Bedrijfsnaam",   placeholder="bijv. Bouwbedrijf De Vries")
    contactpers = st.text_input("Contactpersoon", placeholder="Naam contactpersoon")
    project     = st.text_input("Project",        placeholder="Projectnaam of -nummer")
    cs, cd = st.columns(2)
    with cs: sortering = st.text_input("Sortering", placeholder="bijv. WF, DF…")
    with cd: stuks = st.number_input("Stuks", min_value=1, value=100, step=1)
    leverdatum = st.date_input("Gewenste leverdatum", value=date.today())

    st.markdown("---")
    st.markdown('<div class="section-title">🧱 Steenformaat</div>', unsafe_allow_html=True)
    gekozen = st.selectbox("Kies een steensoort", options=list(STEENFORMATEN.keys()))
    steen_B, steen_A, steen_C = STEENFORMATEN[gekozen]
    if steen_A:
        st.markdown(f'<div class="steen-info">📐 <b>{gekozen}</b> — Lengte <b>{steen_B}mm</b> | Breedte <b>{steen_A}mm</b> | Hoogte <b>{steen_C}mm</b></div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">📐 Basisafmetingen (mm)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        A = st.number_input("A – Breedte (mm)", min_value=1, value=int(steen_A) if steen_A else 100, step=1)
        B = st.number_input("B – Lengte (mm)",  min_value=1, value=int(steen_B) if steen_B else 210, step=1)
    with c2:
        C = st.number_input("C – Hoogte (mm)",  min_value=1, value=int(steen_C) if steen_C else 65,  step=1)
        D = st.number_input("D – Diepte (mm)",  min_value=1, value=22, step=1)

    st.markdown("---")

    # ── X-snedes (langs lengte) ───────────────────────────────────────────
    st.markdown('<div class="section-title">✂️ X-snedes – langs de lengte (B-as)</div>', unsafe_allow_html=True)
    st.caption("Positie in mm vanaf de voorkant")
    x_vals = []; rm_x = None
    for i, val in enumerate(st.session_state.x_cuts):
        st.markdown('<div class="cut-x">', unsafe_allow_html=True)
        ca, cb = st.columns([3,1])
        with ca: v = st.number_input(f"X{i+1} (mm)", min_value=1, max_value=int(B)-1, value=min(int(val),int(B)-1), step=1, key=f"xc_{i}")
        with cb:
            st.write(""); st.write("")
            if st.button("🗑️", key=f"dx_{i}"): rm_x = i
        x_vals.append(v)
        st.markdown('</div>', unsafe_allow_html=True)
    if rm_x is not None:
        st.session_state.x_cuts.pop(rm_x); st.rerun()
    if st.button("➕ X-snede toevoegen", use_container_width=True):
        st.session_state.x_cuts.append(min(100, int(B)-1)); st.rerun()
    st.session_state.x_cuts = x_vals

    st.markdown("---")

    # ── Y-snedes (langs breedte, 90° van X) ──────────────────────────────
    st.markdown('<div class="section-title">✂️ Y-snedes – langs de breedte (A-as, 90° van X)</div>', unsafe_allow_html=True)
    st.caption("Positie in mm vanaf de linkerkant")
    y_vals = []; rm_y = None
    for i, val in enumerate(st.session_state.y_cuts):
        st.markdown('<div class="cut-y">', unsafe_allow_html=True)
        ca, cb = st.columns([3,1])
        with ca: v = st.number_input(f"Y{i+1} (mm)", min_value=1, max_value=int(A)-1, value=min(int(val),int(A)-1), step=1, key=f"yc_{i}")
        with cb:
            st.write(""); st.write("")
            if st.button("🗑️", key=f"dy_{i}"): rm_y = i
        y_vals.append(v)
        st.markdown('</div>', unsafe_allow_html=True)
    if rm_y is not None:
        st.session_state.y_cuts.pop(rm_y); st.rerun()
    if st.button("➕ Y-snede toevoegen", use_container_width=True):
        st.session_state.y_cuts.append(min(50, int(A)-1)); st.rerun()
    st.session_state.y_cuts = y_vals

    st.markdown("---")

    # ── Zool-snedes (langs hoogte) ────────────────────────────────────────
    st.markdown('<div class="section-title">✂️ Zool-snedes – langs de hoogte (C-as)</div>', unsafe_allow_html=True)
    st.caption("Positie in mm vanaf de onderkant")
    z_vals = []; rm_z = None
    for i, val in enumerate(st.session_state.zool_cuts):
        st.markdown('<div class="cut-zool">', unsafe_allow_html=True)
        ca, cb = st.columns([3,1])
        with ca: v = st.number_input(f"Z{i+1} (mm)", min_value=1, max_value=int(C)-1, value=min(int(val),int(C)-1), step=1, key=f"zc_{i}")
        with cb:
            st.write(""); st.write("")
            if st.button("🗑️", key=f"dz_{i}"): rm_z = i
        z_vals.append(v)
        st.markdown('</div>', unsafe_allow_html=True)
    if rm_z is not None:
        st.session_state.zool_cuts.pop(rm_z); st.rerun()
    if st.button("➕ Zool-snede toevoegen", use_container_width=True):
        st.session_state.zool_cuts.append(min(20, int(C)-1)); st.rerun()
    st.session_state.zool_cuts = z_vals

    st.markdown("---")
    opmerkingen = st.text_area("Opmerkingen", height=70, placeholder="Eventuele extra informatie…")

    if st.button("📄 Genereer PDF-formulier", use_container_width=True, type="primary"):
        data = dict(
            bedrijf=bedrijf, contactpersoon=contactpers, project=project,
            sortering=sortering, stuks=stuks, leverdatum=str(leverdatum),
            opmerkingen=opmerkingen, steenformaat=gekozen if steen_A else "",
            A=A, B=B, C=C, D=D,
            X=str(sorted(set(x_vals))),
            Y=str(sorted(set(y_vals))),
            Zool=str(sorted(set(z_vals))),
        )
        pdf_bytes = generate_pdf(data)
        st.download_button(label="⬇️ Download PDF", data=pdf_bytes,
                           file_name=f"deko_steenstrip_{project or 'order'}.pdf",
                           mime="application/pdf", use_container_width=True)

with col_vis:
    st.markdown('<div class="section-title">🎨 Visuele weergave</div>', unsafe_allow_html=True)

    fig = draw_strip_diagram(
        A=A, B=B, C=C, D=D,
        x_cuts=sorted(set(x_vals)),
        y_cuts=sorted(set(y_vals)),
        zool_cuts=sorted(set(z_vals)),
    )
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("---")
    st.markdown('<div class="section-title">📊 Maatoverzicht</div>', unsafe_allow_html=True)
    base_cols = st.columns(4)
    for i, (lbl, val, desc) in enumerate([("A",A,"Breedte"),("B",B,"Lengte"),("C",C,"Hoogte"),("D",D,"Diepte")]):
        with base_cols[i]:
            st.markdown(f"""<div style="background:#1a1a2e;color:white;border-radius:8px;
                padding:0.6rem;text-align:center">
                <div style="font-size:1.2rem;font-weight:700">{val}</div>
                <div style="font-size:0.6rem;opacity:0.8">mm</div>
                <div style="font-size:0.62rem;font-weight:600;margin-top:2px">{lbl} – {desc}</div>
            </div>""", unsafe_allow_html=True)

    for label, vals, color in [
        ("X-snedes (lengte)",  sorted(set(x_vals)), "#c0392b"),
        ("Y-snedes (breedte)", sorted(set(y_vals)), "#1a6fa8"),
        ("Zool-snedes (hoogte)", sorted(set(z_vals)), "#8e44ad"),
    ]:
        if vals:
            st.markdown(f"**{label}:**")
            cols = st.columns(len(vals))
            for i, v in enumerate(vals):
                with cols[i]:
                    st.markdown(f"""<div style="background:{color};color:white;border-radius:8px;
                        padding:0.5rem;text-align:center">
                        <div style="font-size:1.1rem;font-weight:700">{v}</div>
                        <div style="font-size:0.6rem;opacity:0.8">mm</div>
                    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""<div style="text-align:center;color:#9ca3af;font-size:0.8rem;padding:0.5rem">
  Deko B.V. · Peppelenbos 16, 6662 WB Elst (Gld) · T +31 (0) 481 – 366 466 ·
  <a href="mailto:sales@deko.nu" style="color:#9ca3af">sales@deko.nu</a>
</div>""", unsafe_allow_html=True)
