# Goldbach Dream Project 🦋🔢

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

> **Visualisasi Kristal Kupu-Kupu untuk Konjektur Goldbach** - Menvisualisasikan dekomposisi Goldbach dalam bentuk kristal kupu-kupu yang indah menggunakan teori M-Alfa Ridzi.

## 📌 Deskripsi Projek

**Goldbach Dream** adalah projek visualisasi matematika yang memvisualisasikan [Konjektur Goldbach](https://en.wikipedia.org/wiki/Goldbach%27s_conjecture) dalam bentuk kristal kupu-kupu yang menakjubkan. Projek ini menggunakan pendekatan inovatif berbasis teori "M-Alfa Ridzi" yang memposisikan setiap pasangan prima dalam susunan kristal melingkar tanpa celah (0-Gap Crystal Packing).

### Konsep Utama

- **Konjektur Goldbach**: Setiap bilangan genap lebih besar dari 2 dapat dinyatakan sebagai jumlah dua bilangan prima.
- **Teori M-Alfa Ridzi**: Pendekatan midpoint `m = n/2` dengan jarak `d` untuk menemukan pasangan prima simetris.
- **Kristal Kupu-Kupu**: Visualisasi setiap pasangan prima sebagai kupu-kupu dengan sayap yang merepresentasikan besaran prima.

---

## ✨ Fitur

### 1. Visualisasi Kristal Kupu-Kupu (goldbach_dream.py)
- Interface GUI interaktif menggunakan Tkinter
- Visualisasi fraktal kristal kupu-kupu yang indah
- Tampilan 0-Gap Crystal Packing (tanpa tumpang tindih)
- Panel informasi lengkap dengan statistik:
  - Jarak (d) Min/Max dan Rata-rata
  - Diagonal Kupu-kupu (Dg)
  - Radius dan Diameter Semesta
  - Rincian pasangan prima
- Mode gelap (dark background) dengan warna cerah

### 2. Generator Data (only_number.py)
- Generate data untuk rentang bilangan genap
- Output CSV dengan analisis lengkap:
  - Total pasangan Goldbach
  - Statistik jarak (d)
  - Statistik diagonal kupu-kupu
  - Radius dan Diameter Semesta
  - Kepadatan (N/D)
- Cocok untuk analisis data dan membuat grafik

---

## 📋 Requirements / Dependensi

### Python Version
```
Python 3.8 atau lebih tinggi
```

### Library yang Dibutuhkan

| Library | Versi | Deskripsi |
|---------|-------|-----------|
| `numpy` | ≥ 1.20.0 | Komputasi numerik dan array |
| `matplotlib` | ≥ 3.5.0 | Visualisasi dan plotting |
| `pandas` | ≥ 1.3.0 | Manipulasi dan analisis data |
| `tkinter` | Built-in | GUI (sudah termasuk di Python) |

---

## 🚀 Cara Install / Instalasi

### Langkah 1: Clone Repository

```bash
git clone https://github.com/ridzidev/goldbach_dream_project.git
cd goldbach_dream_project
```

### Langkah 2: Buat Virtual Environment (Disarankan)

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

Atau install satu per satu:

```bash
pip install numpy matplotlib pandas
```

### Langkah 4: Verifikasi Instalasi

```bash
python -c "import numpy; import matplotlib; import pandas; print('✓ Semua library terinstall dengan baik!')"
```

---

## 📖 Cara Menggunakan

### 1. Menjalankan Visualisasi Kristal Kupu-Kupu

```bash
python goldbach_dream.py
```

**Langkah-langkah:**
1. Akan muncul dialog untuk input bilangan genap
2. Masukkan bilangan genap ≥ 4 (misal: 50, 100, 200)
3. Klik OK
4. Visualisasi kristal kupu-kupu akan muncul dalam jendela baru

**Contoh Input:**
```
Input an Even Integer n (n >= 4): 100
```

### 2. Menjalankan Generator Data CSV

```bash
python only_number.py
```

**Langkah-langkah:**
1. Masukkan bilangan awal (misal: 10)
2. Masukkan bilangan akhir (misal: 200)
3. Program akan memproses dan menampilkan tabel di console
4. File CSV akan tersimpan otomatis

**Contoh Input:**
```
Masukkan n Awal (misal: 10) : 10
Masukkan n Akhir (misal: 200): 200
```

**Output CSV yang dihasilkan:**
| n (Genap) | m (Titik Tengah) | Total Pasangan | Jarak Min (d) | Jarak Max (d) | Radius Semesta (R) | ... |
|-----------|------------------|----------------|---------------|---------------|-------------------|-----|
| 10        | 5                | 2              | 0             | 3             | 14.14             | ... |
| 12        | 6                | 2              | 1             | 4             | 19.80             | ... |
| ...       | ...              | ...            | ...           | ...           | ...               | ... |

---

## 📊 Output Contoh

### Visualisasi Kristal Kupu-Kupu

Visualisasi untuk n=100 akan menampilkan:
- Kristal kupu-kupu dengan berbagai ukuran
- 27 pasangan prima Goldbach
- Panel informasi statistik lengkap
- Mode gelap yang indah dengan warna-warna cerah

### File CSV

File `goldbach_range_4_to_100.csv` sudah termasuk dalam repository sebagai contoh output.

---

## 🧮 Penjelasan Matematika

### Teori M-Alfa Ridzi

Untuk bilangan genap `n`:
1. Hitung midpoint: `m = n / 2`
2. Untuk setiap jarak `d` dari 0 hingga `m-1`:
   - `p = m - d` (prima kecil)
   - `q = m + d` (prima besar)
3. Jika `p` dan `q` keduanya prima, maka `(p, q)` adalah pasangan Goldbach

### Kristal Packing (0-Gap)

- Setiap pasangan prima direpresentasikan sebagai kotak dengan lebar `W = 2p`
- Kotak-kotak ditempatkan dalam lingkaran tanpa tumpang tindih (0-Gap)
- Menggunakan algoritma tangent point detection untuk positioning

### Butterfly Wings (Sayap Kupu-Kupu)

- Sayap menggunakan persamaan parametrik: `r = exp(sin(θ)) - 2*cos(4θ) + sin((2θ - π)/24)⁵`
- Skala sayap proporsional dengan nilai prima `p`
- Memberikan visualisasi fraktal yang indah

---

## 📁 Struktur File

```
goldbach_dream_project/
├── README.md                    # Dokumentasi lengkap
├── goldbach_dream.py           # Visualisasi kristal kupu-kupu
├── only_number.py              # Generator data CSV
├── goldbach_range_4_to_100.csv # Contoh output CSV
└── requirements.txt            # Daftar dependensi (opsional)
```

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'numpy'"

```bash
pip install numpy matplotlib pandas
```

### Error: "tkinter tidak ditemukan"

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3-tkinter
```

**macOS/Windows:**
Biasanya sudah termasuk. Coba reinstall Python dari python.org

### Error saat menjalankan di Python 2

Pastikan menggunakan Python 3:
```bash
python3 goldbach_dream.py
python3 only_number.py
```

---

## 🤝 Kontribusi

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature-anda`)
3. Commit perubahan (`git commit -m 'Menambah fitur baru'`)
4. Push ke branch (`git push origin feature-anda`)
5. Buat Pull Request

---

## 📝 Lisensi

Projek ini dilisensikan di bawah **MIT License** - lihat file [LICENSE](LICENSE) untuk detail.

---

## 👤 Author

**Ridzidev**
- GitHub: [@ridzidev](https://github.com/ridzidev)

---

## 🙏 Acknowledgments

- Algoritma Sieve of Eratosthenes untuk pencarian prima
- Konsep fraktal kupu-kupu (Fay's Butterfly)
- Semua kontributor dan pengguna projek ini

---

<p align="center">
  Dibuat dengan ❤️ untuk Matematika dan Seni
</p>

