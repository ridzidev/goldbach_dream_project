import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import tkinter as tk
from tkinter import simpledialog

# 1. PONDASI: Sieve of Eratosthenes
def get_primes_up_to(limit):
    if limit < 2: return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

# 2. STRUKTUR: Midpoint Symmetry (Sesuai Teori Ridzi)
def get_symmetric_groups(n, primes_set):
    m = n // 2
    groups = []
    for d in range(m - 1):
        p, q = m - d, m + d
        if p in primes_set and q in primes_set:
            groups.append({'d': d, 'p': p, 'q': q, 'is_central': (d == 0)})
    groups.sort(key=lambda g: g['d'])
    return groups

# 3. PACKING: Zero-Gap Circular Crystal (Statis & Stabil)
def calculate_crystal_packing(groups):
    placed = []
    polygons = []
    max_radius = 0
    eps = 1e-6

    for g in groups:
        p, d = g['p'], g['d']
        # W (Width) berdasarkan p, tapi dibatasi agar tidak meledak di n kecil
        W = 2 * p 
        
        candidates = []
        if not placed:
            candidates.append((0.0, 0.0))
        else:
            # Mencari posisi berdasarkan bounding box terdekat (Zero-Gap)
            for P in placed:
                step = (P['W'] + W) / 2
                candidates.extend([
                    (P['x'] + step, P['y']), (P['x'] - step, P['y']),
                    (P['x'], P['y'] + step), (P['x'], P['y'] - step)
                ])
        
        candidates.sort(key=lambda c: c[0]**2 + c[1]**2)
        
        best_x, best_y = 0, 0
        for cx, cy in candidates:
            overlap = False
            for P in placed:
                if abs(cx - P['x']) < (W + P['W'])/2 - eps and \
                   abs(cy - P['y']) < (W + P['W'])/2 - eps:
                    overlap = True; break
            if not overlap:
                best_x, best_y = cx, cy; break

        def place(x, y, label_p, label_q):
            nonlocal max_radius
            # --- WING GEOMETRY (Stabilized) ---
            theta = np.linspace(0, 2*np.pi, 150)
            # Fungsi Ridzi yang disederhanakan agar tidak 'blob'
            r = np.exp(np.sin(theta)) - 2*np.cos(4*theta) + np.sin((2*theta-np.pi)/24)**5
            
            # Normalisasi r agar pas dalam bounding box p
            xb, yb = r * np.cos(theta), r * np.sin(theta)
            scale = (p * 0.9) / max(np.max(np.abs(xb)), np.max(np.abs(yb)))
            
            wing_out = np.column_stack((x + xb * scale, y + yb * scale))
            wing_in = np.column_stack((x + xb * scale * 0.6, y + yb * scale * 0.6))
            
            # --- BONE SKELETON ---
            t = p * 0.2
            bone = np.array([(p,p), (0,t), (-p,p), (-t,0), (-p,-p), (0,-t), (p,-p), (t,0), (p,p)])
            bone[:, 0] += x; bone[:, 1] += y
            
            placed.append({'x': x, 'y': y, 'W': W})
            polygons.append({'wing_out': wing_out, 'wing_in': wing_in, 'bone': bone, 
                             'cx': x, 'cy': y, 'p': p, 'd': d, 'label': f"({label_p},{label_q})"})
            
            dist = np.sqrt(x**2 + y**2) + p
            max_radius = max(max_radius, dist)

        if g['is_central']:
            place(best_x, best_y, p, p)
        else:
            place(best_x, best_y, p, g['q'])
            place(-best_x, -best_y, g['q'], p)
            
    return polygons, max_radius

# 4. PLOTTING: Final Artemis Map
def plot_goldbach_crystal(n):
    primes = set(get_primes_up_to(n))
    groups = get_symmetric_groups(n, primes)
    if not groups: return

    polygons, R_fit = calculate_crystal_packing(groups)
    
    # Gunakan raw string r"" untuk title agar tidak ada SyntaxWarning \p
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
    ax.set_aspect('equal')
    
    # Universe Circle
    u_circle = plt.Circle((0,0), R_fit, color='cyan', fill=False, lw=1.5, alpha=0.4)
    ax.add_patch(u_circle)
    
    # Plotting Elements
    for poly in polygons:
        p = poly['p']
        # Gradasi warna berdasarkan nilai p
        color_val = plt.cm.turbo(p / (n/2))
        
        ax.add_patch(plt.Polygon(poly['wing_out'], facecolor=color_val, alpha=0.6))
        ax.add_patch(plt.Polygon(poly['wing_in'], facecolor='white', alpha=0.3))
        ax.add_patch(plt.Polygon(poly['bone'], edgecolor='cyan', fill=False, lw=0.8, alpha=0.5))
        
        # Label font size yang menyesuaikan skala
        f_size = max(5, min(10, 50 * p / R_fit))
        ax.text(poly['cx'], poly['cy'], f"{poly['label']}\nd={poly['d']}", 
                color='white', fontsize=f_size, ha='center', va='center',
                path_effects=[pe.withStroke(linewidth=2, foreground="black")])

    ax.set_xlim(-R_fit*1.1, R_fit*1.1)
    ax.set_ylim(-R_fit*1.1, R_fit*1.1)
    ax.axis('off')
    
    plt.title(fr"Ridzi Butterfly Crystal: $n={n}$ (Midpoint Symmetry)", color='gold', fontsize=16)
    
    # Panel Info (Diletakkan di luar axes agar tidak mengganggu layout)
    info_str = f"Universe Radius: {R_fit:.2f}\nTotal Pairs: {len(groups)}"
    fig.text(0.02, 0.02, info_str, color='cyan', family='monospace')
    
    plt.show()

if __name__ == "__main__":
    # Test dengan n=10 untuk membuktikan perbaikan, lalu coba n=4034
    plot_goldbach_crystal(4034)