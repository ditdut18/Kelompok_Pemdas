import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import os

# KONFIGURASI
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "jumlah_penderita_diabetes_jabar.csv")
PLOT_DIR = os.path.join(BASE_DIR, "static", "plots")

os.makedirs(PLOT_DIR, exist_ok=True)


def load_df():
    return pd.read_csv(DATA_PATH)


# SOAL 20
def plot_bar_kabupaten_2019():
    df = load_df()
    df_2019 = df[df["tahun"] == 2019]

    plt.figure(figsize=(12, 6))
    plt.bar(df_2019["nama_kabupaten_kota"], df_2019["jumlah_penderita_dm"])
    plt.xticks(rotation=90)
    plt.title("Jumlah Penderita DM per Kabupaten/Kota Tahun 2019")
    plt.xlabel("Kabupaten/Kota")
    plt.ylabel("Jumlah Penderita DM")
    plt.tight_layout()

    plt.savefig(os.path.join(PLOT_DIR, "bar_kabupaten_2019.png"))
    plt.close()


# SOAL 21
def plot_line_total_per_tahun():
    df = load_df()
    total = df.groupby("tahun")["jumlah_penderita_dm"].sum()

    plt.figure(figsize=(8, 5))
    plt.plot(total.index, total.values, marker="o")
    plt.title("Total Penderita DM Jawa Barat per Tahun")
    plt.xlabel("Tahun")
    plt.ylabel("Total Penderita DM")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(os.path.join(PLOT_DIR, "line_total_per_tahun.png"))
    plt.close()


# SOAL 22
def plot_barh_top10_2019():
    df = load_df()
    top10 = (
        df[df["tahun"] == 2019]
        .sort_values("jumlah_penderita_dm", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(8, 6))
    plt.barh(
        top10["nama_kabupaten_kota"],
        top10["jumlah_penderita_dm"]
    )
    plt.gca().invert_yaxis()
    plt.title("Top 10 Kabupaten/Kota Penderita DM Tertinggi Tahun 2019")
    plt.xlabel("Jumlah Penderita DM")
    plt.tight_layout()

    plt.savefig(os.path.join(PLOT_DIR, "barh_top10_2019.png"))
    plt.close()


# SOAL 23
def plot_pie_kategori_2019():
    df = load_df()
    df_2019 = df[df["tahun"] == 2019].copy()

    df_2019["kategori_dm"] = df_2019["jumlah_penderita_dm"].apply(
        lambda x: "Rendah" if x > 50000
        else "Sedang" if x < 100000
        else "Tinggi"
    )

    kategori = df_2019.groupby("kategori_dm")["jumlah_penderita_dm"].sum()

    plt.figure(figsize=(6, 6))
    plt.pie(kategori, labels=kategori.index, autopct="%1.1f%%", startangle=140)
    plt.title("Proporsi Kategori DM Tahun 2019")
    plt.tight_layout()

    plt.savefig(os.path.join(PLOT_DIR, "pie_kategori_2019.png"))
    plt.close()


# SOAL 24
def plot_bar_3_tahun_terakhir():
    df = load_df()
    tahun_terakhir = sorted(df["tahun"].unique())[-3:]

    total = (
        df[df["tahun"].isin(tahun_terakhir)]
        .groupby("tahun")["jumlah_penderita_dm"]
        .sum()
    )

    plt.figure(figsize=(6, 5))
    plt.bar(total.index.astype(str), total.values)
    plt.title("Perbandingan Total Penderita DM (3 Tahun Terakhir)")
    plt.xlabel("Tahun")
    plt.ylabel("Total Penderita DM")
    plt.tight_layout()

    plt.savefig(os.path.join(PLOT_DIR, "bar_3_tahun_terakhir.png"))
    plt.close()
