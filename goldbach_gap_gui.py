import csv
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from prime_sieve_db import DEFAULT_DB_PATH, ensure_primes_count, get_db_stats


def popcount(x: int) -> int:
    return x.bit_count() if hasattr(x, "bit_count") else bin(x).count("1")


def decode_even_mask(mask: int, limit: int | None = None) -> list[int]:
    """Mengubah bitmask menjadi daftar bilangan genap terurut (bit i -> 2*i + 2)."""
    res: list[int] = []
    while mask:
        lsb = mask & -mask
        idx = lsb.bit_length() - 1
        res.append((idx << 1) + 2)
        mask ^= lsb
        if limit is not None and len(res) >= limit:
            break
    return res


def format_even_preview(mask: int, total_count: int, max_full: int = 200) -> str:
    if total_count == 0:
        return "{}"
    if total_count <= max_full:
        return ",".join(map(str, decode_even_mask(mask)))
    head = decode_even_mask(mask, limit=12)
    max_val = ((mask.bit_length() - 1) << 1) + 2
    return f"{','.join(map(str, head))},...,{max_val} [{total_count} angka]"


def format_primes_preview(primes_slice: list[int], max_full: int = 200) -> str:
    n = len(primes_slice)
    if n <= max_full:
        return ",".join(map(str, primes_slice))
    head = ",".join(map(str, primes_slice[:12]))
    return f"{head},...,{primes_slice[-1]} [{n} prima]"


class GoldbachGapApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Eksplorasi Himpunan Prima, Genap, dan Gap (SQLite + Bitmask)")
        self.root.geometry("1120x700")
        self.root.minsize(880, 540)

        self.primes: list[int] = []
        self.results: list[dict] = []
        self._build_ui()
        self.run_calculation()

    def _build_ui(self) -> None:
        input_frame = ttk.LabelFrame(self.root, text="Parameter Input & Cache SQLite", padding=10)
        input_frame.pack(fill=tk.X, padx=12, pady=(10, 6))

        ttk.Label(input_frame, text="min n:").pack(side=tk.LEFT, padx=(0, 5))
        self.min_n_var = tk.StringVar(value="1")
        self.min_entry = ttk.Entry(input_frame, textvariable=self.min_n_var, width=10)
        self.min_entry.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(input_frame, text="max n:").pack(side=tk.LEFT, padx=(0, 5))
        self.max_n_var = tk.StringVar(value="15")
        self.max_entry = ttk.Entry(input_frame, textvariable=self.max_n_var, width=10)
        self.max_entry.pack(side=tk.LEFT, padx=(0, 15))

        self.run_btn = ttk.Button(
            input_frame, text="Buat Tabel", command=self.run_calculation
        )
        self.run_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.export_btn = ttk.Button(
            input_frame, text="Ekspor CSV", command=self.export_csv
        )
        self.export_btn.pack(side=tk.LEFT, padx=(0, 15))

        self.db_info_var = tk.StringVar(value="")
        ttk.Label(input_frame, textvariable=self.db_info_var).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Siap.")
        ttk.Label(input_frame, textvariable=self.status_var).pack(
            side=tk.RIGHT, padx=(10, 0)
        )

        self.min_entry.bind("<Return>", lambda _e: self.run_calculation())
        self.max_entry.bind("<Return>", lambda _e: self.run_calculation())

        table_frame = ttk.Frame(self.root, padding=(12, 4))
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("n", "prima", "genap", "gap")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        self.tree.heading("n", text="n")
        self.tree.heading("prima", text="himpunan prima")
        self.tree.heading("genap", text="himpunan genap")
        self.tree.heading("gap", text="himpunan gap")

        self.tree.column("n", width=65, minwidth=50, anchor=tk.CENTER, stretch=False)
        self.tree.column("prima", width=260, minwidth=150, anchor=tk.W)
        self.tree.column("genap", width=470, minwidth=200, anchor=tk.W)
        self.tree.column("gap", width=260, minwidth=120, anchor=tk.W)

        y_scroll = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        x_scroll = ttk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        detail_frame = ttk.LabelFrame(
            self.root, text="Detail Baris Terpilih", padding=10
        )
        detail_frame.pack(fill=tk.BOTH, padx=12, pady=(4, 12))

        self.detail_text = tk.Text(
            detail_frame, height=8, wrap=tk.WORD, state=tk.DISABLED
        )
        detail_scroll = ttk.Scrollbar(
            detail_frame, orient=tk.VERTICAL, command=self.detail_text.yview
        )
        self.detail_text.configure(yscrollcommand=detail_scroll.set)

        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        detail_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        total_db, _ = get_db_stats(DEFAULT_DB_PATH)
        self.db_info_var.set(f"DB: {total_db:,} prima")

    def run_calculation(self) -> None:
        try:
            min_n = int(self.min_n_var.get().strip())
            max_n = int(self.max_n_var.get().strip())
        except ValueError:
            messagebox.showerror(
                "Input Tidak Valid", "min n dan max n harus berupa bilangan bulat."
            )
            return

        if min_n < 1:
            messagebox.showerror("Input Tidak Valid", "min n minimal bernilai 1.")
            return
        if max_n < min_n:
            messagebox.showerror(
                "Input Tidak Valid", "max n harus lebih besar atau sama dengan min n."
            )
            return

        self.status_var.set("Memuat / menghitung...")
        self.root.update_idletasks()

        t_start = time.perf_counter()

        # 1. Ambil dari SQLite; jika belum cukup, otomatis sieve & simpan ke SQLite
        primes, generated_new, total_db, added_count = ensure_primes_count(
            max_n, DEFAULT_DB_PATH
        )
        self.primes = primes
        self.db_info_var.set(f"DB: {total_db:,} prima")

        # 2. Bersihkan tabel lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.results.clear()

        # 3. Komputasi penjumlahan & gap berbasis Bitmask
        p_mask = 0
        even_mask = 0

        for k in range(1, max_n + 1):
            p_new = primes[k - 1]
            if p_new == 2:
                even_mask = 1 << 1  # angka 4
            else:
                idx_p = (p_new - 1) >> 1
                p_mask |= 1 << idx_p
                even_mask |= p_mask << idx_p

            if k >= min_n:
                full_mask = ((1 << p_new) - 1) ^ 1
                gap_mask = full_mask ^ even_mask

                count_genap = popcount(even_mask)
                count_gap = popcount(gap_mask)

                row_data = {
                    "n": k,
                    "p_max": p_new,
                    "max_even": 2 * p_new,
                    "even_mask": even_mask,
                    "gap_mask": gap_mask,
                    "count_genap": count_genap,
                    "count_gap": count_gap,
                }
                idx = len(self.results)
                self.results.append(row_data)

                disp_prima = format_primes_preview(primes[:k])
                disp_genap = format_even_preview(even_mask, count_genap)
                disp_gap = format_even_preview(gap_mask, count_gap)

                self.tree.insert(
                    "",
                    tk.END,
                    iid=str(idx),
                    values=(k, disp_prima, disp_genap, disp_gap),
                )

        elapsed_ms = (time.perf_counter() - t_start) * 1000
        sumber = f"+{added_count:,} prima baru ke DB" if generated_new else "dari cache DB"
        self.status_var.set(
            f"Selesai: {len(self.results)} baris dalam {elapsed_ms:.1f} ms ({sumber})"
        )

        if self.results:
            self.tree.selection_set("0")
            self.show_detail(0)

    def on_row_select(self, _event) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        self.show_detail(int(selected[0]))

    def show_detail(self, idx: int) -> None:
        row = self.results[idx]
        k = row["n"]

        prima_slice = self.primes[:k]
        prima_str = (
            ",".join(map(str, prima_slice))
            if k <= 15_000
            else f"{','.join(map(str, prima_slice[:1000]))} ... [total {k:,} prima, ekspor CSV untuk semua]"
        )

        if row["count_genap"] <= 20_000:
            genap_str = ",".join(map(str, decode_even_mask(row["even_mask"])))
        else:
            head = decode_even_mask(row["even_mask"], limit=1000)
            genap_str = (
                f"{','.join(map(str, head))} ... [total {row['count_genap']:,} angka genap, ekspor CSV untuk semua]"
            )

        if row["count_gap"] == 0:
            gap_str = "{}"
        elif row["count_gap"] <= 20_000:
            gap_str = ",".join(map(str, decode_even_mask(row["gap_mask"])))
        else:
            head_g = decode_even_mask(row["gap_mask"], limit=1000)
            gap_str = (
                f"{','.join(map(str, head_g))} ... [total {row['count_gap']:,} gap, ekspor CSV untuk semua]"
            )

        content = (
            f"n = {k}  |  p_max = {row['p_max']:,}  |  batas 2*p_max = {row['max_even']:,}  "
            f"|  jumlah genap = {row['count_genap']:,}  |  jumlah gap = {row['count_gap']:,}\n"
            f"{'-' * 90}\n"
            f"himpunan prima : {prima_str}\n\n"
            f"himpunan genap : {genap_str}\n\n"
            f"himpunan gap   : {gap_str}"
        )
        self.detail_text.configure(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert("1.0", content)
        self.detail_text.configure(state=tk.DISABLED)

    def export_csv(self) -> None:
        if not self.results:
            messagebox.showwarning("Data Kosong", "Belum ada data tabel untuk diekspor.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"goldbach_gap_n_{self.results[0]['n']}_to_{self.results[-1]['n']}.csv",
        )
        if not filepath:
            return

        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["n", "himpunan prima", "himpunan genap", "himpunan gap"])
            for row in self.results:
                k = row["n"]
                prima_str = ",".join(map(str, self.primes[:k]))
                genap_str = ",".join(map(str, decode_even_mask(row["even_mask"])))
                gap_str = (
                    ",".join(map(str, decode_even_mask(row["gap_mask"])))
                    if row["count_gap"] > 0
                    else "{}"
                )
                writer.writerow([k, prima_str, genap_str, gap_str])

        messagebox.showinfo("Berhasil", f"Tabel berhasil diekspor ke:\n{filepath}")


def main() -> None:
    root = tk.Tk()
    GoldbachGapApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()