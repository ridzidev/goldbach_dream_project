# Goldbach Dream Project 🦋🔢

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

> **Ridzi Butterfly Theory on Goldbach Conjecture Visualization** - Visualisasi kristal kupu-kupu untuk Konjektur Goldbach menggunakan pendekatan inovatif Ridzi Butterfly Theory.

## 📌 Deskripsi Projek / Project Description

**Goldbach Dream** adalah projek visualisasi matematika yang memvisualisasikan [Konjektur Goldbach](https://en.wikipedia.org/wiki/Goldbach%27s_conjecture) dalam bentuk kristal kupu-kupu yang menakjubkan. Projek ini menggunakan pendekatan inovatif berbasis **Ridzi Butterfly Theory** yang memposisikan setiap pasangan prima dalam susunan kristal melingkar tanpa celah (0-Gap Crystal Packing).

**Goldbach Dream** is a mathematical visualization project that visualizes the Goldbach Conjecture in the form of stunning butterfly crystals. This project uses the innovative approach of **Ridzi Butterfly Theory** which positions each prime pair in a circular crystal arrangement without gaps (0-Gap Crystal Packing).

## 🦋 Contoh Visualisasi / Visualization Example

<p align="center">
  <img src="Figure_1.png" alt="Butterfly Crystal for n=4034 (m=2017)" width="800">
</p>

<p align="center">
  <em>Butterfly Crystal Visualization untuk n=4034 (m=2017) | Ridzi Butterfly Theory</em>
</p>

### Konsep Utama / Main Concepts

- **Konjektur Goldbach**: Setiap bilangan genap lebih besar dari 2 dapat dinyatakan sebagai jumlah dua bilangan prima.
- **Ridzi Butterfly Theory**: Pendekatan midpoint `m = n/2` dengan jarak `d` untuk menemukan pasangan prima simetris.
- **Kristal Kupu-Kupu**: Visualisasi setiap pasangan prima sebagai kupu-kupu dengan sayap yang merepresentasikan besaran prima.

- **Goldbach Conjecture**: Every even number greater than 2 can be expressed as the sum of two prime numbers.
- **Ridzi Butterfly Theory**: Midpoint approach `m = n/2` with distance `d` to find symmetric prime pairs.
- **Butterfly Crystal**: Visualization of each prime pair as a butterfly with wings representing the prime magnitude.

---

## ✨ Fitur / Features

### 1. Visualisasi Kristal Kupu-Kupu / Butterfly Crystal Visualization (goldbach_dream.py)

| Fitur | Feature |
|-------|---------|
| Interface GUI interaktif menggunakan Tkinter | Interactive GUI interface using Tkinter |
| Visualisasi fraktal kristal kupu-kupu yang indah | Beautiful fractal butterfly crystal visualization |
| Tampilan 0-Gap Crystal Packing (tanpa tumpang tindih) | 0-Gap Crystal Packing display (without overlap) |
| Panel informasi lengkap dengan statistik | Complete information panel with statistics |
| Mode gelap (dark background) dengan warna cerah | Dark background mode with bright colors |

### 2. Generator Data / Data Generator (only_number.py)

| Fitur | Feature |
|-------|---------|
| Generate data untuk rentang bilangan genap | Generate data for even number ranges |
| Output CSV dengan analisis lengkap | CSV output with complete analysis |
| Statistik jarak (d), diagonal, radius semesta | Statistics for distance (d), diagonal, universe radius |
| Cocok untuk analisis data dan membuat grafik | Suitable for data analysis and charting |

---

## 📋 Requirements / Dependensi

### Python Version
```
Python 3.8 atau lebih tinggi / Python 3.8 or higher
```

### Library yang Dibutuhkan / Required Libraries

| Library | Versi / Version | Deskripsi / Description |
|---------|----------------|------------------------|
| `numpy` | ≥ 1.20.0 | Komputasi numerik dan array / Numerical computation and arrays |
| `matplotlib` | ≥ 3.5.0 | Visualisasi dan plotting / Visualization and plotting |
| `pandas` | ≥ 1.3.0 | Manipulasi dan analisis data / Data manipulation and analysis |
| `tkinter` | Built-in | GUI (sudah termasuk di Python / included in Python) |

---

## 🚀 Cara Install / Installation Guide

### Langkah 1: Clone Repository

```bash
git clone https://github.com/ridzidev/goldbach_dream_project.git
cd goldbach_dream_project
```

### Langkah 2: Buat Virtual Environment / Create Virtual Environment (Disarankan/Recommended)

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Langkah 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install satu per satu / Or install individually:

```bash
pip install numpy matplotlib pandas
```

### Langkah 4: Verifikasi Instalasi / Verify Installation

```bash
python -c "import numpy; import matplotlib; import pandas; print('✓ Semua library terinstall dengan baik! / ✓ All libraries installed successfully!')"
```

---

## 📖 Cara Menggunakan / How to Use

### 1. Menjalankan Visualisasi Kristal Kupu-Kupu / Run Butterfly Crystal Visualization

```bash
python goldbach_dream.py
```

**Langkah-langkah / Steps:**
1. Akan muncul dialog untuk input bilangan genap / A dialog will appear for even number input
2. Masukkan bilangan genap ≥ 4 (misal: 50, 100, 200) / Enter even number ≥ 4 (e.g., 50, 100, 200)
3. Klik OK / Click OK
4. Visualisasi kristal kupu-kupu akan muncul dalam jendela baru / Butterfly crystal visualization will appear in a new window

**Contoh Input / Example Input:**
```
Input an Even Integer n (n >= 4): 100
```

### 2. Menjalankan Generator Data CSV / Run CSV Data Generator

```bash
python only_number.py
```

**Langkah-langkah / Steps:**
1. Masukkan bilangan awal (misal: 10) / Enter start number (e.g., 10)
2. Masukkan bilangan akhir (misal: 200) / Enter end number (e.g., 200)
3. Program akan memproses dan menampilkan tabel di console / Program will process and display table in console
4. File CSV akan tersimpan otomatis / CSV file will be saved automatically

**Contoh Input / Example Input:**
```
Masukkan n Awal (misal: 10) : 10
Masukkan n Akhir (misal: 200): 200

Enter start n (e.g., 10): 10
Enter end n (e.g., 200): 200
```

**Output CSV yang dihasilkan / Generated CSV Output:**
| n (Genap/Even) | m (Titik Tengah/Midpoint) | Total Pasangan/Total Pairs | Jarak Min (d) | Jarak Max (d) | Radius Semesta (R) | ... |
|----------------|---------------------------|---------------------------|---------------|---------------|---------------------|-----|
| 10             | 5                         | 2                         | 0             | 3             | 14.14               | ... |
| 12             | 6                         | 2                         | 1             | 4             | 19.80               | ... |
| ...            | ...                       | ...                       | ...           | ...           | ...                 | ... |

---

## 📊 Output Contoh / Sample Output

### Visualisasi Kristal Kupu-Kupu / Butterfly Crystal Visualization

Visualisasi untuk n=4034 (m=2017) menampilkan / Visualization for n=4034 (m=2017) displays:
- Kristal kupu-kupu dengan berbagai ukuran / Butterfly crystals of various sizes
- Banyak pasangan prima Goldbach / Many Goldbach prime pairs
- Panel informasi statistik lengkap / Complete statistical information panel
- Mode gelap yang indah dengan warna-warna cerah / Beautiful dark mode with vibrant colors

### File CSV

File `goldbach_range_4_to_100.csv` sudah termasuk dalam repository sebagai contoh output / Included in repository as sample output.

---

## 🧮 Penjelasan Matematika / Mathematical Explanation (Ridzi Butterfly Theory)

### Konsep Dasar Ridzi Butterfly Theory / Basic Concept of Ridzi Butterfly Theory

Untuk bilangan genap `n` / For even number `n`:
1. Hitung midpoint: `m = n / 2` (Titik Tengah / Midpoint)
2. Untuk setiap jarak `d` dari 0 hingga `m-1` / For each distance `d` from 0 to `m-1`:
   - `p = m - d` (prima kecil / sayap kiri - small prime / left wing)
   - `q = m + d` (prima besar / sayap kanan - large prime / right wing)
3. Jika `p` dan `q` keduanya prima, maka `(p, q)` adalah pasangan Goldbach / If both `p` and `q` are prime, then `(p, q)` is a Goldbach pair

### Istilah Penting dalam Ridzi Butterfly Theory / Important Terms in Ridzi Butterfly Theory

| Istilah / Term | Simbol / Symbol | Deskripsi / Description |
|----------------|-----------------|-------------------------|
| Titik Tengah / Midpoint | `m = n/2` | Titik tengah dari bilangan genap n / Midpoint of even number n |
| Jarak / Distance | `d` | Jarak prima dari titik tengah m / Prime distance from midpoint m |
| Prima Kecil / Small Prime | `p = m - d` | Prima bagian kiri (sayap kecil) / Left prime (small wing) |
| Prima Besar / Large Prime | `q = m + d` | Prima bagian kanan (sayap besar) / Right prime (large wing) |
| Diagonal Kupu / Butterfly Diagonal | `Dg = 2p√2` | Bentang sayap kupu-kupu / Butterfly wing span |
| Radius Semesta / Universe Radius | `R` | Jari-jari kristal lingkaran / Circular crystal radius |
| Diameter Semesta / Universe Diameter | `D = 2R` | Diameter kristal lingkaran / Circular crystal diameter |

### Kristal Packing (0-Gap)

- Setiap pasangan prima direpresentasikan sebagai kotak dengan lebar `W = 2p` / Each prime pair is represented as a box with width `W = 2p`
- Kotak-kotak ditempatkan dalam lingkaran tanpa tumpang tindih (0-Gap) / Boxes are placed in a circle without overlap (0-Gap)
- Menggunakan algoritma tangent point detection untuk positioning / Uses tangent point detection algorithm for positioning

### Butterfly Wings (Sayap Kupu-Kupu)

- Sayap menggunakan persamaan parametrik: `r = exp(sin(θ)) - 2*cos(4θ) + sin((2θ - π)/24)⁵` / Wings use parametric equation
- Skala sayap proporsional dengan nilai prima `p` / Wing scale is proportional to prime value `p`
- Memberikan visualisasi fraktal yang indah / Provides beautiful fractal visualization

---

## 📁 Struktur File / File Structure

```
goldbach_dream_project/
├── README.md                     # Dokumentasi lengkap / Complete documentation
├── goldbach_dream.py            # Visualisasi kristal kupu-kupu / Butterfly crystal visualization
├── only_number.py               # Generator data CSV / CSV data generator
├── goldbach_range_4_to_100.csv  # Contoh output CSV / Sample CSV output
├── requirements.txt             # Daftar dependensi / Dependency list
└── Figure_1.png                 # Contoh visualisasi n=4034 / Sample visualization n=4034
```

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'numpy'"

```bash
pip install numpy matplotlib pandas
```

### Error: "tkinter tidak ditemukan" / "tkinter not found"

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3-tkinter
```

**macOS/Windows:**
Biasanya sudah termasuk. Coba reinstall Python dari python.org / Usually included. Try reinstalling Python from python.org

### Error saat menjalankan di Python 2 / Error when running on Python 2

Pastikan menggunakan Python 3 / Make sure to use Python 3:
```bash
python3 goldbach_dream.py
python3 only_number.py
```

---

## 🤝 Kontribusi / Contributing

1. Fork repository ini / Fork this repository
2. Buat branch baru / Create new branch (`git checkout -b feature-anda`)
3. Commit perubahan / Commit changes (`git commit -m 'Menambah fitur baru'`)
4. Push ke branch / Push to branch (`git push origin feature-anda`)
5. Buat Pull Request / Create Pull Request

---

## 📝 Lisensi / License

Projek ini dilisensikan di bawah **MIT License** - lihat file [LICENSE](LICENSE) untuk detail.

This project is licensed under **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Ridzidev**
- GitHub: [@ridzidev](https://github.com/ridzidev)

---

## 🙏 Acknowledgments

- Algoritma Sieve of Eratosthenes untuk pencarian prima / Sieve of Eratosthenes algorithm for prime finding
- Konsep fraktal kupu-kupu (Fay's Butterfly) / Butterfly fractal concept (Fay's Butterfly)
- Semua kontributor dan pengguna projek ini / All contributors and users of this project

---

<p align="center">
  Dibuat dengan ❤️ untuk Matematika dan Seni / Made with ❤️ for Mathematics and Art
</p>

