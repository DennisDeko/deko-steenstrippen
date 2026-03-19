"""
utils/visualizer.py
Draws an isometric-style 3D diagram of the afgekorte steenstrip.
Both the 'benodigde' and 'restant' parts are full 3D blocks.
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


def draw_strip_diagram(A: float, B: float, C: float, D: float, X: float):
    A = max(A, 1);  B = max(B, 1)
    C = max(C, 1);  D = max(D, 1)
    X = min(max(X, 1), B - 1)

    ref = max(A, B, C)
    aw  = A / ref * 4.0
    bl  = B / ref * 7.0
    ch  = C / ref * 3.5
    xw  = X / B * bl

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
    CUT_FACE  = "#f5b7b1"

    # RESTANT block (back part: y from xw to bl)
    face(ax, [(0,xw,0),(aw,xw,0),(aw,bl,0),(0,bl,0)],
         GRY_SIDE,  ec="#7f8c8d", lw=0.8, alpha=0.5, zorder=2)
    face(ax, [(0,xw,ch),(aw,xw,ch),(aw,bl,ch),(0,bl,ch)],
         GRY_TOP,   ec="#7f8c8d", lw=0.9, alpha=0.85, zorder=3)
    face(ax, [(aw,xw,0),(aw,bl,0),(aw,bl,ch),(aw,xw,ch)],
         GRY_SIDE,  ec="#7f8c8d", lw=0.8, alpha=0.7, zorder=3)
    face(ax, [(0,xw,0),(0,bl,0),(0,bl,ch),(0,xw,ch)],
         GRY_FRONT, ec="#7f8c8d", lw=0.8, alpha=0.5, zorder=3)
    face(ax, [(0,bl,0),(aw,bl,0),(aw,bl,ch),(0,bl,ch)],
         GRY_FRONT, ec="#7f8c8d", lw=0.8, alpha=0.4, zorder=2)

    # BENODIGDE block (front part: y from 0 to xw)
    face(ax, [(0,0,0),(aw,0,0),(aw,xw,0),(0,xw,0)],
         RED_SIDE,  ec="#1a1a2e", lw=1.1, zorder=4)
    face(ax, [(0,0,ch),(aw,0,ch),(aw,xw,ch),(0,xw,ch)],
         RED_TOP,   ec="#1a1a2e", lw=1.1, zorder=5)
    face(ax, [(aw,0,0),(aw,xw,0),(aw,xw,ch),(aw,0,ch)],
         RED_SIDE,  ec="#1a1a2e", lw=1.1, zorder=5)
    face(ax, [(0,0,0),(aw,0,0),(aw,0,ch),(0,0,ch)],
         RED_FRONT, ec="#1a1a2e", lw=1.5, zorder=6)

    # Cut face
    face(ax, [(0,xw,0),(aw,xw,0),(aw,xw,ch),(0,xw,ch)],
         CUT_FACE, ec=RED_FRONT, lw=2.0, zorder=7)

    # Dashed cut line
    p_tl = iso(0,  xw, ch)
    p_tr = iso(aw, xw, ch)
    ax.plot([p_tl[0], p_tr[0]], [p_tl[1], p_tr[1]],
            "--", color=RED_FRONT, lw=1.8, dashes=(5, 3), zorder=8)

    # Saw blade
    saw_center = (p_tl + p_tr) / 2 + np.array([0, 0.9])
    saw_r = 0.55
    circle = plt.Circle(saw_center, saw_r,
                        facecolor="#95a5a6", edgecolor="#2c3e50",
                        lw=1.5, zorder=9, alpha=0.92)
    ax.add_patch(circle)
    for ang in np.linspace(0, 360, 20, endpoint=False):
        r = np.radians(ang)
        t1 = saw_center + saw_r        * np.array([np.cos(r), np.sin(r)])
        t2 = saw_center + (saw_r+0.14) * np.array([np.cos(r), np.sin(r)])
        ax.plot([t1[0], t2[0]], [t1[1], t2[1]], color="#2c3e50", lw=1.3, zorder=10)
    ax.plot(*saw_center, "o", color="#2c3e50", ms=5, zorder=11)
    cut_mid = (p_tl + p_tr) / 2
    ax.annotate("", xy=cut_mid, xytext=saw_center,
                arrowprops=dict(arrowstyle="-|>", color="#2c3e50",
                                lw=1.2, mutation_scale=10), zorder=12)

    # DIMENSIONS
    dim_arrow(ax, (0,0,0), (aw,0,0),
              f"A = {int(A)} mm", color="#1a1a2e", perp=(0, -0.6))
    dim_arrow(ax, (aw,0,0), (aw,bl,0),
              f"B = {int(B)} mm", color="#374151", perp=(0.7, -0.35))
    dim_arrow(ax, (0,0,0), (0,xw,0),
              f"X = {int(X)} mm", color=RED_FRONT, perp=(-0.7, -0.35))

    p_br  = iso(aw, 0, 0)
    p_tr2 = iso(aw, 0, ch)
    off = np.array([0.55, 0])
    ax.annotate("", xy=p_tr2 + off, xytext=p_br + off,
                arrowprops=dict(arrowstyle="<->", color="#374151",
                                lw=1.3, mutation_scale=10), zorder=15)
    mid_c = (p_br + p_tr2) / 2 + off + np.array([0.5, 0])
    ax.text(mid_c[0], mid_c[1], f"C = {int(C)} mm",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color="#374151", zorder=16,
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec="#374151", lw=0.8, alpha=0.95))

    p_dl = iso(0, bl * 0.6, ch * 0.5)
    ax.text(p_dl[0] - 0.5, p_dl[1], f"D = {int(D)} mm",
            ha="right", va="center", fontsize=8.5, fontweight="bold",
            color="#374151", zorder=16,
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec="#374151", lw=0.8, alpha=0.95))

    # LEGEND
    patches = [
        mpatches.Patch(facecolor=RED_FRONT, edgecolor="#1a1a2e", label="Benodigde strip"),
        mpatches.Patch(facecolor=GRY_TOP,   edgecolor="#7f8c8d", label="Restant"),
    ]
    ax.legend(handles=patches, loc="lower right", fontsize=9,
              framealpha=0.95, edgecolor="#d1d5db",
              bbox_to_anchor=(0.98, 0.02))

    ax.set_title("Steenstrippen – Afgekorte strip",
                 fontsize=11, fontweight="bold", color="#1a1a2e",
                 loc="left", pad=10)

    ax.autoscale_view()
    xl = ax.get_xlim(); yl = ax.get_ylim()
    ax.set_xlim(xl[0] - 1.5, xl[1] + 2.2)
    ax.set_ylim(yl[0] - 1.0, yl[1] + 1.8)

    fig.tight_layout(pad=0.5)
    return fig
