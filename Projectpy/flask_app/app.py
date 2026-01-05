from flask import Flask, render_template, request, redirect, url_for
import os

from pandas_service import (
    get_all_data,
    add_data,
    delete_data,
    soal_a,
    soal_b,
    soal_c
)

from analysis_service import (
    plot_bar_kabupaten_2019,
    plot_line_total_per_tahun,
    plot_barh_top10_2019,
    plot_pie_kategori_2019,
    plot_bar_3_tahun_terakhir
)

app = Flask(__name__)

# Route Halaman Utama
@app.route("/")
def index():
    return render_template("index.html")


# Route Halaman CRUD (Kelola Data)
@app.route("/crud")
def crud():
    try:
        data = get_all_data()
        return render_template("crud.html", data=data)
    except Exception as e:
        return f"Terjadi kesalahan saat mengambil data: {e}"


@app.route("/add", methods=["POST"])
def add():
    new_data = {
        "kode_provinsi": request.form["kode_provinsi"],
        "nama_provinsi": request.form["nama_provinsi"],
        "kode_kabupaten_kota": request.form["kode_kabupaten_kota"],
        "nama_kabupaten_kota": request.form["nama_kabupaten_kota"],
        "jumlah_penderita_dm": int(request.form["jumlah_penderita_dm"]),
        "satuan": request.form["satuan"],
        "tahun": int(request.form["tahun"])
    }
    add_data(new_data)
    return redirect(url_for("crud"))


@app.route("/delete/<int:index>")
def delete(index):
    delete_data(index)
    return redirect(url_for("crud"))


# Route Halaman Analisis Data (Pandas)
@app.route("/data")
def data():
    return render_template(
        "data.html",
        a=soal_a(),
        b=soal_b(),
        c=soal_c()
    )


# Route Halaman Visualisasi (Matplotlib)
@app.route("/grafik")
def grafik():
    # Buat folder static jika belum ada
    plot_dir = os.path.join("static", "plots")
    os.makedirs(plot_dir, exist_ok=True)

    # Generate grafik terbaru
    plot_bar_kabupaten_2019()
    plot_line_total_per_tahun()
    plot_barh_top10_2019()
    plot_pie_kategori_2019()
    plot_bar_3_tahun_terakhir()

    return render_template("grafik.html")


if __name__ == "__main__":
    app.run(debug=True)