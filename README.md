# 🧱 Deko Steenstrippen – Afgekorte strip Configurator

Een interactieve Streamlit-applicatie voor het configureren en bestellen van **afgekorte steenstrippen** bij Deko B.V.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Functies

| Functie | Beschrijving |
|---|---|
| 📋 **Orderformulier** | Klantgegevens, sortering, stuks en leverdatum |
| 📐 **Maten invoer** | A, B, C, D en X (zaagsnede) in mm |
| 🎨 **3D-visualisatie** | Live isometrische weergave van de strip met zaagsnede |
| 📊 **Maatoverzicht** | Direct inzicht in benodigd stuk vs. restant |
| 📄 **PDF-export** | Volledig ingevuld bestelformulier als PDF downloaden |

---

## 🚀 Installatie & gebruik

### Lokaal draaien

```bash
# 1. Clone de repo
git clone https://github.com/<jouw-naam>/deko-steenstrippen.git
cd deko-steenstrippen

# 2. Maak een virtuele omgeving (aanbevolen)
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# 3. Installeer dependencies
pip install -r requirements.txt

# 4. Start de app
streamlit run app.py
```

De app opent automatisch op **http://localhost:8501**.

---

## 📦 Deploy op Streamlit Community Cloud

1. Push de repo naar GitHub
2. Ga naar [share.streamlit.io](https://share.streamlit.io)
3. Selecteer jouw repo → `app.py`
4. Klik **Deploy** — klaar!

---

## 📁 Projectstructuur

```
deko-steenstrippen/
├── app.py                   # Hoofdapplicatie (Streamlit UI)
├── requirements.txt         # Python-afhankelijkheden
├── README.md
└── utils/
    ├── __init__.py
    ├── visualizer.py        # 3D isometrische tekening (Matplotlib)
    └── pdf_generator.py     # PDF-formulier generatie (ReportLab)
```

---

## 📐 Maatdefinities

```
         ┌─────────────────────────────────────────┐
         │                                         │
   C/D   │   BENODIGD (rood)     │  RESTANT (grijs) │
         │                                         │
         └─────────────────────────────────────────┘
         ├──── X ────┤├──────── B - X ──────────────┤
         ├──────────────── B (totaal) ───────────────┤
```

| Maat | Beschrijving |
|---|---|
| **A** | Breedte van de voorzijde van de strip (mm) |
| **B** | Totale lengte van de strip (mm) |
| **C** | Hoogte van de strip (mm) |
| **D** | Diepte van de strip (mm) |
| **X** | Positie van de zaagsnede — afstand van het kortste uiteinde (mm) |

> **Let op:** X moet kleiner zijn dan B.

---

## 🏢 Over Deko B.V.

**Deko B.V.**  
Peppelenbos 16  
6662 WB Elst (Gld)  
T +31 (0) 481 – 366 466  
[sales@deko.nu](mailto:sales@deko.nu)

---

## 📄 Licentie

MIT — vrij te gebruiken en aan te passen.
