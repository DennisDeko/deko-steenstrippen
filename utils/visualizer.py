"""
utils/visualizer.py
Draws an isometric-style 3D diagram of the afgekorte steenstrip,
matching the style of the Deko B.V. order form.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import to_rgba


# ── Isometric projection helpers ───────────────────────────────────────────────

def iso(x, y, z, scale_x=1.0, scale_y=1.0):
    """Convert 3-D (x,y,z) → 2-D isometric screen coordinates."""
    sx = (x - y) * np.cos(np.radians(30)) * scale_x
    sy = (x + y) * np.sin(np.radians(30)) * scale_y + z
    return sx, sy


def iso_face(pts, scale_x=1.0, scale_y=1.0):
    """Convert list of (x,y,z) to array of 2-D iso coords."""
    xs, ys = zip(*[iso(p[0], p[1], p[2], scale_x, scale_y) for p in pts])
    return list(zip(xs, ys))


# ── Arrow / dimension annotation helper ───────────────────────────────────────

def dim_arrow(ax, p1, p2, label, color="#1a1a2e", fontsize=9,
              offset=(0, 6), xycoords="data"):
    """Draw a dimension arrow between two 2-D points with a label."""
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.3))
    mx = (p1[0] + p2[0]) / 2 + offset[0]
    my = (p1[1] + p2[1]) / 2 + offset[1]
    ax.text(mx, my, label, ha="center", va="center", fontsize=fontsize,
            fontweight="bold", color=color,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color,
                      lw=0.8, alpha=0.9))


# ── Main drawing function ──────────────────────────────────────────────────────

def draw_strip_diagram(A: float, B: float, C: float, D: float, X: float):
    """
    Draw an isometric-perspective brick strip diagram.

    Dimension convention (matching Deko form):
      A = front face width  (x-direction)
      B = total length       (y-direction, depth going back)
      C = strip height       (z-direction, vertical)
      D = strip thickness    (used as the real cross-section depth label)
      X = cut position from left end

    Returns a matplotlib Figure.
    """
    # ── Normalise inputs (guard against zeros) ────────────────────────────────
    A  = max(A,  1)
    B  = max(B,  1)
    C  = max(C,  1)
    D  = max(D,  1)
    X  = min(max(X, 0), B)   # clamp [0, B]

    # ── Scale factors for nicer aspect ratio ──────────────────────────────────
    # Map real mm to "drawing units" so the figure always looks balanced.
    ref = max(A, B, C, D)
    sx  = 6.0 / ref   # scale x (width A)
    sy  = 3.5 / ref   # scale y (depth B)
    sz  = 4.0 / ref   # scale z (height C)

    # Geometry in normalised units
    aw = A * sx
    bl = B * sy
    ch = C * sz
    xw = X * sy   # X mapped to y-scale

    # ── Figure setup ──────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#f8f9fb")
    ax.set_facecolor("#f8f9fb")

    # ── iso shortcut with our scales ──────────────────────────────────────────
    def i(x, y, z):
        return iso(x, y, z, scale_x=1.0, scale_y=1.0)

    # ── 8 corners of the full box ──────────────────────────────────────────────
    # (x=A-width, y=B-length, z=C-height)
    #  Front-bottom-left=origin
    corners = {
        "FBL": (0,   0,  0),
        "FBR": (aw,  0,  0),
        "FTL": (0,   0,  ch),
        "FTR": (aw,  0,  ch),
        "BBL": (0,   bl, 0),
        "BBR": (aw,  bl, 0),
        "BTL": (0,   bl, ch),
        "BTR": (aw,  bl, ch),
    }
    c = {k: i(*v) for k, v in corners.items()}

    # ── Cut plane corners (at y = xw) ─────────────────────────────────────────
    cut = {
        "CBL": (0,   xw, 0),
        "CBR": (aw,  xw, 0),
        "CTL": (0,   xw, ch),
        "CTR": (aw,  xw, ch),
    }
    k = {kk: i(*vv) for kk, vv in cut.items()}

    # ── Helper to draw a filled face ──────────────────────────────────────────
    def face(pts_2d, facecolor, edgecolor="#1a1a2e", lw=1.2, alpha=1.0, zorder=1):
        from matplotlib.patches import Polygon
        poly = Polygon(pts_2d, closed=True, facecolor=facecolor,
                       edgecolor=edgecolor, lw=lw, alpha=alpha, zorder=zorder)
        ax.add_patch(poly)

    # ── RESTANT (grey, back part B → X) ───────────────────────────────────────
    restant_front = [k["CBL"], k["CBR"], k["CTR"], k["CTL"]]
    restant_top   = [k["CTL"], k["CTR"], c["BTR"], c["BTL"]]
    restant_side  = [k["CBR"], c["BBR"], c["BTR"], k["CTR"]]

    face(restant_top,   "#d1d5db", "#6b7280", lw=0.8, alpha=0.6, zorder=2)
    face(restant_side,  "#9ca3af", "#6b7280", lw=0.8, alpha=0.6, zorder=2)
    face(restant_front, "#e5e7eb", "#6b7280", lw=0.8, alpha=0.6, zorder=3)

    # ── BENODIGD (red, front part 0 → X) ──────────────────────────────────────
    needed_bottom = [c["FBL"], c["FBR"], k["CBR"], k["CBL"]]
    needed_front  = [c["FBL"], c["FBR"], c["FTR"], c["FTL"]]
    needed_top    = [c["FTL"], c["FTR"], k["CTR"], k["CTL"]]
    needed_side   = [c["FBR"], k["CBR"], k["CTR"], c["FTR"]]

    DEKO_RED   = "#c0392b"
    DEKO_DARK  = "#922b21"
    DEKO_LIGHT = "#e74c3c"

    face(needed_bottom, DEKO_DARK,  DEKO_DARK,  lw=1.2, zorder=4)
    face(needed_top,    DEKO_LIGHT, DEKO_DARK,  lw=1.2, zorder=5)
    face(needed_side,   DEKO_DARK,  DEKO_DARK,  lw=1.2, zorder=5)
    face(needed_front,  DEKO_RED,   "#1a1a2e",  lw=1.5, zorder=6)

    # ── Cut face (lighter red) ─────────────────────────────────────────────────
    cut_face = [k["CBL"], k["CBR"], k["CTR"], k["CTL"]]
    face(cut_face, "#fadbd8", DEKO_RED, lw=2.0, zorder=7)

    # ── Dashed cut line (vertical at x=xw) ────────────────────────────────────
    x_cut_vals = [c[0] for c in [k["CTL"], k["CTR"]]]
    y_cut_vals = [c[1] for c in [k["CTL"], k["CTR"]]]
    ax.plot(x_cut_vals, y_cut_vals, "--", color=DEKO_RED, lw=1.5,
            zorder=8, dashes=(5, 3))

    # ── Saw blade icon (simple circle with tick marks) ────────────────────────
    saw_cx = (k["CTL"][0] + k["CTR"][0]) / 2
    saw_cy = (k["CTL"][1] + k["CTR"][1]) / 2 + 0.55
    saw_r  = 0.35
    circle = plt.Circle((saw_cx, saw_cy), saw_r,
                         facecolor="#9ca3af", edgecolor="#374151",
                         lw=1.5, zorder=9, alpha=0.9)
    ax.add_patch(circle)
    # Teeth around the blade
    for ang in np.linspace(0, 360, 18, endpoint=False):
        rad  = np.radians(ang)
        tx   = saw_cx + saw_r * np.cos(rad)
        ty   = saw_cy + saw_r * np.sin(rad)
        tx2  = saw_cx + (saw_r + 0.1) * np.cos(rad)
        ty2  = saw_cy + (saw_r + 0.1) * np.sin(rad)
        ax.plot([tx, tx2], [ty, ty2], color="#374151", lw=1.2, zorder=10)
    # Blade centre
    ax.plot(saw_cx, saw_cy, "o", color="#374151", ms=4, zorder=11)

    # ── DIMENSION ANNOTATIONS ──────────────────────────────────────────────────
    # A – breedte (front bottom edge)
    pA1 = c["FBL"]
    pA2 = c["FBR"]
    dim_arrow(ax, (pA1[0], pA1[1] - 0.35), (pA2[0], pA2[1] - 0.35),
              f"A = {int(A)} mm", color="#1a1a2e", offset=(0, -0.22))

    # B – totale lengte (bottom right edge, going back)
    pB1 = c["FBR"]
    pB2 = c["BBR"]
    boff = 0.42
    dim_arrow(ax, (pB1[0] + boff, pB1[1] - 0.18),
              (pB2[0] + boff, pB2[1] - 0.18),
              f"B = {int(B)} mm", color="#374151", offset=(0.3, 0))

    # C – hoogte (right face, vertical)
    pC1 = c["FBR"]
    pC2 = c["FTR"]
    dim_arrow(ax, (pC1[0] + 0.35, pC1[1]),
              (pC2[0] + 0.35, pC2[1]),
              f"C = {int(C)} mm", color="#374151", offset=(0.42, 0))

    # D – label on the left face, just text (diepte label shown on left side)
    d_mid = ((c["FBL"][0] + c["BBL"][0]) / 2 - 0.5,
             (c["FBL"][1] + c["BBL"][1]) / 2)
    ax.text(d_mid[0], d_mid[1], f"D = {int(D)} mm",
            ha="right", va="center", fontsize=9, fontweight="bold",
            color="#374151",
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec="#374151", lw=0.8, alpha=0.9))

    # X – cut position (front bottom to cut bottom)
    pX1 = c["FBL"]
    pX2 = k["CBL"]
    dim_arrow(ax, (pX1[0] - 0.45, pX1[1]),
              (pX2[0] - 0.45, pX2[1]),
              f"X = {int(X)} mm", color=DEKO_RED, offset=(-0.52, 0))

    # ── Legend ────────────────────────────────────────────────────────────────
    leg_x = ax.get_xlim()[1] if ax.get_xlim()[1] != 0 else 3
    patches = [
        mpatches.Patch(facecolor=DEKO_RED,  edgecolor="#1a1a2e", label="Benodigde strip"),
        mpatches.Patch(facecolor="#d1d5db", edgecolor="#6b7280", label="Restant"),
    ]
    ax.legend(handles=patches, loc="lower right", fontsize=8.5,
              framealpha=0.9, edgecolor="#d1d5db")

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.set_title("Steenstrippen – Afgekorte strip",
                 fontsize=11, fontweight="bold", color="#1a1a2e",
                 pad=10, loc="left")

    ax.autoscale_view()
    fig.tight_layout()
    return fig
