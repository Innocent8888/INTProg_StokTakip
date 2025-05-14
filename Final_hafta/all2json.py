from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stok.db'
db = SQLAlchemy(app)

# Modeller
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    urunler = db.relationship('Urun', backref='user', lazy=True)

class Kategori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False, unique=True)

    urunler = db.relationship('Urun', backref='kategori', lazy=True)

class Urun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(150), nullable=False)
    aciklama = db.Column(db.Text, nullable=True)
    miktar = db.Column(db.Integer, nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def export_stok_to_json():
    with app.app_context():
        users = User.query.all()
        data = []
        for user in users:
            user_data = {
                'id': user.id,
                'ad': user.ad,
                'email': user.email,
                'urunler': []
            }

            for urun in users.urunler:
                urun_data = {
                    'id': urun.id,
                    'ad': urun.ad,
                    'aciklama': urun.aciklama,
                    'miktar': urun.miktar,
                    'kategori': urun.kategori.ad
                }
                user_data['urunler'].append(urun_data)

            data.append(user_data)

        with open('stok_durumu.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Stok verileri başarıyla stok_durumu.json dosyasına kaydedildi!")

if __name__ == '__main__':
    export_stok_to_json()