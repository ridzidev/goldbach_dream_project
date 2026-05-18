import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import tkinter as tk
from tkinter import simpledialog

# Sieve of Eratosthenes (Efficient)
def get_primes_up_to(limit):
    if limit < 2: return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

# RIDZI BUTTERFLY THEORY: Midpoint m and Distance d
def get_symmetric_groups(n, primes_set):
    m = n // 2
    groups = []
    
    for d in range(m - 1):
        p = m - d
        q = m + d
        if p in primes_set and q in primes_set:
            groups.append({
                'is_central': (d == 0),
                'd': d, 'm': m,
                'p': p, 'q': q      
            })
            
    # Sort by distance d ASCENDING 
    groups.sort(key=lambda g: g['d'], reverse=False)
    return groups

# ZERO-GAP CIRCULAR CRYSTAL ALGORITHM (With Butterfly Wing Anatomy Modification)
def calculate_crystal_packing(groups):
    placed_xy = []
    polygons = []
    max_radius_fit = 0
    total_square_area = 0
    contact_points = [] # Melacak titik yang menyentuh radius terluar
    eps = 1e-6 

    for g in groups:
        p, q, d, is_central = g['p'], g['q'], g['d'], g['is_central']
        
        # Menggunakan skala logaritmik untuk massa (Prime Number Theorem) [cite: 172]
        W = (2 * p) / np.log(p + 1) 
        half_w = W / 2
        diag_val = W * np.sqrt(2)
        
        candidates = []
        if not placed_xy:
            candidates.append((0, 0) if is_central else (half_w, 0))
        else:
            U_edges, V_edges = [0.0], [0.0]
            for P in placed_xy:
                gap_half = (P['W'] + W) / 2
                U_edges.extend([P['x'] - gap_half, P['x'] + gap_half])
                V_edges.extend([P['y'] - gap_half, P['y'] + gap_half])
            
            for x_cand in U_edges:
                for y_cand in V_edges:
                    if not is_central and max(abs(x_cand), abs(y_cand)) < half_w - eps:
                        continue
                    valid = True
                    for P in placed_xy:
                        check_w = (P['W'] + W) / 2
                        if abs(x_cand - P['x']) < check_w - eps and abs(y_cand - P['y']) < check_w - eps:
                            valid = False
                            break
                    if valid: candidates.append((x_cand, y_cand))
        
        candidates.sort(key=lambda c: (round(c[0]**2 + c[1]**2, 5), round(abs(c[0]), 5)))
        best_x, best_y = candidates[0]
        
        def place_item(cx, cy, label):
            nonlocal max_radius_fit, total_square_area
            placed_xy.append({'x': cx, 'y': cy, 'W': W})
            
            # --- ANALISIS TITIK KONTAK (SUDUT PERSEGI) ---
            # Setiap persegi memiliki 4 sudut. Kita cari yang terjauh dari pusat.
            corners = [
                (cx + half_w, cy + half_w), (cx - half_w, cy + half_w),
                (cx + half_w, cy - half_w), (cx - half_w, cy - half_w)
            ]
            
            for (kx, ky) in corners:
                r_dist = np.sqrt(kx**2 + ky**2)
                if abs(r_dist - max_radius_fit) < eps:
                    contact_points.append({'x': kx, 'y': ky, 'pair': (p, q)})
                elif r_dist > max_radius_fit:
                    max_radius_fit = r_dist
                    contact_points.clear()
                    contact_points.append({'x': kx, 'y': ky, 'pair': (p, q)})

            total_square_area += (W * W)

            # --- GEOMETRI 'X' BONE & BUTTERFLY ---
            t = half_w * 0.22
            x_verts = np.array([
                (half_w, half_w), (half_w-t, half_w), (0, t), (-half_w+t, half_w), (-half_w, half_w),
                (-half_w, half_w-t), (-t, 0), (-half_w, -half_w+t), (-half_w, -half_w),
                (-half_w+t, -half_w), (0, -t), (half_w-t, -half_w), (half_w, -half_w),
                (half_w, -half_w+t), (t, 0), (half_w, half_w-t)
            ])
            x_verts[:, 0] += cx; x_verts[:, 1] += cy
            
            theta = np.linspace(0, 2*np.pi, 200)
            # Fay's Butterfly Wing Parametric Function [cite: 57]
            r_wing = np.exp(np.sin(theta)) - 2*np.cos(4*theta) + np.sin((2*theta - np.pi)/24)**5
            xb, yb = r_wing * np.cos(theta), r_wing * np.sin(theta)
            scale = (half_w * 0.95) / max(np.max(np.abs(xb)), np.max(np.abs(yb)))
            
            polygons.append({
                'x_verts': x_verts,
                'wing_outer': np.column_stack((cx + xb * scale, cy + yb * scale)),
                'wing_inner': np.column_stack((cx + xb * scale * 0.6, cy + yb * scale * 0.6)),
                'cx': cx, 'cy': cy, 'p': p, 'W': W, 'label': label
            })

        if is_central:
            place_item(best_x, best_y, f"({p},{p})\nd=0")
        else:
            place_item(best_x, best_y, f"({p},{q})\nd={d}")
            place_item(-best_x, -best_y, f"({q},{p})\nd={d}")
            
    return polygons, max_radius_fit, total_square_area, contact_points

def plot_fractal_goldbach_crystal(n):
    if n % 2 != 0: n -= 1
    primes = set(get_primes_up_to(n))
    groups = get_symmetric_groups(n, primes)
    if not groups: return

    m = n // 2
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_aspect('equal')

    polygons_data, R_fit, total_sq_area, contacts = calculate_crystal_packing(groups)
    
    # Metrik Cakupan Ruang 
    universe_area = np.pi * (R_fit**2)
    coverage_ratio = (total_sq_area / universe_area) * 100 if universe_area > 0 else 0

    # Universe Circle & Axis
    ax.add_patch(plt.Circle((0, 0), R_fit, color='cyan', fill=False, lw=1.5, alpha=0.5))
    ax.axhline(0, color='white', lw=0.4, alpha=0.3, ls='--')
    ax.axvline(0, color='white', lw=0.4, alpha=0.3, ls='--')

    cmap_wing = plt.get_cmap('turbo')
    for poly in polygons_data:
        p, cx, cy, w_val = poly['p'], poly['cx'], poly['cy'], poly['W']
        
        # Render Sayap & Bone
        ax.add_patch(plt.Polygon(poly['wing_outer'], facecolor=cmap_wing(p/m), alpha=0.7))
        ax.add_patch(plt.Polygon(poly['wing_inner'], facecolor='orange', alpha=0.4))
        ax.add_patch(plt.Polygon(poly['x_verts'], facecolor='white', alpha=0.2, edgecolor='cyan'))
        
        # Gambar Persegi (Bounding Box) yang Anda sukai
        ax.add_patch(plt.Rectangle((cx - w_val/2, cy - w_val/2), w_val, w_val, 
                                   fill=False, edgecolor='white', lw=0.6, alpha=0.3, ls=':'))

    # Visualisasi Titik Kontak
    for cp in contacts:
        angle = np.degrees(np.arctan2(cp['y'], cp['x']))
        ax.plot(cp['x'], cp['y'], 'ro', markersize=5)
        ax.annotate(f"{angle:.1f}°", (cp['x'], cp['y']), color='red', fontsize=8, fontweight='bold')

    # PANEL INFORMASI YANG DIPERKAYA
    contact_info = ""
    for i, cp in enumerate(contacts[:3]): # Ambil 3 titik pertama
        angle = np.degrees(np.arctan2(cp['y'], cp['x']))
        contact_info += f"Contact {i+1}: ({cp['x']:.1f}, {cp['y']:.1f}) @ {angle:.1f}°\n"

    info_text = (
        f" GOLDBACH STRUCTURAL ANALYSIS\n"
        f" {'='*34}\n"
        f" n Value : {n} | Midpoint: {m}\n"
        f" Total Pairs: {len(groups)}\n"
        f" {'='*34}\n\n"
        f" UNIVERSE CIRCLE GEOMETRY\n"
        f" {'='*34}\n"
        f" Radius (R): {R_fit:.4f}\n"
        f" Square Area: {total_sq_area:.2f}\n"
        f" Coverage Ratio: {coverage_ratio:.2f}%\n"
        f" {'='*34}\n\n"
        f" SYMMETRIC CONTACT POINTS\n"
        f" {'='*34}\n"
        f"{contact_info}"
        f" {'='*34}\n\n"
        f" ANALYTICAL INSIGHT\n"
        f" {'='*34}\n"
        f" Persegi yang menyentuh\n"
        f" lingkaran berasal dari\n"
        f" pasangan: {contacts[0]['pair']}\n"
        f" {'='*34}\n"
    )
    
    fig.text(0.015, 0.5, info_text, fontsize=9, color='white', va='center', family='monospace',
             bbox=dict(facecolor='#0a192f', alpha=0.85, edgecolor='#00ffcc', boxstyle='round', lw=1.5))

    plt.title(f"Butterfly Crystal Analysis: Goldbach Symmetry (n={n})", color='gold', fontsize=16)
    plt.axis('off')
    plt.tight_layout(rect=[0.26, 0.0, 1.0, 1.0])
    plt.show()


def main():
    root = tk.Tk()
    root.withdraw()
    n = simpledialog.askinteger("Butterfly Crystal Mapping",
                                     "Input an Even Integer n\n(n >= 4):",
                                     minvalue=4, maxvalue=10000)
    if n:
        plot_fractal_goldbach_crystal(n)

if __name__ == "__main__":
    main()

