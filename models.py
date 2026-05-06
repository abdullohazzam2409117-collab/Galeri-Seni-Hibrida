from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Seniman(db.Model):
    id_seniman = db.Column(db.Integer, primary_key=True)
    nama_seniman = db.Column(db.String(100), nullable=False)
    biografi = db.Column(db.Text)
    # Relasi: Satu seniman menciptakan banyak karya seni
    karya_seni = db.relationship('KaryaSeni', backref='seniman', lazy=True)

class KaryaSeni(db.Model):
    id_karya = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.Text)
    id_seniman = db.Column(db.Integer, db.ForeignKey('seniman.id_seniman'), nullable=False)
    # Relasi: Satu karya seni memiliki banyak narasi AR (beda bahasa)
    narasinya = db.relationship('NarasiAR', backref='karya', lazy=True)

class NarasiAR(db.Model):
    id_narasi = db.Column(db.Integer, primary_key=True)
    bahasa = db.Column(db.String(50), nullable=False)
    durasi = db.Column(db.String(20))
    file_konten = db.Column(db.String(255))
    id_karya = db.Column(db.Integer, db.ForeignKey('karya_seni.id_karya'), nullable=False)

class Pengunjung(db.Model):
    id_pengunjung = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kontak = db.Column(db.String(50))
    asal_daerah = db.Column(db.String(100))

class Sensor(db.Model):
    id_sensor = db.Column(db.Integer, primary_key=True)
    tipe_sensor = db.Column(db.String(50))
    status_aktif = db.Column(db.Boolean, default=True)

class LogInteraksi(db.Model):
    id_log = db.Column(db.Integer, primary_key=True)
    waktu_akses = db.Column(db.DateTime, default=datetime.utcnow)
    id_pengunjung = db.Column(db.Integer, db.ForeignKey('pengunjung.id_pengunjung'), nullable=False)
    id_karya = db.Column(db.Integer, db.ForeignKey('karya_seni.id_karya'), nullable=False)
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensor.id_sensor'), nullable=False)