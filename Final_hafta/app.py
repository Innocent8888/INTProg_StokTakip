from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.String(20), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Incorrect email or password!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Şifreler uyuşmuyor!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Hesabınız başarıyla oluşturuldu!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    urunler = Product.query.all()

    # Otomatik istatistikler
    kategori_sayisi = len(set([urun.category for urun in urunler]))
    urun_sayisi = len(urunler)
    son_guncelleme = max([urun.updated_at for urun in urunler], default="Veri yok")

    kritik = "Yeterli"  # Bu kısmı daha sonra mantığa göre özelleştirebilirsin

    return render_template(
        'dashboard.html',
        urunler=urunler,
        kategori_sayisi=kategori_sayisi,
        urun_sayisi=urun_sayisi,
        son_guncelleme=son_guncelleme,
        kritik=kritik
    )

@app.route('/urunler')
@login_required
def urun_listesi():
    urunler = Product.query.all()
    return render_template('urunler.html', urunler=urunler)

@app.route('/urun/ekle', methods=['GET', 'POST'])
@login_required
def urun_ekle():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        quantity = int(request.form.get('quantity'))
        updated_at = datetime.today().strftime('%Y-%m-%d')

        new_product = Product(name=name, category=category, quantity=quantity, updated_at=updated_at)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('urun_listesi'))

    return render_template('urun_ekle.html')

@app.route('/urun/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def urun_duzenle(id):
    urun = Product.query.get_or_404(id)
    if request.method == 'POST':
        urun.name = request.form.get('name')
        urun.category = request.form.get('category')
        urun.quantity = int(request.form.get('quantity'))
        urun.updated_at = datetime.today().strftime('%Y-%m-%d')

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('urun_listesi'))

    return render_template('urun_duzenle.html', urun=urun)

@app.route('/urun/sil/<int:id>')
@login_required
def urun_sil(id):
    urun = Product.query.get_or_404(id)
    db.session.delete(urun)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('urun_listesi'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yapıldı.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)