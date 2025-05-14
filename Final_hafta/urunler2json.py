from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stok.db'
db = SQLAlchemy(app)

# Modeller
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Urun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(150), nullable=False)
    aciklama = db.Column(db.Text, nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    miktar = db.Column(db.Integer, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('urunler', lazy=True))

# JSON'a aktarım fonksiyonu
def export_urunler_to_json():
    with app.app_context():
        urunler = Urun.query.all()
        data = []
        for urun in urunler:
            data.append({
                'id': urun.id,
                'ad': urun.ad,
                'aciklama': urun.aciklama,
                'kategori': urun.kategori,
                'miktar': urun.miktar,
                'kullanici_id': urun.kullanici_id,
                'kullanici_adi': urun.user.name if urun.user else None
            })

        with open('urunler.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Ürünler başarıyla urunler.json dosyasına kaydedildi!")

# Ana fonksiyon
if __name__ == '__main__':
    export_urunler_to_json()