from flask import Flask, render_template, request, redirect, url_for
from models import db, Pengunjung
from models import Seniman, KaryaSeni, NarasiAR, Sensor, LogInteraksi, Pengunjung # Pastikan Pengunjung diimport dari models
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Sesuai struktur folder kamu
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/detail')
def detail():
    return render_template('detail.html')
# --- FITUR BARU PERTEMUAN 10 ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Ekstraksi data dari form [cite: 348]
        nama_input = request.form['nama']
        kontak_input = request.form['kontak']
        asal_input = request.form['asal_daerah']
        # Simpan ke Database Fisik [cite: 287]
        baru = Pengunjung(nama=nama_input, kontak=kontak_input, asal_daerah=asal_input)
        db.session.add(baru)
        db.session.commit()
        # Redirect kembali ke beranda setelah sukses [cite: 347]
        return redirect(url_for('index'))
    return render_template('register.html')
    # FITUR 1: Input Koleksi Karya Seni Baru
@app.route('/admin/tambah-karya', methods=['GET', 'POST'])
def tambah_karya():
    if request.method == 'POST':
        # Ekstraksi Data [cite: 348]
        judul_val = request.form['judul']
        desc_val = request.form['deskripsi']
        seniman_id = request.form['id_seniman']
        # Simpan ke Database [cite: 391-392]
        baru = KaryaSeni(judul=judul_val, deskripsi=desc_val, id_seniman=seniman_id)
        db.session.add(baru)
        db.session.commit()
        return redirect(url_for('list_karya'))
    # Ambil daftar seniman agar bisa dipilih di dropdown
    daftar_seniman = Seniman.query.all()
    return render_template('tambah_karya.html', seniman=daftar_seniman)

# --- OPERASI READ (LIST KARYA) ---
@app.route('/admin/karya')
def list_karya():
    # Mengambil semua data karya seni dari database [cite: 351]
    karya = KaryaSeni.query.all()
    return render_template('list_karya.html', karya=karya)

# --- OPERASI UPDATE ---
@app.route('/admin/update-karya/<int:id>', methods=['GET', 'POST'])
def update_karya(id):
    # Mengambil data lama berdasarkan ID [cite: 352]
    karya = KaryaSeni.query.get_or_404(id)
    
    if request.method == 'POST':
        # Menangkap data baru dari form [cite: 348]
        karya.judul = request.form['judul']
        karya.deskripsi = request.form['deskripsi']
        karya.id_seniman = request.form['id_seniman']
        
        # Komit ulang ke basis data [cite: 288]
        db.session.commit()
        return redirect(url_for('list_karya'))
    
    daftar_seniman = Seniman.query.all()
    return render_template('update_karya.html', karya=karya, seniman=daftar_seniman)

# --- OPERASI DELETE ---
@app.route('/admin/delete-karya/<int:id>', methods=['POST'])
def delete_karya(id):
    # Mengambil data berdasarkan ID unik
    karya = KaryaSeni.query.get_or_404(id)
    
    # Implementasikan fungsi penghapusan record [cite: 289]
    db.session.delete(karya)
    db.session.commit()
    
    return redirect(url_for('list_karya'))

# FITUR 2: Input Narasi AR untuk Karya Tertentu
@app.route('/admin/tambah-narasi', methods=['GET', 'POST'])
def tambah_narasi():
    if request.method == 'POST':
        lang = request.form['bahasa']
        file_path = request.form['file']
        karya_id = request.form['id_karya']
        narasi_baru = NarasiAR(bahasa=lang, file_konten=file_path, id_karya=karya_id)
        db.session.add(narasi_baru)
        db.session.commit()
        return redirect(url_for('detail'))
    daftar_karya = KaryaSeni.query.all()
    return render_template('tambah_narasi.html', karya=daftar_karya)
# FITUR 3: Simulasi Log Sensor (Hibrida)
@app.route('/simulasi-sensor', methods=['GET', 'POST'])
def simulasi_sensor():
    if request.method == 'POST':
        p_id = request.form['id_pengunjung']
        s_id = request.form['id_sensor']
        k_id = request.form['id_karya']
        # Mencatat interaksi real-time ke tabel Log_Interaksi [cite: 248-250]
        log_baru = LogInteraksi(id_pengunjung=p_id, id_sensor=s_id, id_karya=k_id)
        db.session.add(log_baru)
        db.session.commit()
        return redirect(url_for('detail'))
    # Ambil data untuk pilihan dropdown
    p = Pengunjung.query.all()
    s = Sensor.query.all()
    k = KaryaSeni.query.all()
    return render_template('simulasi_sensor.html', pengunjung=p, sensor=s, karya=k)
if __name__ == '__main__':
    app.run(debug=True)