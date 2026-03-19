"""
utils/visualizer.py
X = snede langs de LENGTE (horizontaal in aanzicht)
Y = snede langs de HOOGTE (verticaal in aanzicht)
Meerdere X en Y snedes mogelijk.
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


def draw_saw_length(ax, xw, aw, ch, color="#2c3e50", zorder=21):
    """Zaagblad boven X-snede (langs lengte)."""
    p_tl = iso(0,  xw, ch)
    p_tr = iso(aw, xw, ch)
    saw_c = (p_tl + p_tr) / 2 + np.array([0, 0.8])
    r = 0.38
    ax.add_patch(plt.Circle(saw_c, r, facecolor="#95a5a6",
                            edgecolor=color, lw=1.4, zorder=zorder, alpha=0.92))
    for ang in np.linspace(0, 360, 18, endpoint=False):
        a = np.radians(ang)
        t1 = saw_c + r       * np.array([np.cos(a), np.sin(a)])
        t2 = saw_c + (r+0.1) * np.array([np.cos(a), np.sin(a)])
        ax.plot([t1[0],t2[0]], [t1[1],t2[1]], color=color, lw=1.1, zorder=zorder+1)
    ax.plot(*saw_c, "o", color=color, ms=3.5, zorder=zorder+2)
    ax.annotate("", xy=(p_tl+p_tr)/2, xytext=saw_c,
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=1.1, mutation_scale=9), zorder=zorder+2)


def draw_saw_height(ax, yw, bl, aw, color="#8e44ad", zorder=25):
    """Zaagblad naast Y-snede (langs hoogte)."""
    p_bl = iso(aw, 0,  yw)
    p_br = iso(aw, bl, yw)
    saw_c = (p_bl + p_br) / 2 + np.array([0.7, 0])
    r = 0.38
    ax.add_patch(plt.Circle(saw_c, r, facecolor="#d7bde2",
                            edgecolor=color, lw=1.4, zorder=zorder, alpha=0.92))
    for ang in np.linspace(0, 360, 18, endpoint=False):
        a = np.radians(ang)
        t1 = saw_c + r       * np.array([np.cos(a), np.sin(a)])
        t2 = saw_c + (r+0.1) * np.array([np.cos(a), np.sin(a)])
        ax.plot([t1[0],t2[0]], [t1[1],t2[1]], color=color, lw=1.1, zorder=zorder+1)
    ax.plot(*saw_c, "o", color=color, ms=3.5, zorder=zorder+2)
    ax.annotate("", xy=(p_bl+p_br)/2, xytext=saw_c,
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=1.1, mutation_scale=9), zorder=zorder+2)


def dim_arrow(ax, p1_3d, p2_3d, label, color="#1a1a2e",
              perp=(0,0), fontsize=8.0, zorder=15):
    p1 = iso(*p1_3d) + np.array(perp)
    p2 = iso(*p2_3d) + np.array(perp)
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="<->", color=color,
                                lw=1.3, mutation_scale=10), zorder=zorder)
    mid = (p1 + p2) / 2
    ax.text(mid[0], mid[1], label, ha="center", va="center",
            fontsize=fontsize, fontweight="bold", color=color, zorder=zorder+1,
            bbox=dict(boxstyle="round,pad=0.2", fc="white",
                      ec=color, lw=0.7, alpha=0.95))


def draw_strip_diagram(A, B, C, D, x_cuts=None, y_cuts=None):
    """
    Parameters
    ----------
    A, B, C, D : float  — afmetingen in mm
    x_cuts     : list[float]  — snede-posities langs de LENGTE (B-as), mm vanaf voorkant
    y_cuts     : list[float]  — snede-posities langs de HOOGTE (C-as), mm vanaf onderkant
    """
    x_cuts = sorted([v for v in (x_cuts or []) if 0 < v < B])
    y_cuts = sorted([v for v in (y_cuts or []) if 0 < v < C])

    A = max(A,1); B = max(B,1); C = max(C,1); D = max(D,1)

    scale = 7.0 / max(A, B, C)
    aw = A * scale
    bl = B * scale
    ch = C * scale
    xs = [v * scale for v in x_cuts]   # X-snede posities in tekeningeenheden
    ys = [v * scale for v in y_cuts]   # Y-snede posities in tekeningeenheden

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#f0f3f8")
    ax.set_facecolor("#f0f3f8")

    RED   = "#c0392b"
    RTOP  = "#e74c3c"
    RSIDE = "#922b21"
    GREY  = "#bdc3c7"
    GTOP  = "#d5d8dc"
    GSIDE = "#99a3a4"
    XCUT  = "#f5b7b1"   # rood snijvlak
    YCUT  = "#d7bde2"   # paars snijvlak

    # ── Bepaal segmenten langs lengte (X-snedes) ──────────────────────────
    x_bounds = [0] + xs + [bl]
    # Segmenten langs hoogte (Y-snedes)
    y_bounds = [0] + ys + [ch]

    # Benodigde segmenten = tussen eerste en laatste X-snede (of hele lengte)
    # Alles buiten = restant
    # Als geen snedes: alles is benodigde strip
    if len(xs) >= 2:
        needed_y0 = xs[0]
        needed_y1 = xs[-1]
    elif len(xs) == 1:
        needed_y0 = 0
        needed_y1 = xs[0]
    else:
        needed_y0 = 0
        needed_y1 = bl

    if len(ys) >= 2:
        needed_z0 = ys[0]
        needed_z1 = ys[-1]
    elif len(ys) == 1:
        needed_z0 = 0
        needed_z1 = ys[0]
    else:
        needed_z0 = 0
        needed_z1 = ch

    def is_needed(y0, y1, z0, z1):
        """Is dit segment het benodigde stuk?"""
        y_ok = (y0 >= needed_y0 - 0.001) and (y1 <= needed_y1 + 0.001)
        z_ok = (z0 >= needed_z0 - 0.001) and (z1 <= needed_z1 + 0.001)
        return y_ok and z_ok

    # ── Teken alle blokken per segment ────────────────────────────────────
    for i, (yb0, yb1) in enumerate(zip(x_bounds[:-1], x_bounds[1:])):
        for j, (zb0, zb1) in enumerate(zip(y_bounds[:-1], y_bounds[1:])):
            needed = is_needed(yb0, yb1, zb0, zb1)
            fc_top   = RTOP  if needed else GTOP
            fc_side  = RSIDE if needed else GSIDE
            fc_front = RED   if needed else GREY
            ec       = "#1a1a2e" if needed else "#7f8c8d"
            lw       = 1.1 if needed else 0.7
            zo       = 4 if needed else 2
            al_grey  = 0.75

            # Bottom (alleen onderste laag)
            if j == 0:
                face(ax, [(0,yb0,zb0),(aw,yb0,zb0),(aw,yb1,zb0),(0,yb1,zb0)],
                     fc_side, ec=ec, lw=lw,
                     alpha=1.0 if needed else al_grey, zorder=zo-1)
            # Top
            face(ax, [(0,yb0,zb1),(aw,yb0,zb1),(aw,yb1,zb1),(0,yb1,zb1)],
                 fc_top, ec=ec, lw=lw,
                 alpha=1.0 if needed else al_grey, zorder=zo+1)
            # Voorkant (y=0 kant)
            if i == 0:
                face(ax, [(0,yb0,zb0),(aw,yb0,zb0),(aw,yb0,zb1),(0,yb0,zb1)],
                     fc_front, ec=ec, lw=lw+0.3 if needed else lw,
                     alpha=1.0 if needed else al_grey, zorder=zo+2)
            # Rechterkant (x=aw)
            face(ax, [(aw,yb0,zb0),(aw,yb1,zb0),(aw,yb1,zb1),(aw,yb0,zb1)],
                 fc_side, ec=ec, lw=lw,
                 alpha=1.0 if needed else al_grey, zorder=zo)
            # Linkerkant (x=0) — alleen buitenste
            if True:
                face(ax, [(0,yb0,zb0),(0,yb1,zb0),(0,yb1,zb1),(0,yb0,zb1)],
                     fc_front, ec=ec, lw=lw,
                     alpha=0.5 if not needed else 0.7, zorder=zo-1)
            # Achterkant (y=bl kant)
            if i == len(x_bounds) - 2:
                face(ax, [(0,yb1,zb0),(aw,yb1,zb0),(aw,yb1,zb1),(0,yb1,zb1)],
                     fc_front, ec=ec, lw=lw,
                     alpha=0.4 if not needed else 0.5, zorder=zo-1)

    # ── X-snijvlakken (langs lengte) ──────────────────────────────────────
    for idx, xw in enumerate(xs):
        for j, (zb0, zb1) in enumerate(zip(y_bounds[:-1], y_bounds[1:])):
            face(ax, [(0,xw,zb0),(aw,xw,zb0),(aw,xw,zb1),(0,xw,zb1)],
                 XCUT, ec="none", lw=0, zorder=8)

        # Randlijnen
        for zb in y_bounds:
            pl = iso(0,  xw, zb)
            pr = iso(aw, xw, zb)
            ax.plot([pl[0],pr[0]], [pl[1],pr[1]],
                    color="#1a1a2e", lw=1.5, zorder=20)
        for xpos in [0, aw]:
            pts = [iso(xpos, xw, zb) for zb in y_bounds]
            for k in range(len(pts)-1):
                ax.plot([pts[k][0],pts[k+1][0]], [pts[k][1],pts[k+1][1]],
                        color="#1a1a2e", lw=1.5, zorder=20)

        # Stippellijn bovenkant
        p_tl = iso(0,  xw, ch)
        p_tr = iso(aw, xw, ch)
        ax.plot([p_tl[0],p_tr[0]], [p_tl[1],p_tr[1]],
                "--", color=RED, lw=1.6, dashes=(5,3), zorder=21)
        draw_saw_length(ax, xw, aw, ch, zorder=22+idx)

    # ── Y-snijvlakken (langs hoogte) ──────────────────────────────────────
    for idx, yw in enumerate(ys):
        for i, (yb0, yb1) in enumerate(zip(x_bounds[:-1], x_bounds[1:])):
            face(ax, [(0,yb0,yw),(aw,yb0,yw),(aw,yb1,yw),(0,yb1,yw)],
                 YCUT, ec="none", lw=0, zorder=9)

        # Randlijnen
        for yb in x_bounds:
            pl = iso(0,  yb, yw)
            pr = iso(aw, yb, yw)
            ax.plot([pl[0],pr[0]], [pl[1],pr[1]],
                    color="#8e44ad", lw=1.5, zorder=20)
        for xpos in [0, aw]:
            pts = [iso(xpos, yb, yw) for yb in x_bounds]
            for k in range(len(pts)-1):
                ax.plot([pts[k][0],pts[k+1][0]], [pts[k][1],pts[k+1][1]],
                        color="#8e44ad", lw=1.5, zorder=20)

        draw_saw_height(ax, yw, bl, aw, zorder=26+idx)

    # ── MATEN ─────────────────────────────────────────────────────────────
    # A
    dim_arrow(ax, (0,0,0), (aw,0,0),
              f"A={int(A)}mm", color="#1a1a2e", perp=(0,-0.55))
    # B
    dim_arrow(ax, (aw,0,0), (aw,bl,0),
              f"B={int(B)}mm", color="#374151", perp=(1.0,-0.5))
    for yb in [0, bl]:
        p = iso(aw, yb, 0)
        ax.plot([p[0], p[0]+1.0], [p[1], p[1]-0.5],
                ":", color="#374151", lw=0.9, zorder=14)
    # C
    p_bot = iso(aw, 0, 0)
    p_top = iso(aw, 0, ch)
    off = np.array([0.5, 0])
    ax.annotate("", xy=p_top+off, xytext=p_bot+off,
                arrowprops=dict(arrowstyle="<->", color="#374151",
                                lw=1.2, mutation_scale=10), zorder=15)
    mc = (p_bot+p_top)/2 + off + np.array([0.4,0])
    ax.text(mc[0], mc[1], f"C={int(C)}mm", ha="left", va="center",
            fontsize=8, fontweight="bold", color="#374151", zorder=16,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#374151",
                      lw=0.7, alpha=0.95))
    # D
    pd = iso(0, bl*0.6, ch*0.5)
    ax.text(pd[0]-0.5, pd[1], f"D={int(D)}mm", ha="right", va="center",
            fontsize=8, fontweight="bold", color="#374151", zorder=16,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#374151",
                      lw=0.7, alpha=0.95))

    # X-snede labels
    prev = 0
    for idx, (xv, xw) in enumerate(zip(x_cuts, xs)):
        dim_arrow(ax, (0, prev*scale, 0), (0, xw, 0),
                  f"X{idx+1}={int(xv)}mm",
                  color=RED, perp=(-0.7 - idx*0.05, -0.35 - idx*0.1))
        prev = xv

    # Y-snede labels
    prev = 0
    for idx, (yv, yw) in enumerate(zip(y_cuts, ys)):
        p1 = iso(aw, bl, prev*scale) + np.array([0.5+idx*0.05, 0])
        p2 = iso(aw, bl, yw)         + np.array([0.5+idx*0.05, 0])
        ax.annotate("", xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="<->", color="#8e44ad",
                                    lw=1.3, mutation_scale=10), zorder=15)
        mid = (p1+p2)/2 + np.array([0.4,0])
        ax.text(mid[0], mid[1], f"Y{idx+1}={int(yv)}mm",
                ha="left", va="center", fontsize=8, fontweight="bold",
                color="#8e44ad", zorder=16,
                bbox=dict(boxstyle="round,pad=0.2", fc="white",
                          ec="#8e44ad", lw=0.7, alpha=0.95))
        prev = yv

    # ── LEGENDA ───────────────────────────────────────────────────────────
    patches = [
        mpatches.Patch(facecolor=RED,  edgecolor="#1a1a2e", label="Benodigde strip"),
        mpatches.Patch(facecolor=GTOP, edgecolor="#7f8c8d", label="Restant"),
    ]
    if x_cuts:
        patches.append(mpatches.Patch(facecolor=XCUT, edgecolor=RED,
                                       label="X-snijvlak (lengte)"))
    if y_cuts:
        patches.append(mpatches.Patch(facecolor=YCUT, edgecolor="#8e44ad",
                                       label="Y-snijvlak (hoogte)"))
    ax.legend(handles=patches, loc="lower right", fontsize=8.5,
              framealpha=0.95, edgecolor="#d1d5db",
              bbox_to_anchor=(0.98, 0.02))

    ax.set_title("Steenstrippen – Afgekorte strip",
                 fontsize=11, fontweight="bold", color="#1a1a2e",
                 loc="left", pad=10)

    ax.autoscale_view()
    xl = ax.get_xlim(); yl = ax.get_ylim()
    ax.set_xlim(xl[0]-1.8, xl[1]+3.0)
    ax.set_ylim(yl[0]-1.2, yl[1]+1.8)
    fig.tight_layout(pad=0.5)
    return fig
