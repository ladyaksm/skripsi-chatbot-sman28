import pandas as pd

def parse_excel(filepath):
    df_raw = pd.read_excel(filepath, header=None)
    df_raw = df_raw.fillna("")

    # DETEKSI baris pertama yang punya kolom valid (bukan Unnamed)
    header_row_idx = None
    for idx, row in df_raw.iterrows():
        labels = [str(v).strip().lower() for v in row.values]
        # Minimal harus ada 2 kolom yang bukan kosong dan bukan angka
        valid_labels = [
            v for v in labels 
            if v not in ["", "nan"] and not v.replace(".", "").isdigit()
        ]
        if len(valid_labels) >= 2:   # baris header pasti punya banyak label
            header_row_idx = idx
            break

    if header_row_idx is None:
        raise Exception("Gagal deteksi header Excel otomatis.")

    print("HEADER TERDETEKSI DI BARIS:", header_row_idx)

    # Baca excel dengan header
    df = pd.read_excel(filepath, header=header_row_idx)
    df = df.fillna("")

    # Bersihin kolom Unnamed tetap
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

    # Kolom yang TIDAK boleh di-ffill
    cols_no_ffill = ["nama", "kelas"]  # kolom personal tiap siswa (khusus data prestasi yang punya merge cell)

    # Tentukan kolom yang boleh di-ffill (metadata event)
    cols_to_ffill = [
        c for c in df.columns
        if c.lower() not in cols_no_ffill
    ]

    # Forward fill metadata event di kolom tertentu
    df[cols_to_ffill] = df[cols_to_ffill].replace("", pd.NA).ffill()

    # Konversi ke dict
    rows = df.to_dict(orient="records")
    return rows
