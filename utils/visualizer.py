"""
utils/visualizer.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon


def iso(x, y, z):
    sx = (x - y) * np.cos(np.radians(30))
    sy = (x + y) * np.sin(np.radians(30)) + z
    return np.array([sx, sy])


def face(ax, pts3d, fc, ec="#222222", lw=1.1, alpha=1.0, zorder=1):
    pts2d = [iso(p[0], p[1], p[2]) for p in pts3d]
    poly = Polygon(pts2d, closed=True, facecolor=fc,
                   edgecolor=ec, linewidth=lw, alpha=alpha, zorder=zorder)
    ax.add_patch(poly)
    return pts2d


def dim_arrow(ax, p1_3d, p2_3d, label, color="#1a1a2e",
              perp=(0, 0), fontsize=8.5, zorder=15):
    p1 = iso(*p1_3d) + np.array(perp)
    p2 = iso(*p2_3d) + np.array(perp)
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="<->", color=color,
                                lw=1.4, mutation_scale=10),
                zorder=zorder)
    mid = (p1 + p2) / 2
    ax.text(mid[0], mid[1], label,
            ha="center", va="center", fontsize=fontsize,
            fontweight="bold", color=color, zorder=zorder + 1,
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec=color, lw=0.8, alpha=0.95))


def draw_saw(ax, p_tl, p_tr, zorder=21):
    """Teken een zaagblad boven het snijvlak."""
    saw_center = (p_tl + p_tr) / 2 + np.array([0, 0.9])
    saw_r = 0.45
    circle = plt.Circle(saw_center, saw_r,
                        facecolor="#95a5a6", edgecolor="#2c3e50",
                        lw=1.5, zorder=zorder, alpha=0.92)
    ax.add_patch(circle)
    for ang in np.linspace(0, 360, 20, endpoint=False):
        r  = np.radians(ang)
        t1 = saw_center + saw_r         * np.array([np.cos(r), np.sin(r)])
        t2 = saw_center + (saw_r + 0.12)* np.array([np.cos(r), np.sin(r)])
        ax.plot([t1[0], t2[0]], [t1[1], t2[1]],
                color="#2c3e50", lw=1.2, zorder=zorder + 1)
    ax.plot(*saw_center, "o", color="#2c3e50", ms=4, zorder=zorder + 2)
    cut_mid = (p_tl + p_tr) / 2
    ax.annotate("", xy=cut_mid, xytext=saw_center,
                arrowprops=dict(arrowstyle="-|>", color="#2c3e50",
                                lw=1.2, mutation_scale=10),
                zorder=zorder + 2)


def draw_cut_face(ax, xw, aw, ch, RED_FRONT, zorder_base=8):
    """Teken snijvlak + alle randlijnen op positie y=xw."""
    CUT_FACE = "#f5b7b1"
    face(ax, [(0,xw,0),(aw,xw,0),(aw,xw,ch),(0,xw,ch)],
         CUT_FACE, ec="none", lw=0, zorder=zorder_base)

    p_bl = iso(0,  xw, 0)
    p_br = iso(aw, xw, 0)
    p_tl = iso(0,  xw, ch)
    p_tr = iso(aw, xw, ch)

    ax.plot([p_bl[0], p_tl[0]], [p_bl[1], p_tl[1]],
            color="#1a1a2e", lw=1.8, zorder=20)
    ax.plot([p_br[0], p_tr[0]], [p_br[1], p_tr[1]],
            color="#1a1a2e", lw=1.8, zorder=20)
    ax.plot([p_bl[0], p_br[0]], [p_bl[1], p_br[1]],
            color="#1a1a2e", lw=1.8, zorder=20)
    ax.plot([p_tl[0], p_tr[0]], [p_tl[1], p_tr[1]],
            "--", color=RED_FRONT, lw=1.8, dashes=(5, 3), zorder=20)

    return p_tl, p_tr


def draw_strip_diagram(A: float, B: float, C: float, D: float,
                       X: float, Y: float = 0):
    """
    Teken isometrisch 3D diagram met X-snede (voorkant) en Y-snede (achterkant).

      X = afstand zaagsnede vanaf voorkant
      Y = afstand zaagsnede vanaf achterkant (0 = geen Y-snede)

    Benodigde stuk = van X tot (B - Y)
    """
    A = max(A, 1);  B = max(B, 1)
    C = max(C, 1);  D = max(D, 1)
    Y = max(Y, 0)
    X = min(max(X, 1), B - 1)
    if Y > 0:
        Y = min(Y, B - X - 1)

    ref   = max(A, B, C)
    scale = 7.0 / ref
    aw = A * scale
    bl = B * scale
    ch = C * scale
    xw = X * scale
    yw = (B - Y) * scale   # positie Y-snede vanuit voorkant

    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#f0f3f8")
    ax.set_facecolor("#f0f3f8")

    RED_FRONT = "#c0392b"
    RED_TOP   = "#e74c3c"
    RED_SIDE  = "#922b21"
    GRY_FRONT = "#bdc3c7"
    GRY_TOP   = "#d5d8dc"
    GRY_SIDE  = "#99a3a4"

    # ── RESTANT VOOR (van 0 tot xw) ───────────────────────────────────────
    face(ax, [(0,0,0),(aw,0,0),(aw,xw,0),(0,xw,0)],
         GRY_SIDE,  ec="#7f8c8d", lw=0.8, alpha=0.5, zorder=1)
    face(ax, [(0,0,0),(0,xw,0),(0,xw,ch),(0,0,ch)],
         GRY_FRONT, ec="#7f8c8d", lw=0.8, alpha=0.5, zorder=2)
    face(ax, [(aw,0,0),(aw,xw,0),(aw,xw,ch),(aw,0,ch)],
         GRY_SIDE,  ec="#7f8c8d", lw=0.8, alpha=0.7, zorder=2)
    face(ax, [(0,0,ch),(aw,0,ch),(aw,xw,ch),(0,xw,ch)],
         GRY_TOP,   ec="#7f8c8d", lw=0.9, alpha=0.85, zorder=3)
    face(ax, [(0,0,0),(aw,0,0),(aw,0,ch),(0,0,ch)],
         GRY_FRONT, ec="#7f8c8d", lw=0.8, alpha=0.6, zorder=3)  # voorkant

    # ── RESTANT ACHTER (van yw tot bl) — alleen als Y > 0 ─────────────────
    if Y > 0:
        face(ax, [(0,yw,0),(aw,yw,0),(aw,bl,0),(0,bl,0)],
             GRY_SIDE,  ec="#7f8c8d", lw=0.8, alpha=0.5, zorder=1)
        face(ax, [(0,bl,0),(aw,bl,0),(aw,bl,ch),(0,bl,ch)],
             GRY_FRONT, ec="#7f8c8d", lw=0.8, alpha=0.4, zorder=1)
        face(ax, [(0,yw,0),(0,bl,0),(0,bl,ch),(0,yw,ch)],
             GRY_FRONT, ec="#7f8c8d", lw=0.8, alpha=0.5, zorder=2)
        face(ax, [(aw,yw,0),(aw,bl,0),(aw,bl,ch),(aw,yw,ch)],
             GRY_SIDE,  ec="#7f8c8d", lw=0.8, alpha=0.7, zorder=2)
        face(ax, [(0,yw,ch),(aw,yw,ch),(aw,bl,ch),(0,bl,ch)],
             GRY_TOP,   ec="#7f8c8d", lw=0.9, alpha=0.85, zorder=3)
    else:
        # Geen Y-snede: restant loopt door tot achterkant
        face(ax, [(0,xw,0),(aw,xw,0),(aw,bl,0),(0,bl,0)],
             GRY_SIDE,  ec="#7f8c8d", lw=0.8, alpha=0.5, zorder=1)
        face(ax, [(0,bl,0),(aw,bl,0),(aw,bl,ch),(0,bl,ch)],
             GRY_FRONT, ec="#7f8c8d", lw=0.8, alpha=0.4, zorder=1)
        face(ax, [(0,xw,0),(0,bl,0),(0,bl,ch),(0,xw,ch)],
             GRY_FRONT, ec="#7f8c8d", lw=0.8, alpha=0.5, zorder=2)
        face(ax, [(aw,xw,0),(aw,bl,0),(aw,bl,ch),(aw,xw,ch)],
             GRY_SIDE,  ec="#7f8c8d", lw=0.8, alpha=0.7, zorder=2)
        face(ax, [(0,xw,ch),(aw,xw,ch),(aw,bl,ch),(0,bl,ch)],
             GRY_TOP,   ec="#7f8c8d", lw=0.9, alpha=0.85, zorder=3)

    # ── BENODIGDE block (van xw tot yw of bl) ─────────────────────────────
    eind = yw if Y > 0 else bl
    face(ax, [(0,xw,0),(aw,xw,0),(aw,eind,0),(0,eind,0)],
         RED_SIDE,  ec="#1a1a2e", lw=1.1, zorder=4)
    face(ax, [(0,xw,0),(0,eind,0),(0,eind,ch),(0,xw,ch)],
         RED_SIDE,  ec="#1a1a2e", lw=1.1, zorder=5)
    face(ax, [(aw,xw,0),(aw,eind,0),(aw,eind,ch),(aw,xw,ch)],
         RED_SIDE,  ec="#1a1a2e", lw=1.1, zorder=5)
    face(ax, [(0,xw,ch),(aw,xw,ch),(aw,eind,ch),(0,eind,ch)],
         RED_TOP,   ec="#1a1a2e", lw=1.1, zorder=6)

    # ── X snijvlak ────────────────────────────────────────────────────────
    p_tl_x, p_tr_x = draw_cut_face(ax, xw, aw, ch, RED_FRONT, zorder_base=8)
    draw_saw(ax, p_tl_x, p_tr_x, zorder=21)

    # ── Y snijvlak (alleen als Y > 0) ─────────────────────────────────────
    if Y > 0:
        p_tl_y, p_tr_y = draw_cut_face(ax, yw, aw, ch, "#e67e22", zorder_base=9)
        draw_saw(ax, p_tl_y, p_tr_y, zorder=25)

    # ── MATEN ─────────────────────────────────────────────────────────────

    # A – breedte
    dim_arrow(ax, (0,0,0), (aw,0,0),
              f"A = {int(A)} mm", color="#1a1a2e", perp=(0, -0.55))

    # B – volledige lengte
    dim_arrow(ax, (aw,0,0), (aw,bl,0),
              f"B = {int(B)} mm", color="#374151", perp=(1.0, -0.5))
    p_front_r = iso(aw, 0,  0)
    p_back_r  = iso(aw, bl, 0)
    ax.plot([p_front_r[0], p_front_r[0] + 1.0],
            [p_front_r[1], p_front_r[1] - 0.5],
            ":", color="#374151", lw=1.0, zorder=14)
    ax.plot([p_back_r[0],  p_back_r[0]  + 1.0],
            [p_back_r[1],  p_back_r[1]  - 0.5],
            ":", color="#374151", lw=1.0, zorder=14)

    # X – zaagsnede voorkant
    dim_arrow(ax, (0,0,0), (0,xw,0),
              f"X = {int(X)} mm", color=RED_FRONT, perp=(-0.7, -0.35))

    # Y – zaagsnede achterkant
    if Y > 0:
        dim_arrow(ax, (0,yw,0), (0,bl,0),
                  f"Y = {int(Y)} mm", color="#e67e22", perp=(-0.7, -0.35))

    # C – hoogte
    p_br  = iso(aw, 0, 0)
    p_tr2 = iso(aw, 0, ch)
    off   = np.array([0.5, 0])
    ax.annotate("", xy=p_tr2 + off, xytext=p_br + off,
                arrowprops=dict(arrowstyle="<->", color="#374151",
                                lw=1.3, mutation_scale=10), zorder=15)
    mid_c = (p_br + p_tr2) / 2 + off + np.array([0.45, 0])
    ax.text(mid_c[0], mid_c[1], f"C = {int(C)} mm",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color="#374151", zorder=16,
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec="#374151", lw=0.8, alpha=0.95))

    # D – diepte
    p_dl = iso(0, bl * 0.6, ch * 0.5)
    ax.text(p_dl[0] - 0.5, p_dl[1], f"D = {int(D)} mm",
            ha="right", va="center", fontsize=8.5, fontweight="bold",
            color="#374151", zorder=16,
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec="#374151", lw=0.8, alpha=0.95))

    # ── LEGENDA ───────────────────────────────────────────────────────────
    patches = [
        mpatches.Patch(facecolor=RED_FRONT,  edgecolor="#1a1a2e", label="Benodigde strip"),
        mpatches.Patch(facecolor=GRY_TOP,    edgecolor="#7f8c8d", label="Restant"),
    ]
    if Y > 0:
        patches.append(
            mpatches.Patch(facecolor="#f5b7b1", edgecolor="#e67e22",
                           label="Y-snijvlak")
        )
    ax.legend(handles=patches, loc="lower right", fontsize=9,
              framealpha=0.95, edgecolor="#d1d5db",
              bbox_to_anchor=(0.98, 0.02))

    ax.set_title("Steenstrippen – Afgekorte strip",
                 fontsize=11, fontweight="bold", color="#1a1a2e",
                 loc="left", pad=10)

    ax.autoscale_view()
    xl = ax.get_xlim(); yl = ax.get_ylim()
    ax.set_xlim(xl[0] - 1.5, xl[1] + 2.8)
    ax.set_ylim(yl[0] - 1.0, yl[1] + 1.8)

    fig.tight_layout(pad=0.5)
    return fig
