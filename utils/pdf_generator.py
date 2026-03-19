"""
utils/pdf_generator.py
Generates a filled-in PDF order form for Deko Steenstrippen – Afgekorte strip.
Uses ReportLab for PDF generation.
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether,
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle
from reportlab.graphics import renderPDF


# ── Brand colours ──────────────────────────────────────────────────────────────
DEKO_DARK  = colors.HexColor("#1a1a2e")
DEKO_RED   = colors.HexColor("#c0392b")
DEKO_GREY  = colors.HexColor("#6b7280")
DEKO_LIGHT = colors.HexColor("#f8f9fb")


def _header_drawing(width: float) -> Drawing:
    """Return a branded header banner as a ReportLab Drawing."""
    h = 22 * mm
    d = Drawing(width, h)
    # Background
    d.add(Rect(0, 0, width, h, fillColor=DEKO_DARK, strokeColor=None))
    # Red accent bar on the left
    d.add(Rect(0, 0, 4 * mm, h, fillColor=DEKO_RED, strokeColor=None))
    # Company name
    d.add(String(10 * mm, h / 2 + 3,
                 "DEKO B.V.",
                 fontName="Helvetica-Bold", fontSize=13,
                 fillColor=colors.white))
    d.add(String(10 * mm, h / 2 - 5,
                 "Steenstrippen – Afgekorte strip  |  Geveloplossingen",
                 fontName="Helvetica", fontSize=8,
                 fillColor=colors.Color(1, 1, 1, alpha=0.75)))
    # Date (top-right)
    today = datetime.today().strftime("%d-%m-%Y")
    d.add(String(width - 35 * mm, h / 2 - 2,
                 f"Datum: {today}",
                 fontName="Helvetica", fontSize=7,
                 fillColor=colors.Color(1, 1, 1, alpha=0.65)))
    return d


def _strip_diagram_drawing(A, B, C, D, X, width=130 * mm) -> Drawing:
    """
    Simple 2-D schematic cross-section diagram for the PDF.
    Shows a top-down strip with the cut position X marked.
    """
    height = 40 * mm
    d = Drawing(width, height)

    # Scale: map B → 100mm drawing width
    margin = 10 * mm
    draw_w = width - 2 * margin
    draw_h = 18 * mm
    bar_y  = (height - draw_h) / 2

    scale = draw_w / max(B, 1)

    # Full strip (grey = restant)
    d.add(Rect(margin, bar_y, draw_w, draw_h,
               fillColor=colors.HexColor("#d1d5db"),
               strokeColor=colors.HexColor("#6b7280"),
               strokeWidth=0.5))

    # Needed part (red)
    needed_w = X * scale
    d.add(Rect(margin, bar_y, needed_w, draw_h,
               fillColor=colors.HexColor("#e74c3c"),
               strokeColor=colors.HexColor("#c0392b"),
               strokeWidth=1))

    # Cut dashed line
    cut_x = margin + needed_w
    for i in range(0, int(height), 3):
        if i % 6 < 3:
            d.add(Line(cut_x, i, cut_x, min(i + 3, height),
                       strokeColor=DEKO_RED, strokeWidth=1.2))

    # Labels inside bars
    lbl_x = margin + needed_w / 2
    d.add(String(lbl_x - 8 * mm, bar_y + draw_h / 2 - 2,
                 "Benodigde strip",
                 fontName="Helvetica-Bold", fontSize=6.5,
                 fillColor=colors.white))

    rest_x = margin + needed_w + (draw_w - needed_w) / 2
    d.add(String(rest_x - 8 * mm, bar_y + draw_h / 2 - 2,
                 "Restant",
                 fontName="Helvetica", fontSize=6.5,
                 fillColor=colors.HexColor("#374151")))

    # ── Dimension annotations ──────────────────────────────────────────────────
    arrow_y = bar_y - 7 * mm

    # X arrow
    d.add(Line(margin, arrow_y, margin + needed_w, arrow_y,
               strokeColor=DEKO_RED, strokeWidth=1))
    d.add(String(margin + needed_w / 2 - 5 * mm, arrow_y - 4 * mm,
                 f"X = {int(X)} mm",
                 fontName="Helvetica-Bold", fontSize=7,
                 fillColor=DEKO_RED))

    # B arrow (total)
    b_arr_y = bar_y + draw_h + 6 * mm
    d.add(Line(margin, b_arr_y, margin + draw_w, b_arr_y,
               strokeColor=DEKO_DARK, strokeWidth=0.8))
    d.add(String(margin + draw_w / 2 - 5 * mm, b_arr_y + 1 * mm,
                 f"B = {int(B)} mm (totale lengte)",
                 fontName="Helvetica", fontSize=6.5,
                 fillColor=DEKO_DARK))

    # Height label (right side)
    d.add(String(margin + draw_w + 2 * mm, bar_y + draw_h / 2 - 2,
                 f"C={int(C)}mm  D={int(D)}mm",
                 fontName="Helvetica", fontSize=6,
                 fillColor=DEKO_GREY))

    return d


def generate_pdf(data: dict) -> bytes:
    """
    Generate a complete order-form PDF and return it as bytes.

    Parameters
    ----------
    data : dict with keys:
        bedrijf, contactpersoon, project, sortering, stuks,
        leverdatum, opmerkingen, A, B, C, D, X
    """
    buf = BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=15 * mm,   bottomMargin=20 * mm,
        title="Deko – Steenstrippen Afgekorte strip",
    )

    W = A4[0] - 36 * mm   # usable width

    styles = getSampleStyleSheet()
    normal = ParagraphStyle("normal", fontName="Helvetica",
                            fontSize=9, leading=14)
    bold   = ParagraphStyle("bold",   fontName="Helvetica-Bold",
                            fontSize=9, leading=14)
    small  = ParagraphStyle("small",  fontName="Helvetica",
                            fontSize=7.5, leading=12, textColor=DEKO_GREY)
    section_title = ParagraphStyle("section", fontName="Helvetica-Bold",
                                   fontSize=8, leading=12,
                                   textColor=DEKO_GREY,
                                   spaceAfter=3)

    story = []

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(_header_drawing(W))
    story.append(Spacer(1, 6 * mm))

    # ── Klantgegevens table ───────────────────────────────────────────────────
    story.append(Paragraph("KLANTGEGEVENS", section_title))

    def field_row(label, value):
        return [
            Paragraph(label, bold),
            Paragraph(str(value) if value else "—", normal),
        ]

    client_data = [
        field_row("Bedrijfsnaam",    data.get("bedrijf", "")),
        field_row("Contactpersoon",  data.get("contactpersoon", "")),
        field_row("Project",         data.get("project", "")),
        field_row("Sortering",       data.get("sortering", "")),
        field_row("Stuks",           data.get("stuks", "")),
        field_row("Gewenste leverdatum", data.get("leverdatum", "")),
    ]

    client_table = Table(client_data, colWidths=[45 * mm, W - 45 * mm])
    client_table.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 0), (0, -1), colors.HexColor("#f0f2f8")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1),
         [colors.white, colors.HexColor("#fafafa")]),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#e8eaed")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",(0, 0), (-1, -1), 6),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0,0), (-1, -1), 4),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 6 * mm))

    # ── Dimensions table ──────────────────────────────────────────────────────
    story.append(Paragraph("AFMETINGEN", section_title))

    dim_headers = [
        Paragraph("<b>Maat</b>", bold),
        Paragraph("<b>Waarde (mm)</b>", bold),
        Paragraph("<b>Omschrijving</b>", bold),
    ]
    dims = [
        ("A", data.get("A", 0), "Breedte voorzijde"),
        ("B", data.get("B", 0), "Totale lengte van de strip"),
        ("C", data.get("C", 0), "Hoogte van de strip"),
        ("D", data.get("D", 0), "Diepte van de strip"),
        ("X", data.get("X", 0), "Zaagsnede positie (afkorting)"),
    ]

    dim_rows = [dim_headers]
    for lbl, val, desc in dims:
        style = bold if lbl == "X" else normal
        colour = colors.HexColor("#fce8e6") if lbl == "X" else colors.white
        row = [
            Paragraph(f"<b>{lbl}</b>", bold),
            Paragraph(str(int(val)), style),
            Paragraph(desc, normal),
        ]
        dim_rows.append(row)

    dim_table = Table(dim_rows,
                      colWidths=[15 * mm, 30 * mm, W - 45 * mm])
    dim_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), DEKO_DARK),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#fafafa")]),
        ("BACKGROUND",   (0, 5), (-1, 5), colors.HexColor("#fce8e6")),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#e8eaed")),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("ALIGN",        (1, 0), (1, -1), "CENTER"),
    ]))
    story.append(dim_table)
    story.append(Spacer(1, 6 * mm))

    # ── Diagram ───────────────────────────────────────────────────────────────
    story.append(Paragraph("SCHEMATISCHE WEERGAVE", section_title))
    story.append(
        _strip_diagram_drawing(
            data.get("A", 210), data.get("B", 1000),
            data.get("C", 65),  data.get("D", 22),
            data.get("X", 300), width=W,
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "* In geval van afkorten: de X-maat geeft de positie van de zaagsnede "
        "aan (afstand van het kortste uiteinde). "
        "Het rode gedeelte is de benodigde strip, het grijze gedeelte is het restant.",
        small,
    ))
    story.append(Spacer(1, 6 * mm))

    # ── Derived info ──────────────────────────────────────────────────────────
    B_val = data.get("B", 0)
    X_val = data.get("X", 0)
    rest  = max(B_val - X_val, 0)

    summary_data = [
        [Paragraph("<b>Benodigd stuk</b>", bold),
         Paragraph(f"{int(X_val)} mm", normal)],
        [Paragraph("<b>Restant</b>", bold),
         Paragraph(f"{int(rest)} mm", normal)],
    ]
    sum_table = Table(summary_data, colWidths=[45 * mm, W - 45 * mm])
    sum_table.setStyle(TableStyle([
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#bbf7d0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",(0, 0), (-1, -1), 6),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0,0), (-1, -1), 4),
    ]))
    story.append(sum_table)
    story.append(Spacer(1, 6 * mm))

    # ── Opmerkingen ───────────────────────────────────────────────────────────
    if data.get("opmerkingen"):
        story.append(Paragraph("OPMERKINGEN", section_title))
        story.append(Paragraph(data["opmerkingen"], normal))
        story.append(Spacer(1, 5 * mm))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width=W, thickness=0.5, color=DEKO_GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "Deko B.V.  |  Peppelenbos 16, 6662 WB Elst (Gld)  |  "
        "T +31 (0) 481 – 366 466  |  sales@deko.nu",
        ParagraphStyle("footer", fontName="Helvetica", fontSize=7,
                       textColor=DEKO_GREY, alignment=TA_CENTER),
    ))

    doc.build(story)
    return buf.getvalue()

