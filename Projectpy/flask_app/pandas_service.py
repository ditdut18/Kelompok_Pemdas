import pandas as pd
import os

# Konfigurasi path file
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE_PATH = os.path.join(DATA_DIR, "jumlah_penderita_diabetes_jabar.csv")

def load_df():
    return pd.read_csv(FILE_PATH)

def save_df(df):
    df.to_csv(FILE_PATH, index=False)

# --- Fitur CRUD ---

def get_all_data():
    return load_df().to_dict(orient="records")

def add_data(new_data: dict):
    df = load_df()
    df = pd.concat(
        [df, pd.DataFrame([new_data])],
        ignore_index=True
    )
    save_df(df)

def delete_data(index: int):
    df = load_df()
    index = int(index)

    if 0 <= index < len(df):
        df = df.drop(index=index).reset_index(drop=True)
    
    save_df(df)

# --- Jawaban Soal A (Pengenalan DataFrame) ---

def soal_a():
    df = load_df()

    return {
        "a1_head_5_baris": df.head(),
        "a2_tail_5_baris": df.tail(),
        "a3_info_struktur": df.dtypes.astype(str),
        "a4_statistik_deskriptif": df[["jumlah_penderita_dm", "tahun"]].describe(),
        "a5_nilai_unik_tahun": sorted(df["tahun"].unique()),
        "a6_nilai_unik_kabupaten": df["nama_kabupaten_kota"].unique(),
        "a6_jumlah_kabupaten": df["nama_kabupaten_kota"].nunique(),
        "a7_kolom_terpilih": df[["nama_kabupaten_kota", "jumlah_penderita_dm", "tahun"]]
    }

# --- Jawaban Soal B (Filtering & Sorting) ---

def soal_b():
    df = load_df()
    data_2019 = df[df["tahun"] == 2019]

    return {
        "b8_data_tahun_2019": data_2019,
        "b9_lebih_100k": df[df["jumlah_penderita_dm"] > 100000],
        "b10_sort_jumlah_desc": df.sort_values(
            by="jumlah_penderita_dm", 
            ascending=False
        ),
        "b11_sort_tahun_dan_jumlah": df.sort_values(
            by=["tahun", "jumlah_penderita_dm"], 
            ascending=[True, False]
        ),
        "b12_top10_2019": (
            data_2019
            .sort_values("jumlah_penderita_dm", ascending=False)
            .head(10)
        ),
        "b13_kabupaten_bogor": df[df["nama_kabupaten_kota"] == "KABUPATEN BOGOR"]
    }

# --- Jawaban Soal C (Agregasi) ---

def soal_c():
    df = load_df()

    # Total penderita per tahun
    c14_total_per_tahun = (
        df.groupby("tahun")["jumlah_penderita_dm"]
        .sum()
        .reset_index(name="total_jumlah_penderita_dm")
    )

    # Rata-rata per kota
    c15_rata_per_kabupaten = (
        df.groupby("nama_kabupaten_kota")["jumlah_penderita_dm"]
        .mean()
        .reset_index(name="rata_rata_penderita_dm")
    )

    # Mencari nilai max dan min
    total_per_kab = df.groupby("nama_kabupaten_kota")["jumlah_penderita_dm"].sum()
    c16_kabupaten_tertinggi = total_per_kab.idxmax()
    c16_kabupaten_terendah = total_per_kab.idxmin()

    # Menambah kolom kategori
    df_kategori = df.copy()
    df_kategori["kategori_dm"] = df_kategori["jumlah_penderita_dm"].apply(
        lambda x: "Rendah" if x < 50000 else "Sedang" if x < 100000 else "Tinggi"
    )

    # Menghitung persentase
    df_persen = df_kategori.copy()
    df_persen["persentase_tahun"] = (
        df_persen["jumlah_penderita_dm"] / 
        df_persen.groupby("tahun")["jumlah_penderita_dm"].transform("sum") * 100
    )

    # Ringkasan data (agg)
    c19_tabel_ringkas = (
        df.groupby("tahun")
        .agg(
            total_jumlah_penderita_dm=("jumlah_penderita_dm", "sum"),
            jumlah_kabupaten_kota=("nama_kabupaten_kota", "count")
        )
        .reset_index()
    )

    return {
        "c14_total_per_tahun": c14_total_per_tahun,
        "c15_rata_per_kabupaten": c15_rata_per_kabupaten,
        "c16_kabupaten_tertinggi": c16_kabupaten_tertinggi,
        "c16_kabupaten_terendah": c16_kabupaten_terendah,
        "c17_data_dengan_kategori": df_kategori,
        "c18_data_dengan_persentase": df_persen,
        "c19_tabel_ringkas": c19_tabel_ringkas
    }