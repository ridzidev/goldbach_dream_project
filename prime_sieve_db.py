import math
import os
import sqlite3
import sys
import time
from itertools import compress

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "primes.db"
)


def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS primes (
            idx INTEGER PRIMARY KEY,
            value INTEGER NOT NULL UNIQUE
        )
        """
    )
    conn.commit()


def _upper_bound_nth_prime(n: int) -> int:
    """Batas atas eksak Rosser-Schoenfeld untuk bilangan prima ke-n."""
    if n < 6:
        return 15
    ln_n = math.log(n)
    return int(n * (ln_n + math.log(ln_n))) + 64


def _simple_odd_sieve(limit: int) -> list[int]:
    """Menghasilkan prima ganjil <= limit untuk basis segmented sieve."""
    if limit < 3:
        return []
    size = (limit - 3) // 2 + 1
    buf = bytearray(b"\x01") * size
    sqrt_limit = math.isqrt(limit)
    for i in range((sqrt_limit - 3) // 2 + 1):
        if buf[i]:
            p = 2 * i + 3
            start_idx = (p * p - 3) // 2
            count = (size - 1 - start_idx) // p + 1
            buf[start_idx::p] = b"\x00" * count
    return list(compress(range(3, limit + 1, 2), buf))


def _sieve_odd_range(start_odd: int, end_odd: int, chunk_odds: int = 262_144) -> list[int]:
    """Segmented sieve khusus bilangan ganjil pada rentang [start_odd, end_odd]."""
    if start_odd > end_odd:
        return []
    if start_odd < 3:
        start_odd = 3
    if start_odd % 2 == 0:
        start_odd += 1
    if end_odd % 2 == 0:
        end_odd -= 1
    if start_odd > end_odd:
        return []

    base_primes = _simple_odd_sieve(math.isqrt(end_odd))
    result: list[int] = []

    seg_low = start_odd
    step_span = (chunk_odds - 1) * 2
    while seg_low <= end_odd:
        seg_high = min(end_odd, seg_low + step_span)
        size = (seg_high - seg_low) // 2 + 1
        buf = bytearray(b"\x01") * size

        limit_p = math.isqrt(seg_high)
        for p in base_primes:
            if p > limit_p:
                break
            m = ((seg_low + p - 1) // p) * p
            if m < p * p:
                m = p * p
            if m % 2 == 0:
                m += p
            if m <= seg_high:
                start_idx = (m - seg_low) // 2
                count = (size - 1 - start_idx) // p + 1
                buf[start_idx::p] = b"\x00" * count

        result.extend(compress(range(seg_low, seg_high + 1, 2), buf))
        seg_low = seg_high + 2

    return result


def get_db_stats(db_path: str = DEFAULT_DB_PATH) -> tuple[int, int]:
    """Mengembalikan (jumlah_prima_di_db, nilai_prima_terbesar)."""
    with sqlite3.connect(db_path) as conn:
        _init_db(conn)
        row = conn.execute(
            "SELECT COALESCE(MAX(idx), 0), COALESCE(MAX(value), 0) FROM primes"
        ).fetchone()
        return int(row[0]), int(row[1])


def ensure_primes_count(
    target_n: int, db_path: str = DEFAULT_DB_PATH
) -> tuple[list[int], bool, int, int]:
    """
    Memastikan database memiliki minimal target_n bilangan prima.
    Mengembalikan: (list_prima_1_sampai_n, apakah_generate_baru, total_di_db, jumlah_baru_ditambah)
    """
    if target_n < 1:
        return [], False, 0, 0

    with sqlite3.connect(db_path) as conn:
        _init_db(conn)
        current_count, last_val = conn.execute(
            "SELECT COALESCE(MAX(idx), 0), COALESCE(MAX(value), 0) FROM primes"
        ).fetchone()
        current_count = int(current_count)
        last_val = int(last_val)

        if current_count >= target_n:
            rows = conn.execute(
                "SELECT value FROM primes WHERE idx <= ? ORDER BY idx ASC", (target_n,)
            ).fetchall()
            return [r[0] for r in rows], False, current_count, 0

        existing: list[int] = []
        if current_count > 0:
            rows = conn.execute(
                "SELECT value FROM primes ORDER BY idx ASC"
            ).fetchall()
            existing = [r[0] for r in rows]

        new_primes: list[int] = []
        if current_count == 0:
            new_primes.append(2)
            start_odd = 3
        elif last_val == 2:
            start_odd = 3
        else:
            start_odd = last_val + 2

        limit = max(_upper_bound_nth_prime(target_n), start_odd + 1024)
        while current_count + len(new_primes) < target_n:
            batch = _sieve_odd_range(start_odd, limit)
            new_primes.extend(batch)
            if current_count + len(new_primes) >= target_n:
                break
            start_odd = (limit + 2) if limit % 2 == 1 else (limit + 1)
            limit = max(limit * 2, start_odd + 65_536)

        conn.executemany(
            "INSERT INTO primes (idx, value) VALUES (?, ?)",
            enumerate(new_primes, start=current_count + 1),
        )
        conn.commit()

        total_in_db = current_count + len(new_primes)
        all_primes = existing + new_primes
        return all_primes[:target_n], True, total_in_db, len(new_primes)


def ensure_primes_up_to_value(
    max_val: int, db_path: str = DEFAULT_DB_PATH
) -> tuple[int, int]:
    """Mengisi database dengan seluruh bilangan prima <= max_val."""
    if max_val < 2:
        return get_db_stats(db_path)[0], 0

    with sqlite3.connect(db_path) as conn:
        _init_db(conn)
        current_count, last_val = conn.execute(
            "SELECT COALESCE(MAX(idx), 0), COALESCE(MAX(value), 0) FROM primes"
        ).fetchone()
        current_count = int(current_count)
        last_val = int(last_val)

        if last_val >= max_val:
            return current_count, 0

        new_primes: list[int] = []
        if current_count == 0:
            new_primes.append(2)
            start_odd = 3
        elif last_val == 2:
            start_odd = 3
        else:
            start_odd = last_val + 2

        if start_odd <= max_val:
            new_primes.extend(_sieve_odd_range(start_odd, max_val))

        if new_primes:
            conn.executemany(
                "INSERT INTO primes (idx, value) VALUES (?, ?)",
                enumerate(new_primes, start=current_count + 1),
            )
            conn.commit()

        return current_count + len(new_primes), len(new_primes)


def main() -> None:
    print("=== Generator Database Bilangan Prima (SQLite + Segmented Sieve) ===")
    total_now, max_p_now = get_db_stats()
    print(f"Status DB saat ini ({DEFAULT_DB_PATH}): {total_now:,} prima (terbesar: {max_p_now:,})")

    if len(sys.argv) >= 2:
        try:
            target_n = int(sys.argv[1])
        except ValueError:
            print("Argumen harus berupa bilangan bulat (jumlah prima n).")
            return
        t0 = time.perf_counter()
        primes, generated, total_db, added = ensure_primes_count(target_n)
        dt = (time.perf_counter() - t0) * 1000
        status = f"Ditambah {added:,} prima baru" if generated else "Sudah tersedia di DB"
        print(f"Selesai dalam {dt:.2f} ms | {status} | Total di DB: {total_db:,} | p_{target_n} = {primes[-1]:,}")
        return

    print("Pilih mode pengisian:")
    print("  1. Berdasarkan jumlah prima (n prima pertama)")
    print("  2. Berdasarkan batas nilai maksimum (prima <= X)")
    mode = input("Pilihan (1/2): ").strip()

    if mode == "1":
        target_n = int(input("Masukkan jumlah prima n: ").strip())
        t0 = time.perf_counter()
        primes, generated, total_db, added = ensure_primes_count(target_n)
        dt = (time.perf_counter() - t0) * 1000
        print(f"Selesai dalam {dt:.2f} ms | Prima baru: {added:,} | Total DB: {total_db:,} | p_{target_n} = {primes[-1]:,}")
    elif mode == "2":
        max_val = int(input("Masukkan batas nilai maksimum X: ").strip())
        t0 = time.perf_counter()
        total_db, added = ensure_primes_up_to_value(max_val)
        dt = (time.perf_counter() - t0) * 1000
        _, max_p = get_db_stats()
        print(f"Selesai dalam {dt:.2f} ms | Prima baru: {added:,} | Total DB: {total_db:,} | Terbesar: {max_p:,}")
    else:
        print("Pilihan tidak dikenali.")


if __name__ == "__main__":
    main()