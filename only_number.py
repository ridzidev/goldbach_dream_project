import numpy as np
import pandas as pd
import math
import time

# ==========================================
# 1. LOGIKA MATEMATIKA DASAR
# ==========================================

def get_primes_up_to(limit):
    """Sieve of Eratosthenes untuk mencari prima."""
    if limit < 2: return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def get_goldbach_partitions(n, primes_set):
    """Mendapatkan semua pasangan Goldbach untuk n tertentu."""
    m = n // 2
    groups = []
    
    # Mencari pasangan (p, q) berdasarkan jarak d dari m
    for d_val in range(m - 1):
        p = m - d_val
        q = m + d_val
        if p in primes_set and q in primes_set:
            groups.append({
                'p': p, 'q': q,
                'd': d_val,
                'is_central': (d_val == 0)
            })
            
    # Urutkan berdasarkan jarak d (Ascending) -> Penting untuk algoritma packing
    groups.sort(key=lambda g: g['d'])
    return groups

# ==========================================
# 2. SIMULASI PACKING (TANPA GAMBAR)
# ==========================================

def calculate_universe_metrics(groups):
    """
    Menjalankan simulasi penempatan '0-Gap' secara virtual 
    hanya untuk mendapatkan Jari-jari Semesta (R_fit).
    """
    placed_xy = []
    max_dist_universe = 0.0
    eps = 1e-6 

    for g in groups:
        p, is_central = g['p'], g['is_central']
        W = 2 * p  # Lebar bounding box
        
        candidates = []
        
        # 1. Posisi Awal
        if not placed_xy:
            if is_central:
                candidates.append((0.0, 0.0))
            else:
                candidates.append((W/2.0, 0.0))
        else:
            # 2. Cari titik singgung
            U_edges = [0.0]
            V_edges = [0.0]
            for P in placed_xy:
                half = (P['W'] + W) / 2.0
                U_edges.extend([P['x'] - half, P['x'] + half])
                V_edges.extend([P['y'] - half, P['y'] + half])
            
            for x_cand in U_edges:
                for y_cand in V_edges:
                    if not is_central and max(abs(x_cand), abs(y_cand)) < (W / 2.0) - eps:
                        continue
                    
                    valid = True
                    for P in placed_xy:
                        half = (P['W'] + W) / 2.0
                        if abs(x_cand - P['x']) < half - eps and abs(y_cand - P['y']) < half - eps:
                            valid = False
                            break
                    
                    if valid:
                        candidates.append((x_cand, y_cand))
        
        # 3. Pilih kandidat terdekat ke pusat
        if candidates:
            candidates.sort(key=lambda c: (round(c[0]**2 + c[1]**2, 5), round(abs(c[0]), 5)))
            best_x, best_y = candidates[0]
        else:
            best_x, best_y = (0, 0)
            
        # Simpan posisi
        placed_xy.append({'x': best_x, 'y': best_y, 'W': W})
        
        # Update Jari-jari Semesta (R)
        # Jarak dari pusat (0,0) ke titik terjauh pada bounding box item ini
        # Jarak pusat item + setengah diagonal item
        dist_center = math.sqrt(best_x**2 + best_y**2)
        half_diag = p * math.sqrt(2) # diagonal dari pusat item ke sudut item
        max_dist_universe = max(max_dist_universe, dist_center + half_diag)
        
        # Simulasi simetri (tidak perlu hitung posisi, cukup tahu radiusnya sama)
        
    return max_dist_universe

# ==========================================
# 3. ENGINE UTAMA (LOOP RENTANG)
# ==========================================

def generate_range_data(start_n, end_n):
    # Pastikan genap
    if start_n % 2 != 0: start_n += 1
    
    print(f"Sedang memproses rentang n = {start_n} hingga {end_n}...")
    print("Mohon tunggu, sedang melakukan kalkulasi geometri...")
    
    # Pre-calculate primes untuk kecepatan
    all_primes = set(get_primes_up_to(end_n))
    
    data_rows = []
    
    start_time = time.time()
    
    for n in range(start_n, end_n + 1, 2):
        # 1. Dapatkan partisi
        groups = get_goldbach_partitions(n, all_primes)
        
        if not groups:
            continue
            
        m = n // 2
        count_pairs = len(groups)
        
        # 2. Statistik Jarak (d)
        d_values = [g['d'] for g in groups]
        min_d = min(d_values)
        max_d = max(d_values)
        avg_d = sum(d_values) / count_pairs
        
        # 3. Statistik Diagonal Kupu-kupu (Dg)
        # Dg = 2 * p * sqrt(2)
        p_values = [g['p'] for g in groups]
        max_p = max(p_values) # Biasanya pasangan pusat atau dekat pusat
        min_p = min(p_values) # Biasanya pasangan terluar (d terbesar)
        
        max_diag = 2 * max_p * math.sqrt(2)
        min_diag = 2 * min_p * math.sqrt(2)
        
        # 4. Hitung Radius Semesta (Simulasi Packing)
        universe_radius = calculate_universe_metrics(groups)
        universe_diameter = universe_radius * 2
        
        # 5. Susun Baris Data
        row = {
            'n (Genap)': n,
            'm (Titik Tengah)': m,
            'Total Pasangan': count_pairs,
            'Jarak Min (d)': min_d,
            'Jarak Max (d)': max_d,
            'Jarak Rata2 (d)': round(avg_d, 2),
            'Diagonal Max (Dg)': round(max_diag, 4),
            'Diagonal Min (Dg)': round(min_diag, 4),
            'Radius Semesta (R)': round(universe_radius, 4),
            'Diameter Semesta (D)': round(universe_diameter, 4),
            'Kepadatan (N/D)': round(count_pairs / universe_diameter, 4) # Rasio jumlah partisi terhadap ukuran ruang
        }
        data_rows.append(row)

    elapsed = time.time() - start_time
    print(f"\nSelesai dalam {elapsed:.2f} detik.")
    
    # Buat DataFrame
    df = pd.DataFrame(data_rows)
    return df

# ==========================================
# 4. EKSEKUSI
# ==========================================

if __name__ == "__main__":
    try:
        print("--- GENERATOR TABEL DATA GOLDBACH ---")
        s_input = int(input("Masukkan n Awal (misal: 10) : "))
        e_input = int(input("Masukkan n Akhir (misal: 200): "))
        
        if s_input < 4: s_input = 4
        if e_input < s_input: 
            print("Error: n Akhir harus lebih besar dari n Awal.")
        else:
            df_result = generate_range_data(s_input, e_input)
            
            # Tampilkan Tabel di Konsol
            print("\n=== TABEL REKAPITULASI DATA ===")
            # Mengatur tampilan pandas agar semua kolom terlihat
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(df_result.to_string(index=False))
            
            # Simpan ke CSV
            filename = f"goldbach_range_{s_input}_to_{e_input}.csv"
            df_result.to_csv(filename, index=False)
            print(f"\n[SUKSES] File CSV tersimpan: {filename}")
            print("Anda bisa membuka file ini di Excel untuk membuat grafik perbandingan.")
            
    except ValueError:
        print("Input harus berupa angka bulat.")
    except ImportError:
        print("Modul 'pandas' belum terinstall. Silakan install dengan: pip install pandas")