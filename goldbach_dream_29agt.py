import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

# ==============================================================================
# 1. PONDASI ARITMETIKA PRIMA
# ==============================================================================
def sieve_primes_up_to(limit):
    if limit < 2: return set()
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return set(np.nonzero(sieve)[0])

def get_goldbach_pairs(n, primes_set):
    m = n // 2
    pairs = []
    for d in range(m - 1):
        p, q = m - d, m + d
        if p in primes_set and q in primes_set:
            pairs.append({'d': d, 'p': p, 'q': q, 'is_central': (d == 0)})
    pairs.sort(key=lambda x: x['d'])
    return pairs

# ==============================================================================
# 2. GENERATOR KUPU-KUPU FRAKTAL (Murni Geometri Tanpa Teks)
# ==============================================================================
def generate_butterfly_shapes(cx, cy, radius, angle=0.0):
    theta = np.linspace(0, 2*np.pi, 140)
    # Kurva harmonik sayap kristal Ridzi
    r_raw = np.exp(np.sin(theta)) - 2*np.cos(4*theta) + np.sin((2*theta - np.pi)/24)**5
    max_extent = np.max(np.abs(r_raw))
    r_safe = (r_raw / max_extent) * radius * 0.96

    xw = r_safe * np.cos(theta)
    yw = r_safe * np.sin(theta)

    cos_a, sin_a = np.cos(angle), np.sin(angle)
    x_rot = xw * cos_a - yw * sin_a + cx
    y_rot = xw * sin_a + yw * cos_a + cy
    wing_out = np.column_stack((x_rot, y_rot))

    # Sayap dalam bersinar (Glowing core)
    xi_rot = (xw * 0.55) * cos_a - (yw * 0.55) * sin_a + cx
    yi_rot = (xw * 0.55) * sin_a + (yw * 0.55) * cos_a + cy
    wing_in = np.column_stack((xi_rot, yi_rot))

    # Rangka Tulang Sumbu Simetri (Bone Cross)
    s = radius * 0.88
    t = radius * 0.20
    bone_raw = np.array([
        (s, s), (0, t), (-s, s), (-t, 0),
        (-s, -s), (0, -t), (s, -s), (t, 0), (s, s)
    ])
    bx = bone_raw[:, 0] * cos_a - bone_raw[:, 1] * sin_a + cx
    by = bone_raw[:, 0] * sin_a + bone_raw[:, 1] * cos_a + cy
    bone_poly = np.column_stack((bx, by))

    return wing_out, wing_in, bone_poly

# ==============================================================================
# 3. PACKING BEBAS TABRAKAN (Strict Zero-Overlap)
# ==============================================================================
def pack_crystal(n, pairs):
    m = n // 2
    R_universe = float(m)
    placed = []

    if not pairs:
        return placed, R_universe

    if len(pairs) == 1 and pairs[0]['is_central']:
        # KASUS TUNGGAL: 1 Kupu-kupu raksasa memenuhi seluruh semesta
        r_single = R_universe * 0.94
        w_out, w_in, bone = generate_butterfly_shapes(0, 0, r_single, 0)
        placed.append({'w_out': w_out, 'w_in': w_in, 'bone': bone, 'radius': r_single})
        return placed, R_universe

    start_idx = 0
    if pairs[0]['is_central']:
        # Nukleus Pusat
        r_core = R_universe * 0.48
        w_out, w_in, bone = generate_butterfly_shapes(0, 0, r_core, 0)
        placed.append({'cx': 0, 'cy': 0, 'radius': r_core, 'w_out': w_out, 'w_in': w_in, 'bone': bone})
        start_idx = 1

    angles_to_search = np.linspace(0, np.pi, 180, endpoint=False)

    for i in range(start_idx, len(pairs)):
        g = pairs[i]
        p = g['p']
        fraction_p = p / m
        target_r = max(R_universe * 0.40 * (fraction_p ** 1.2), R_universe * 0.04)
        current_r = target_r

        best_placement = None
        best_dist = float('inf')

        for attempt in range(12):
            for theta in angles_to_search:
                min_R_cand = 0.0
                cos_t, sin_t = np.cos(theta), np.sin(theta)

                for item in placed:
                    ix, iy, ir = item.get('cx', 0), item.get('cy', 0), item['radius']
                    req_dist = ir + current_r + 1e-4
                    dot = ix * cos_t + iy * sin_t
                    cross = -ix * sin_t + iy * cos_t

                    if abs(cross) < req_dist:
                        offset = np.sqrt(max(0.0, req_dist**2 - cross**2))
                        cand = dot + offset
                        if cand > min_R_cand:
                            min_R_cand = cand

                cand_x = min_R_cand * cos_t
                cand_y = min_R_cand * sin_t

                if min_R_cand + current_r > R_universe * 0.99 or 2 * min_R_cand < 2 * current_r:
                    continue

                collision = False
                for item in placed:
                    ix, iy, ir = item.get('cx', 0), item.get('cy', 0), item['radius']
                    if np.hypot(cand_x - ix, cand_y - iy) < (ir + current_r - 1e-4) or \
                       np.hypot(-cand_x - ix, -cand_y - iy) < (ir + current_r - 1e-4):
                        collision = True
                        break

                if not collision and min_R_cand < best_dist:
                    best_dist = min_R_cand
                    best_placement = (cand_x, cand_y, current_r, theta)

            if best_placement is not None:
                break
            current_r *= 0.88
            if current_r < R_universe * 0.035:
                break

        if best_placement is not None:
            bx, by, br, b_theta = best_placement
            w1_out, w1_in, b1 = generate_butterfly_shapes(bx, by, br, b_theta + np.pi/2)
            placed.append({'cx': bx, 'cy': by, 'radius': br, 'w_out': w1_out, 'w_in': w1_in, 'bone': b1})

            w2_out, w2_in, b2 = generate_butterfly_shapes(-bx, -by, br, b_theta + np.pi/2)
            placed.append({'cx': -bx, 'cy': -by, 'radius': br, 'w_out': w2_out, 'w_in': w2_in, 'bone': b2})

    return placed, R_universe

# ==============================================================================
# 4. APLIKASI GUI ANIMATOR INTERAKTIF
# ==============================================================================
class RidziButterflyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ridzi Butterfly Crystal Animator - Goldbach Growth")
        self.root.geometry("960x900")
        self.root.configure(bg="#030712")

        self.primes_cache = set()
        self.max_limit_cached = 0

        self.is_playing = False
        self.current_idx = 0
        self.even_sequence = []
        self.max_overall_radius = 10.0

        self.setup_ui()
        self.setup_canvas()

    def setup_ui(self):
        control_frame = tk.Frame(self.root, bg="#0B132B", padx=15, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Label & Entry Rentang
        lbl_range = tk.Label(control_frame, text="Rentang Genap (contoh 4:20):", 
                             fg="#00FFCC", bg="#0B132B", font=("Segoe UI", 11, "bold"))
        lbl_range.pack(side=tk.LEFT, padx=5)

        self.entry_range = tk.Entry(control_frame, font=("Segoe UI", 11, "bold"), 
                                    width=12, bg="#1C2541", fg="#FFFFFF", insertbackground="white")
        self.entry_range.insert(0, "4:30")
        self.entry_range.pack(side=tk.LEFT, padx=5)

        # Tombol Mulai / Play
        self.btn_play = tk.Button(control_frame, text="▶ Play", command=self.toggle_play,
                                  bg="#00E5FF", fg="#000000", font=("Segoe UI", 10, "bold"), width=9)
        self.btn_play.pack(side=tk.LEFT, padx=6)

        # Tombol Reset
        self.btn_reset = tk.Button(control_frame, text="🔄 Reset", command=self.reset_animation,
                                   bg="#FF0055", fg="#FFFFFF", font=("Segoe UI", 10, "bold"), width=8)
        self.btn_reset.pack(side=tk.LEFT, padx=6)

        # Slider Kecepatan Delay (ms)
        lbl_speed = tk.Label(control_frame, text="Speed (ms):", fg="#A0FFE6", bg="#0B132B", font=("Segoe UI", 9))
        lbl_speed.pack(side=tk.LEFT, padx=(15, 2))

        self.speed_slider = tk.Scale(control_frame, from_=50, to=1000, orient=tk.HORIZONTAL,
                                     bg="#0B132B", fg="#00FFCC", highlightthickness=0, length=120)
        self.speed_slider.set(250)
        self.speed_slider.pack(side=tk.LEFT, padx=5)

        # Info Status N
        self.lbl_status = tk.Label(control_frame, text="n = 4  (m = 2)", 
                                   fg="#FFE600", bg="#0B132B", font=("Consolas", 13, "bold"))
        self.lbl_status.pack(side=tk.RIGHT, padx=10)

    def setup_canvas(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8), facecolor="#02060E")
        self.ax.set_facecolor("#02060E")
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def parse_input_range(self):
        raw = self.entry_range.get().strip()
        sep = ":" if ":" in raw else ("-" if "-" in raw else ",")
        parts = raw.split(sep)
        if len(parts) != 2:
            raise ValueError("Gunakan format min:max (contoh: 4:20)")
        n_min = int(parts[0].strip())
        n_max = int(parts[1].strip())
        
        if n_min < 4: n_min = 4
        if n_min % 2 != 0: n_min += 1
        if n_max % 2 != 0: n_max -= 1
        if n_min > n_max:
            raise ValueError("Batas bawah harus <= batas atas!")
        return n_min, n_max

    def prepare_data(self):
        n_min, n_max = self.parse_input_range()
        if n_max > self.max_limit_cached:
            self.primes_cache = sieve_primes_up_to(n_max + 100)
            self.max_limit_cached = n_max + 100

        self.even_sequence = list(range(n_min, n_max + 1, 2))
        self.current_idx = 0
        self.max_overall_radius = float(n_max // 2)

    def draw_frame(self, n):
        m = n // 2
        pairs = get_goldbach_pairs(n, self.primes_cache)
        placed_butterflies, R_universe = pack_crystal(n, pairs)

        self.ax.clear()
        self.ax.set_facecolor("#02060E")
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # 1. Lingkaran Semesta Aktif (Tumbuh Membesar)
        u_circle = Circle((0, 0), R_universe, edgecolor="#00FFCC", facecolor="#001824",
                          lw=2.2, alpha=0.95, zorder=1)
        self.ax.add_patch(u_circle)

        # 2. Render Kupu-Kupu Murni Tanpa Teks
        placed_butterflies.sort(key=lambda b: b['radius'], reverse=True)
        for b in placed_butterflies:
            rad = b['radius']
            ratio = rad / (R_universe * 0.48) if R_universe > 0 else 0.5
            color_val = plt.cm.viridis(max(0.18, min(0.95, ratio)))

            # Sayap Luar
            self.ax.add_patch(Polygon(b['w_out'], facecolor=color_val, edgecolor="#00FFAA",
                                      lw=0.8, alpha=0.75, zorder=3))
            # Sayap Dalam (Glow)
            self.ax.add_patch(Polygon(b['w_in'], facecolor="#FFFFFF", edgecolor="#80FFFF",
                                      lw=0.4, alpha=0.45, zorder=4))
            # Rangka Tulang Sumbu Simetri
            self.ax.add_patch(Polygon(b['bone'], edgecolor="#00FFFF", facecolor="none",
                                      lw=0.7, alpha=0.85, zorder=5))

        # Batas Kanvas Terkunci pada Skala Maksimum n_max agar Terlihat Efek Pertumbuhan
        view_limit = self.max_overall_radius * 1.08
        self.ax.set_xlim(-view_limit, view_limit)
        self.ax.set_ylim(-view_limit, view_limit)

        self.lbl_status.config(text=f"n = {n}  (m = {m})  |  Pairs: {len(pairs)}")
        self.canvas.draw_idle()

    def animation_loop(self):
        if not self.is_playing:
            return

        if self.current_idx < len(self.even_sequence):
            current_n = self.even_sequence[self.current_idx]
            self.draw_frame(current_n)
            self.current_idx += 1
            delay = self.speed_slider.get()
            self.root.after(delay, self.animation_loop)
        else:
            # Loop selesai, tombol kembali ke Play
            self.is_playing = False
            self.btn_play.config(text="▶ Replay", bg="#00E5FF")

    def toggle_play(self):
        if not self.is_playing:
            try:
                if self.current_idx == 0 or self.current_idx >= len(self.even_sequence):
                    self.prepare_data()
                self.is_playing = True
                self.btn_play.config(text="⏸ Pause", bg="#FFAA00")
                self.animation_loop()
            except Exception as e:
                messagebox.showerror("Error Input", str(e))
        else:
            self.is_playing = False
            self.btn_play.config(text="▶ Resume", bg="#00E5FF")

    def reset_animation(self):
        self.is_playing = False
        self.btn_play.config(text="▶ Play", bg="#00E5FF")
        self.current_idx = 0
        try:
            self.prepare_data()
            if self.even_sequence:
                self.draw_frame(self.even_sequence[0])
        except Exception:
            pass

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = RidziButterflyApp(root)
    root.mainloop()