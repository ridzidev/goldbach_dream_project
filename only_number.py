import numpy as np
import pandas as pd
import math
import time

# ==========================================
# 1. BASIC MATHEMATICAL LOGIC
# ==========================================

def get_primes_up_to(limit):
    """Sieve of Eratosthenes for finding primes."""
    if limit < 2: return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def get_goldbach_partitions(n, primes_set):
    """Get all Goldbach partitions for a given n."""
    m = n // 2
    groups = []
    
    # Find pairs (p, q) based on distance d from m
    for d_val in range(m - 1):
        p = m - d_val
        q = m + d_val
        if p in primes_set and q in primes_set:
            groups.append({
                'p': p, 'q': q,
                'd': d_val,
                'is_central': (d_val == 0)
            })
            
    # Sort by distance d (Ascending) -> Important for packing algorithm
    groups.sort(key=lambda g: g['d'])
    return groups

# ==========================================
# 2. PACKING SIMULATION (WITHOUT VISUALIZATION)
# ==========================================

def calculate_universe_metrics(groups):
    """
    Runs virtual 0-Gap placement simulation 
    only to get Universe Radius (R_fit).
    """
    placed_xy = []
    max_dist_universe = 0.0
    eps = 1e-6 

    for g in groups:
        p, is_central = g['p'], g['is_central']
        W = 2 * p  # Bounding box width
        
        candidates = []
        
        # 1. Initial Position
        if not placed_xy:
            if is_central:
                candidates.append((0.0, 0.0))
            else:
                candidates.append((W/2.0, 0.0))
        else:
            # 2. Find tangent points
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
        
        # 3. Select closest candidate to center
        if candidates:
            candidates.sort(key=lambda c: (round(c[0]**2 + c[1]**2, 5), round(abs(c[0]), 5)))
            best_x, best_y = candidates[0]
        else:
            best_x, best_y = (0, 0)
            
        # Store position
        placed_xy.append({'x': best_x, 'y': best_y, 'W': W})
        
        # Update Universe Radius (R)
        # Distance from center (0,0) to farthest point on this item's bounding box
        # Item center distance + half diagonal of item
        dist_center = math.sqrt(best_x**2 + best_y**2)
        half_diag = p * math.sqrt(2) # diagonal from item center to corner
        max_dist_universe = max(max_dist_universe, dist_center + half_diag)
        
        # Symmetry simulation (no need to calculate position, just know radius is the same)
        
    return max_dist_universe

# ==========================================
# 3. MAIN ENGINE (RANGE LOOP)
# ==========================================

def generate_range_data(start_n, end_n):
    # Ensure even
    if start_n % 2 != 0: start_n += 1
    
    print(f"Processing range n = {start_n} to {end_n}...")
    print("Please wait, performing geometry calculations...")
    
    # Pre-calculate primes for speed
    all_primes = set(get_primes_up_to(end_n))
    
    data_rows = []
    
    start_time = time.time()
    
    for n in range(start_n, end_n + 1, 2):
        # 1. Get partitions
        groups = get_goldbach_partitions(n, all_primes)
        
        if not groups:
            continue
            
        m = n // 2
        count_pairs = len(groups)
        
        # 2. Distance (d) Statistics
        d_values = [g['d'] for g in groups]
        min_d = min(d_values)
        max_d = max(d_values)
        avg_d = sum(d_values) / count_pairs
        
        # 3. Butterfly Diagonal (Dg) Statistics
        # Dg = 2 * p * sqrt(2)
        p_values = [g['p'] for g in groups]
        max_p = max(p_values) # Usually central pair or near center
        min_p = min(p_values) # Usually outermost pair (largest d)
        
        max_diag = 2 * max_p * math.sqrt(2)
        min_diag = 2 * min_p * math.sqrt(2)
        
        # 4. Calculate Universe Radius (Packing Simulation)
        universe_radius = calculate_universe_metrics(groups)
        universe_diameter = universe_radius * 2
        
        # 5. Compose Data Row
        row = {
            'n (Even)': n,
            'm (Midpoint)': m,
            'Total Pairs': count_pairs,
            'Distance Min (d)': min_d,
            'Distance Max (d)': max_d,
            'Distance Avg (d)': round(avg_d, 2),
            'Diagonal Max (Dg)': round(max_diag, 4),
            'Diagonal Min (Dg)': round(min_diag, 4),
            'Universe Radius (R)': round(universe_radius, 4),
            'Universe Diameter (D)': round(universe_diameter, 4),
            'Density (N/D)': round(count_pairs / universe_diameter, 4) # Ratio of partition count to space size
        }
        data_rows.append(row)

    elapsed = time.time() - start_time
    print(f"\nCompleted in {elapsed:.2f} seconds.")
    
    # Create DataFrame
    df = pd.DataFrame(data_rows)
    return df

# ==========================================
# 4. EXECUTION
# ==========================================

if __name__ == "__main__":
    try:
        print("--- GOLDBACH DATA TABLE GENERATOR ---")
        s_input = int(input("Enter start n (e.g., 10): "))
        e_input = int(input("Enter end n (e.g., 200): "))
        
        if s_input < 4: s_input = 4
        if e_input < s_input: 
            print("Error: End n must be greater than start n.")
        else:
            df_result = generate_range_data(s_input, e_input)
            
            # Display Table in Console
            print("\n=== DATA SUMMARY TABLE ===")
            # Setting pandas display to show all columns
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(df_result.to_string(index=False))
            
            # Save to CSV
            filename = f"goldbach_range_{s_input}_to_{e_input}.csv"
            df_result.to_csv(filename, index=False)
            print(f"\n[SUCCESS] CSV file saved: {filename}")
            print("You can open this file in Excel to create comparison charts.")
            
    except ValueError:
        print("Input must be an integer.")
    except ImportError:
        print("Module 'pandas' not installed. Please install with: pip install pandas")

