import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import tkinter as tk
from tkinter import simpledialog

# Sieve prima (Efisien)
def get_primes_up_to(limit):
    if limit < 2: return []
    sieve = [True] * (limit + 1
    )
    sieve[0] = sieve[1] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

# MENGGUNAKAN TEORI M ALFA RIDZI: Midpoint m dan Jarak d
def get_symmetric_groups(n, primes_set):
    m = n // 2
    groups =[]
    
    for d in range(m - 1):
        p = m - d
        q = m + d
        if p in primes_set and q in primes_set:
            groups.append({
                'is_central': (d == 0),
                'd': d, 'm': m,
                'p': p, 'q': q      
            })
            
    # Urutkan berdasarkan jarak d ASCENDING 
    groups.sort(key=lambda g: g['d'], reverse=False)
    return groups

# ALGORITMA ASLI: Kristal Lingkaran Nol-Celah (Dengan Modifikasi Anatomi Sayap)
def calculate_crystal_packing(groups):
    placed_xy = []
    polygons =[]
    max_radius_fit = 0
    eps = 1e-6 

    for g in groups:
        p, q, d, is_central = g['p'], g['q'], g['d'], g['is_central']
        W = 2 * p  # Lebar mutlak (0 Gap)
        diag_val = 2 * p * np.sqrt(2) # Perhitungan diagonal kupu-kupu (Diagonal Square = W * sqrt(2))
        
        candidates =[]
        
        # 1. Posisikan Pasangan Pertama
        if not placed_xy:
            if is_central:
                candidates.append((0, 0))
            else:
                candidates.append((W/2, 0))
        else:
            # 2. Cari titik singgung dari yang sudah ditempatkan
            U_edges = [0.0]
            V_edges = [0.0]
            for P in placed_xy:
                half = (P['W'] + W) / 2
                U_edges.extend([P['x'] - half, P['x'] + half])
                V_edges.extend([P['y'] - half, P['y'] + half])
            
            for x_cand in U_edges:
                for y_cand in V_edges:
                    if not is_central and max(abs(x_cand), abs(y_cand)) < (W / 2) - eps:
                        continue
                        
                    valid = True
                    for P in placed_xy:
                        half = (P['W'] + W) / 2
                        if abs(x_cand - P['x']) < half - eps and abs(y_cand - P['y']) < half - eps:
                            valid = False
                            break
                    
                    if valid:
                        candidates.append((x_cand, y_cand))
        
        # 3. Sortir Jarak ke Pusat (Mempertahankan kristal melingkar)
        candidates.sort(key=lambda c: (round(c[0]**2 + c[1]**2, 5), round(abs(c[0]), 5), round(abs(c[1]), 5), c[0], c[1]))
        best_x, best_y = candidates[0]
        
        def place_item(cx, cy, label):
            nonlocal max_radius_fit
            placed_xy.append({'x': cx, 'y': cy, 'W': W})
            
            # --- BAGIAN 1: TULANG 'X' ---
            t = p * 0.22  # Ketebalan tulang
            x_verts = np.array([
                (p, p), (p-t, p), (0, t), (-p+t, p), (-p, p),
                (-p, p-t), (-t, 0), (-p, -p+t), (-p, -p),
                (-p+t, -p), (0, -t), (p-t, -p), (p, -p),
                (p, -p+t), (t, 0), (p, p-t)
            ])
            x_verts[:, 0] += cx
            x_verts[:, 1] += cy
            
            dist = np.linalg.norm(x_verts, axis=1)
            max_radius_fit = max(max_radius_fit, np.max(dist))
            
            # --- BAGIAN 2: SAYAP KUPU-KUPU (PARAMETRIK FAY) ---
            theta = np.linspace(0, 2*np.pi, 200)
            r = np.exp(np.sin(theta)) - 2*np.cos(4*theta) + np.sin((2*theta - np.pi)/24)**5
            
            xb = r * np.cos(theta)
            yb = r * np.sin(theta)
            
            scale = (p * 0.95) / max(np.max(np.abs(xb)), np.max(np.abs(yb)))
            
            wing_outer = np.column_stack((cx + xb * scale, cy + yb * scale))
            wing_inner = np.column_stack((cx + xb * scale * 0.6, cy + yb * scale * 0.6))

            polygons.append({
                'x_verts': x_verts,
                'wing_outer': wing_outer,
                'wing_inner': wing_inner,
                'cx': cx, 'cy': cy, 'p': p, 'label': label
            })

        # 4. Terapkan Simetri Titik Pusat (-x, -y) dengan label berisi Diagonal Kupu-kupu
        if is_central:
            place_item(best_x, best_y, f"({p},{p})\nd=0\nDg={diag_val:.1f}")
        else:
            place_item(best_x, best_y, f"({p},{q})\nd={d}\nDg={diag_val:.1f}")
            place_item(-best_x, -best_y, f"({q},{p})\nd={d}\nDg={diag_val:.1f}")
            
    return polygons, max_radius_fit

def plot_fractal_goldbach_crystal(n):
    if n % 2 != 0: n -= 1
    if n < 4:
        print("n harus bilangan genap >= 4")
        return
        
    primes = set(get_primes_up_to(n))
    groups = get_symmetric_groups(n, primes)

    if not groups: 
        print(f"Tidak ada partisi Goldbach untuk n={n}")
        return

    m = n // 2
    plt.style.use('dark_background')
    
    # Rasio window yang lebih lebar untuk menampung UI Teks Panel
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_aspect('equal')

    polygons_data, R_fit = calculate_crystal_packing(groups)

    # Lingkaran Semesta
    circle = plt.Circle((0, 0), R_fit, color='cyan', fill=False, lw=1.5, alpha=0.5, linestyle='-')
    ax.add_patch(circle)
    
    ax.axhline(0, color='white', lw=0.4, alpha=0.3, linestyle='--')
    ax.axvline(0, color='white', lw=0.4, alpha=0.3, linestyle='--')

    cmap_wing = plt.get_cmap('turbo')   
    cmap_core = plt.get_cmap('magma')   

    for poly_data in polygons_data:
        p, cx, cy = poly_data['p'], poly_data['cx'], poly_data['cy']
        
        ratio = p / m if m > 0 else 0
        
        # Gambar Layer Sayap
        poly_out = plt.Polygon(poly_data['wing_outer'], facecolor=cmap_wing(ratio), edgecolor='none', alpha=0.7)
        ax.add_patch(poly_out)
        
        poly_in = plt.Polygon(poly_data['wing_inner'], facecolor=cmap_core(1.0 - ratio), edgecolor='none', alpha=0.9)
        ax.add_patch(poly_in)
        
        # Gambar Tulang
        poly_x = plt.Polygon(poly_data['x_verts'], facecolor='white', edgecolor='cyan', lw=1.2, alpha=0.25)
        ax.add_patch(poly_x)
        
        # Kotak Pembatas
        bbox = plt.Rectangle((cx - p, cy - p), 2*p, 2*p, 
                             fill=False, edgecolor='white', lw=0.5, alpha=0.2, linestyle=':')
        ax.add_patch(bbox)
        
        # Label dengan detail baru
        fontsize = max(4, int((p / m) * 10)) if m > 0 else 6
        ax.text(cx, cy, poly_data['label'], 
                color='white', ha='center', va='center', 
                fontsize=fontsize, fontweight='bold', alpha=1.0,
                path_effects=[pe.withStroke(linewidth=2.5, foreground="black")])

    padding_view = R_fit * 1.05 if R_fit > 0 else 5
    ax.set_xlim(-padding_view, padding_view)
    ax.set_ylim(-padding_view, padding_view)
    ax.axis('off')

    plt.title(f"Butterfly Crystal Map of Goldbach Decomposition\n$n = {n}, \\quad m = {m}$", 
              color='gold', fontsize=18, pad=20, fontweight='bold')
              
    ax.text(0, -padding_view * 0.98, f"Deterministic Circular Tangent Packing (0 Gap)\nStructure: 'X' Skeleton with Fay's Butterfly Wings", 
            color='cyan', ha='center', fontsize=12, alpha=0.8)

    # ================= PANEL INFORMASI AKURAT =================
    d_vals = [g['d'] for g in groups]
    p_vals = [g['p'] for g in groups]
    
    info_text = (
        f" INFORMASI ANALISIS GOLDBACH\n"
        f" {'='*34}\n"
        f" Nilai n (Genap)  : {n}\n"
        f" Titik Tengah (m) : {m}\n"
        f" Total Pasangan   : {len(groups)}\n"
        f" {'='*34}\n\n"
        f" GEOMETRI LINGKARAN SEMESTA\n"
        f" {'='*34}\n"
        f" Jari-jari (R)    : {R_fit:.4f}\n"
        f" Diameter (D)     : {(2 * R_fit):.4f}\n"
        f" Keliling Lingk.  : {(2 * np.pi * R_fit):.4f}\n"
        f" Luas Area Lingk. : {(np.pi * R_fit**2):.4f}\n"
        f" {'='*34}\n\n"
        f" ANALISIS JARAK & DIAGONAL KUPU\n"
        f" {'='*34}\n"
        f" Jarak (d) Min/Max  : {min(d_vals)} / {max(d_vals)}\n"
        f" Jarak (d) Rata-rata: {(sum(d_vals)/len(d_vals)):.2f}\n\n"
        f" Sayap Utama Min (p): {min(p_vals)}\n"
        f" Sayap Utama Max (p): {max(p_vals)}\n"
        f" Diagonal (Dg) Min  : {(2 * min(p_vals) * np.sqrt(2)):.4f}\n"
        f" Diagonal (Dg) Max  : {(2 * max(p_vals) * np.sqrt(2)):.4f}\n"
        f" {'='*34}\n\n"
        f" MAKNA GEOMETRI DALAM GOLDBACH\n"
        f" {'='*34}\n"
        f" - Jarak (d): Simpangan prima dari m.\n"
        f" - Diagonal (Dg): Bentang mutlak sayap\n"
        f"   yang melambangkan energi prima p.\n"
        f" - Diameter (D): Total area probabilitas\n"
        f"   seluruh sebaran partisi n.\n"
        f" - 0-Gap: Konsistensi fraktal kristal.\n\n"
        f" RINCIAN PASANGAN (p, q):\n"
        f" {'-'*34}\n"
    )
    
    # Menampilkan hingga 12 pasangan di tabel panel
    for idx, g in enumerate(groups):
        p, q, d = g['p'], g['q'], g['d']
        diag = 2 * p * np.sqrt(2)
        if idx < 12:
            info_text += f"[{idx+1:02d}] ({p:^4}, {q:^4}) | d={d:<4} | Dg={diag:.1f}\n"
        elif idx == 12:
            info_text += f" ... dan {len(groups) - 12} pasangan lainnya\n"
            break
            
    # Membuat TextBox Panel di sebelah kiri menggunakan koordinat figure absolut
    fig.text(0.015, 0.5, info_text, 
             fontsize=10, color='white', va='center', ha='left',
             family='monospace',
             bbox=dict(facecolor='#0a192f', alpha=0.85, edgecolor='#00ffcc', boxstyle='round,pad=1', lw=1.5))
    # ==========================================================

    # Menggunakan rect di tight_layout agar plot utama menyisakan area kosong di sebelah kiri
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