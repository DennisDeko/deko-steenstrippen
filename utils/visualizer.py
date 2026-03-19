"""
utils/visualizer.py
X = snede langs de LENGTE (horizontaal)
Y = snede langs de HOOGTE (verticaal)
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


def draw_saw_x(ax, xw, aw, ch, zorder=21):
    p_tl = iso(0,  xw, ch)
    p_tr = iso(aw, xw, ch)
    saw_c = (p_tl + p_tr) / 2 + np.array([0, 0.8])
    r = 0.38
    ax.add_patch(plt.Circle(saw_c, r, facecolor="#95a5a6",
                            edgecolor="#2c3e50", lw=1.4, zorder=zorder, alpha=0.92))
    for ang in np.linspace(0, 360, 18, endpoint=False):
        a = np.radians(ang)
        t1 = saw_c + r        * np.array([np.cos(a), np.sin(a)])
        t2 = saw_c + (r+0.10) * np.array([np.cos(a), np.sin(a)])
        ax.plot([t1[0], t2[0]], [t1[1], t2[1]], color="#2c3e50", lw=1.1, zorder=zorder+1)
    ax.plot(*saw_c, "o", color="#2c3e50", ms=3.5, zorder=zorder+2)
    mid = (p_tl + p_tr) / 2
    ax.annotate("", xy=mid, xytext=saw_c,
                arrowprops=dict(arrowstyle="-|>", color="#2c3e50",
                                lw=1.1, mutation_scale=9), zorder=zorder+2)


def draw_saw_y(ax, yw, bl, aw, zorder=25):
    p1 = iso(aw, 0,  yw)
    p2 = iso(aw, bl, yw)
    saw_c = (p1 + p2) / 2 + np.array([0.7, 0])
    r = 0.38
    ax.add_patch(plt.Circle(saw_c, r, facecolor="#d7bde2",
                            edgecolor="#8e44ad", lw=1.4, zorder=zorder, alpha=0.92))
    for ang in np.linspace(0, 360, 18, endpoint=False):
        a = np.radians(ang)
        t1 = saw_c + r        * np.array([np.cos(a), np.sin(a)])
        t2 = saw_c + (r+0.10) * np.array([np.cos(a), np.sin(a)])
        ax.plot([t1[0], t2[0]], [t1[1], t2[1]], color="#8e44ad", lw=1.1, zorder=zorder+1)
    ax.plot(*saw_c, "o", color="#8e44ad", ms=3.5, zorder=zorder+2)
    mid = (p1 + p2) / 2
    ax.annotate("", xy=mid, xytext=saw_c,
                arrowprops=dict(arrowstyle="-|>", color="#8e44ad",
                                lw=1.1, mutation_scale=9), zorder=zorder+2)


def dim_arrow(ax, p1_2d, p2_2d, label, color="#1a1a2e", fontsize=8.0, zorder=15):
    ax.annotate("", xy=p2_2d, xytext=p1_2d,
                arrowprops=dict(arrowstyle="<->", color=color,
                                lw=1.3, mutation_scale=10), zorder=zorder)
    mid = ((p1_2d[0]+p2_2d[0])/2, (p1_2d[1]+p2_2d[1])/2)
    ax.text(mid[0], mid[1], label, ha="center", va="center",
            fontsize=fontsize, fontweight="bold", color=color, zorder=zorder+1,
            bbox=dict(boxstyle="round,pad=0.2", fc="white",
                      ec=color, lw=0.7, alpha=0.95))


def draw_strip_diagram(A, B, C, D, x_cuts=None, y_cuts=None):
    """
    A = breedte, B = lengte, C = hoogte, D = diepte (label)
    x_cuts = lijst van snede-posities langs LENGTE (mm vanaf voorkant)
    y_cuts = lijst van snede-posities langs HOOGTE (mm vanaf onderkant)
    """
    # ── Invoer opschonen ──────────────────────────────────────────────────
    A = max(float(A), 1)
    B = max(float(B), 1)
    C = max(float(C), 1)
    D = max(float(D), 1)

    x_cuts = sorted([float(v) for v in (x_cuts or []) if 0 < float(v) < B])
    y_cuts = sorted([float(v) for v in (y_cuts or []) if 0 < float(v) < C])

    # ── Schaling ──────────────────────────────────────────────────────────
    scale = 7.0 / max(A, B, C)
    aw = A * scale
    bl = B * scale
    ch = C * scale

    # Grenzen in tekeningeenheden
    x_bounds_mm = [0.0] + x_cuts + [B]
    y_bounds_mm = [0.0] + y_cuts + [C]
    x_bounds = [v * scale for v in x_bounds_mm]
    y_bounds = [v * scale for v in y_bounds_mm]

    # ── Kleuren ───────────────────────────────────────────────────────────
    RED     = "#c0392b"
    RTOP    = "#e74c3c"
    RSIDE   = "#922b21"
    GREY    = "#bdc3c7"
    GTOP    = "#d5d8dc"
    GSIDE   = "#99a3a4"
    XCUT_C  = "#f5b7b1"
    YCUT_C  = "#d7bde2"

    # ── Bepaal welk segment "benodigd" is ─────────────────────────────────
    # Standaard: eerste X-segment is benodigd (0 → eerste snede)
    # Bij meerdere snedes: tussensegmenten zijn restant
    # Geen snedes: alles benodigd
    def is_needed(xi, yi):
        """xi = index langs lengte, yi = index langs hoogte."""
        x_ok = (xi == 0) if x_cuts else True
        y_ok = (yi == 0) if y_cuts else True
        return x_ok and y_ok

    # ── Figuur ────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#f0f3f8")
    ax.set_facecolor("#f0f3f8")

    # ── Teken blokken per segment ─────────────────────────────────────────
    n_x = len(x_bounds) - 1
    n_y = len(y_bounds) - 1

    for xi in range(n_x):
        yb0 = x_bounds[xi]
        yb1 = x_bounds[xi + 1]
        for yi in range(n_y):
            zb0 = y_bounds[yi]
            zb1 = y_bounds[yi + 1]

            needed = is_needed(xi, yi)
            fc_top   = RTOP  if needed else GTOP
            fc_side  = RSIDE if needed else GSIDE
            fc_front = RED   if needed else GREY
            ec       = "#1a1a2e" if needed else "#7f8c8d"
            lw       = 1.1 if needed else 0.7
            zo       = 4   if needed else 2
            al       = 1.0 if needed else 0.75

            # Bovenkant
            face(ax, [(0,yb0,zb1),(aw,yb0,zb1),(aw,yb1,zb1),(0,yb1,zb1)],
                 fc_top, ec=ec, lw=lw, alpha=al, zorder=zo+1)
            # Rechterkant
            face(ax, [(aw,yb0,zb0),(aw,yb1,zb0),(aw,yb1,zb1),(aw,yb0,zb1)],
                 fc_side, ec=ec, lw=lw, alpha=al, zorder=zo)
            # Voorkant (yi=0 kant, zb0=onderkant)
            if xi == 0:
                face(ax, [(0,yb0,zb0),(aw,yb0,zb0),(aw,yb0,zb1),(0,yb0,zb1)],
                     fc_front, ec=ec, lw=lw+0.2 if needed else lw,
                     alpha=al, zorder=zo+2)
            # Onderkant (alleen onderste rij)
            if yi == 0:
                face(ax, [(0,yb0,zb0),(aw,yb0,zb0),(aw,yb1,zb0),(0,yb1,zb0)],
                     fc_side, ec=ec, lw=lw, alpha=al*0.6, zorder=zo-1)
            # Linkerkant
            face(ax, [(0,yb0,zb0),(0,yb1,zb0),(0,yb1,zb1),(0,yb0,zb1)],
                 fc_front, ec=ec, lw=lw, alpha=al*0.5, zorder=zo-1)
            # Achterkant (laatste X-segment)
            if xi == n_x - 1:
                face(ax, [(0,yb1,zb0),(aw,yb1,zb0),(aw,yb1,zb1),(0,yb1,zb1)],
                     fc_front, ec=ec, lw=lw, alpha=al*0.4, zorder=zo-1)

    # ── X-snijvlakken tekenen ─────────────────────────────────────────────
    for idx, xw_mm in enumerate(x_cuts):
        xw = xw_mm * scale
        # Vlak
        face(ax, [(0,xw,0),(aw,xw,0),(aw,xw,ch),(0,xw,ch)],
             XCUT_C, ec="none", lw=0, zorder=8)
        # Randen
        for zv in y_bounds:
            pl = iso(0,  xw, zv)
            pr = iso(aw, xw, zv)
            ax.plot([pl[0], pr[0]], [pl[1], pr[1]],
                    color="#1a1a2e", lw=1.5, zorder=20)
        for xpos in [0, aw]:
            for k in range(len(y_bounds)-1):
                p1 = iso(xpos, xw, y_bounds[k])
                p2 = iso(xpos, xw, y_bounds[k+1])
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                        color="#1a1a2e", lw=1.5, zorder=20)
        # Stippellijn bovenkant
        tl = iso(0,  xw, ch)
        tr = iso(aw, xw, ch)
        ax.plot([tl[0], tr[0]], [tl[1], tr[1]],
                "--", color=RED, lw=1.5, dashes=(5, 3), zorder=21)
        draw_saw_x(ax, xw, aw, ch, zorder=22+idx)

    # ── Y-snijvlakken tekenen ─────────────────────────────────────────────
    for idx, yw_mm in enumerate(y_cuts):
        yw = yw_mm * scale
        # Vlak
        face(ax, [(0,0,yw),(aw,0,yw),(aw,bl,yw),(0,bl,yw)],
             YCUT_C, ec="none", lw=0, zorder=9)
        # Randen
        for yb in x_bounds:
            pl = iso(0,  yb, yw)
            pr = iso(aw, yb, yw)
            ax.plot([pl[0], pr[0]], [pl[1], pr[1]],
                    color="#8e44ad", lw=1.5, zorder=20)
        for xpos in [0, aw]:
            for k in range(len(x_bounds)-1):
                p1 = iso(xpos, x_bounds[k],   yw)
                p2 = iso(xpos, x_bounds[k+1], yw)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                        color="#8e44ad", lw=1.5, zorder=20)
        draw_saw_y(ax, yw, bl, aw, zorder=26+idx)

    # ── Maatpijlen ────────────────────────────────────────────────────────
    # A
    p1 = iso(0,  0, 0) + np.array([0, -0.55])
    p2 = iso(aw, 0, 0) + np.array([0, -0.55])
    dim_arrow(ax, p1, p2, f"A={int(A)}mm", color="#1a1a2e")

    # B
    p1 = iso(aw, 0,  0) + np.array([1.0, -0.5])
    p2 = iso(aw, bl, 0) + np.array([1.0, -0.5])
    dim_arrow(ax, p1, p2, f"B={int(B)}mm", color="#374151")
    for yb in [0, bl]:
        p = iso(aw, yb, 0)
        ax.plot([p[0], p[0]+1.0], [p[1], p[1]-0.5],
                ":", color="#374151", lw=0.9, zorder=14)

    # C
    p_bot = iso(aw, 0, 0)  + np.array([0.5, 0])
    p_top = iso(aw, 0, ch) + np.array([0.5, 0])
    ax.annotate("", xy=p_top, xytext=p_bot,
                arrowprops=dict(arrowstyle="<->", color="#374151",
                                lw=1.2, mutation_scale=10), zorder=15)
    mc = ((p_bot[0]+p_top[0])/2 + 0.4, (p_bot[1]+p_top[1])/2)
    ax.text(mc[0], mc[1], f"C={int(C)}mm", ha="left", va="center",
            fontsize=8, fontweight="bold", color="#374151", zorder=16,
            bbox=dict(boxstyle="round,pad=0.2", fc="white",
                      ec="#374151", lw=0.7, alpha=0.95))

    # D
    pd = iso(0, bl*0.6, ch*0.5)
    ax.text(pd[0]-0.5, pd[1], f"D={int(D)}mm", ha="right", va="center",
            fontsize=8, fontweight="bold", color="#374151", zorder=16,
            bbox=dict(boxstyle="round,pad=0.2", fc="white",
                      ec="#374151", lw=0.7, alpha=0.95))

    # X-snede labels
    prev_mm = 0.0
    for idx, xv in enumerate(x_cuts):
        p1 = iso(0, prev_mm*scale, 0) + np.array([-0.7 - idx*0.6, -0.35])
        p2 = iso(0, xv*scale,      0) + np.array([-0.7 - idx*0.6, -0.35])
        dim_arrow(ax, p1, p2, f"X{idx+1}={int(xv)}mm", color=RED)
        prev_mm = xv

    # Y-snede labels
    prev_mm = 0.0
    for idx, yv in enumerate(y_cuts):
        p1 = iso(aw, bl, prev_mm*scale) + np.array([0.5 + idx*0.6, 0])
        p2 = iso(aw, bl, yv*scale)      + np.array([0.5 + idx*0.6, 0])
        dim_arrow(ax, p1, p2, f"Y{idx+1}={int(yv)}mm", color="#8e44ad")
        prev_mm = yv

    # ── Legenda ───────────────────────────────────────────────────────────
    patches = [
        mpatches.Patch(facecolor=RED,    edgecolor="#1a1a2e", label="Benodigde strip"),
        mpatches.Patch(facecolor=GTOP,   edgecolor="#7f8c8d", label="Restant"),
    ]
    if x_cuts:
        patches.append(mpatches.Patch(facecolor=XCUT_C, edgecolor=RED,
                                       label="X-snijvlak (lengte)"))
    if y_cuts:
        patches.append(mpatches.Patch(facecolor=YCUT_C, edgecolor="#8e44ad",
                                       label="Y-snijvlak (hoogte)"))
    ax.legend(handles=patches, loc="lower right", fontsize=8.5,
              framealpha=0.95, edgecolor="#d1d5db",
              bbox_to_anchor=(0.98, 0.02))

    ax.set_title("Steenstrippen – Afgekorte strip",
                 fontsize=11, fontweight="bold", color="#1a1a2e",
                 loc="left", pad=10)

    ax.autoscale_view()
    xl = ax.get_xlim(); yl = ax.get_ylim()
    ax.set_xlim(xl[0]-1.8, xl[1]+3.2)
    ax.set_ylim(yl[0]-1.2, yl[1]+1.8)
    fig.tight_layout(pad=0.5)
    return fig
