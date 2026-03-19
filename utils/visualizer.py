"""
utils/visualizer.py
X    = snede langs de LENGTE  (B-as)
Y    = snede langs de BREEDTE (A-as, 90gr van X)
Zool = snede langs de HOOGTE  (C-as)
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
    pts2d = [iso(float(p[0]), float(p[1]), float(p[2])) for p in pts3d]
    poly = Polygon(pts2d, closed=True, facecolor=fc,
                   edgecolor=ec, linewidth=lw, alpha=alpha, zorder=zorder)
    ax.add_patch(poly)


def draw_saw(ax, center_2d, color="#2c3e50", target_2d=None, zorder=21):
    r = 0.38
    ax.add_patch(plt.Circle(center_2d, r, facecolor="#95a5a6",
                            edgecolor=color, lw=1.4, zorder=zorder, alpha=0.92))
    for ang in np.linspace(0, 360, 18, endpoint=False):
        a = np.radians(ang)
        t1 = center_2d + r        * np.array([np.cos(a), np.sin(a)])
        t2 = center_2d + (r+0.10) * np.array([np.cos(a), np.sin(a)])
        ax.plot([t1[0], t2[0]], [t1[1], t2[1]], color=color, lw=1.1, zorder=zorder+1)
    ax.plot(*center_2d, "o", color=color, ms=3.5, zorder=zorder+2)
    if target_2d is not None:
        ax.annotate("", xy=target_2d, xytext=center_2d,
                    arrowprops=dict(arrowstyle="-|>", color=color,
                                    lw=1.1, mutation_scale=9), zorder=zorder+2)


def dim_arrow(ax, p1, p2, label, color="#1a1a2e", fontsize=8.0, zorder=15):
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="<->", color=color,
                                lw=1.3, mutation_scale=10), zorder=zorder)
    mid = (p1 + p2) / 2
    ax.text(mid[0], mid[1], label, ha="center", va="center",
            fontsize=fontsize, fontweight="bold", color=color, zorder=zorder+1,
            bbox=dict(boxstyle="round,pad=0.2", fc="white",
                      ec=color, lw=0.7, alpha=0.95))


def draw_strip_diagram(A, B, C, D, x_cuts=None, y_cuts=None, zool_cuts=None):
    A = max(float(A), 1); B = max(float(B), 1)
    C = max(float(C), 1); D = max(float(D), 1)

    x_cuts    = sorted([float(v) for v in (x_cuts    or []) if 0 < float(v) < B])
    y_cuts    = sorted([float(v) for v in (y_cuts    or []) if 0 < float(v) < A])
    zool_cuts = sorted([float(v) for v in (zool_cuts or []) if 0 < float(v) < C])

    scale = 7.0 / max(A, B, C)
    aw = A * scale; bl = B * scale; ch = C * scale

    xb = [v * scale for v in [0.0] + x_cuts    + [B]]
    yb = [v * scale for v in [0.0] + y_cuts    + [A]]
    zb = [v * scale for v in [0.0] + zool_cuts + [C]]

    RED  = "#c0392b"; RTOP  = "#e74c3c"; RSIDE = "#922b21"
    GREY = "#bdc3c7"; GTOP  = "#d5d8dc"; GSIDE = "#99a3a4"
    XCOL = "#f5b7b1"; YCOL  = "#a9cce3"; ZCOL  = "#d7bde2"
    YLINE = "#1a6fa8"; ZLINE = "#8e44ad"

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_aspect("equal"); ax.axis("off")
    fig.patch.set_facecolor("#f0f3f8"); ax.set_facecolor("#f0f3f8")

    def is_needed(xi, yi, zi):
        return ((xi == 0) if x_cuts else True) and \
               ((yi == 0) if y_cuts else True) and \
               ((zi == 0) if zool_cuts else True)

    nx = len(xb)-1; ny = len(yb)-1; nz = len(zb)-1

    for xi in range(nx):
        for yi in range(ny):
            for zi in range(nz):
                y0, y1 = xb[xi], xb[xi+1]
                x0, x1 = yb[yi], yb[yi+1]
                z0, z1 = zb[zi], zb[zi+1]
                n   = is_needed(xi, yi, zi)
                fct = RTOP  if n else GTOP
                fcs = RSIDE if n else GSIDE
                fcf = RED   if n else GREY
                ec  = "#1a1a2e" if n else "#7f8c8d"
                lw  = 1.1 if n else 0.7
                zo  = 4   if n else 2
                al  = 1.0 if n else 0.75

                face(ax,[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)], fct,ec=ec,lw=lw,alpha=al,zorder=zo+1)
                face(ax,[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)], fcs,ec=ec,lw=lw,alpha=al,zorder=zo)
                if xi == 0:
                    face(ax,[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)], fcf,ec=ec,lw=lw+0.2 if n else lw,alpha=al,zorder=zo+2)
                if zi == 0:
                    face(ax,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)], fcs,ec=ec,lw=lw,alpha=al*0.6,zorder=zo-1)
                face(ax,[(x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1)], fcf,ec=ec,lw=lw,alpha=al*0.5,zorder=zo-1)
                if xi == nx-1:
                    face(ax,[(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)], fcf,ec=ec,lw=lw,alpha=al*0.4,zorder=zo-1)

    # X-snijvlakken
    for idx, xv in enumerate(x_cuts):
        xw = xv * scale
        face(ax,[(0,xw,0),(aw,xw,0),(aw,xw,ch),(0,xw,ch)], XCOL,ec="none",lw=0,zorder=8)
        for zv in zb:
            pl=iso(0,xw,zv); pr=iso(aw,xw,zv)
            ax.plot([pl[0],pr[0]],[pl[1],pr[1]],color="#1a1a2e",lw=1.5,zorder=20)
        for xpos in [0,aw]:
            for k in range(len(zb)-1):
                p1=iso(xpos,xw,zb[k]); p2=iso(xpos,xw,zb[k+1])
                ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color="#1a1a2e",lw=1.5,zorder=20)
        tl=iso(0,xw,ch); tr=iso(aw,xw,ch)
        ax.plot([tl[0],tr[0]],[tl[1],tr[1]],"--",color=RED,lw=1.5,dashes=(5,3),zorder=21)
        saw_c=(tl+tr)/2+np.array([0,0.8])
        draw_saw(ax,saw_c,color="#2c3e50",target_2d=(tl+tr)/2,zorder=22+idx)

    # Y-snijvlakken
    for idx, yv in enumerate(y_cuts):
        yw = yv * scale
        face(ax,[(yw,0,0),(yw,bl,0),(yw,bl,ch),(yw,0,ch)], YCOL,ec="none",lw=0,zorder=9)
        for zv in zb:
            pl=iso(yw,0,zv); pr=iso(yw,bl,zv)
            ax.plot([pl[0],pr[0]],[pl[1],pr[1]],color=YLINE,lw=1.5,zorder=20)
        for ypos in [0,bl]:
            for k in range(len(zb)-1):
                p1=iso(yw,ypos,zb[k]); p2=iso(yw,ypos,zb[k+1])
                ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=YLINE,lw=1.5,zorder=20)
        pm=iso(yw,bl/2,ch); saw_c=pm+np.array([0,0.8])
        draw_saw(ax,saw_c,color=YLINE,target_2d=pm,zorder=26+idx)

    # Zool-snijvlakken
    for idx, zv_mm in enumerate(zool_cuts):
        zw = zv_mm * scale
        face(ax,[(0,0,zw),(aw,0,zw),(aw,bl,zw),(0,bl,zw)], ZCOL,ec="none",lw=0,zorder=10)
        for ypos in xb:
            pl=iso(0,ypos,zw); pr=iso(aw,ypos,zw)
            ax.plot([pl[0],pr[0]],[pl[1],pr[1]],color=ZLINE,lw=1.5,zorder=20)
        for xpos in [0,aw]:
            for k in range(len(xb)-1):
                p1=iso(xpos,xb[k],zw); p2=iso(xpos,xb[k+1],zw)
                ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=ZLINE,lw=1.5,zorder=20)
        pm=iso(aw,bl/2,zw); saw_c=pm+np.array([0.8,0])
        draw_saw(ax,saw_c,color=ZLINE,target_2d=pm,zorder=28+idx)

    # Maatpijlen
    dim_arrow(ax, iso(0,0,0)+[0,-0.55],   iso(aw,0,0)+[0,-0.55],   f"A={int(A)}mm", "#1a1a2e")
    dim_arrow(ax, iso(aw,0,0)+[1.0,-0.5], iso(aw,bl,0)+[1.0,-0.5], f"B={int(B)}mm", "#374151")
    for ypos in [0,bl]:
        p=iso(aw,ypos,0); ax.plot([p[0],p[0]+1.0],[p[1],p[1]-0.5],":",color="#374151",lw=0.9)

    pb=iso(aw,0,0)+[0.5,0]; pt=iso(aw,0,ch)+[0.5,0]
    ax.annotate("",xy=pt,xytext=pb,arrowprops=dict(arrowstyle="<->",color="#374151",lw=1.2,mutation_scale=10),zorder=15)
    mc=((pb[0]+pt[0])/2+0.4,(pb[1]+pt[1])/2)
    ax.text(mc[0],mc[1],f"C={int(C)}mm",ha="left",va="center",fontsize=8,fontweight="bold",color="#374151",zorder=16,
            bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="#374151",lw=0.7,alpha=0.95))

    pd=iso(0,bl*0.6,ch*0.5)
    ax.text(pd[0]-0.5,pd[1],f"D={int(D)}mm",ha="right",va="center",fontsize=8,fontweight="bold",color="#374151",zorder=16,
            bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="#374151",lw=0.7,alpha=0.95))

    prev=0.0
    for idx,xv in enumerate(x_cuts):
        dim_arrow(ax, iso(0,prev*scale,0)+[-0.7-idx*0.6,-0.35], iso(0,xv*scale,0)+[-0.7-idx*0.6,-0.35], f"X{idx+1}={int(xv)}mm", RED)
        prev=xv

    prev=0.0
    for idx,yv in enumerate(y_cuts):
        dim_arrow(ax, iso(prev*scale,0,0)+[0,-0.9-idx*0.5], iso(yv*scale,0,0)+[0,-0.9-idx*0.5], f"Y{idx+1}={int(yv)}mm", YLINE)
        prev=yv

    prev=0.0
    for idx,zv in enumerate(zool_cuts):
        dim_arrow(ax, iso(aw,bl,prev*scale)+[0.5+idx*0.6,0], iso(aw,bl,zv*scale)+[0.5+idx*0.6,0], f"Z{idx+1}={int(zv)}mm", ZLINE)
        prev=zv

    patches=[
        mpatches.Patch(facecolor=RED, edgecolor="#1a1a2e",label="Benodigde strip"),
        mpatches.Patch(facecolor=GTOP,edgecolor="#7f8c8d",label="Restant"),
    ]
    if x_cuts:    patches.append(mpatches.Patch(facecolor=XCOL,edgecolor=RED,  label="X-snijvlak (lengte)"))
    if y_cuts:    patches.append(mpatches.Patch(facecolor=YCOL,edgecolor=YLINE,label="Y-snijvlak (breedte)"))
    if zool_c
