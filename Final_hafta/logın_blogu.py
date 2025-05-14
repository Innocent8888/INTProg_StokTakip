from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Kullanıcıyı veritabanında e-posta ile ara
        user = User.query.filter_by(email=email).first()

        # Kullanıcı varsa ve şifre doğruysa
        if user and check_password_hash(user.password, password):
            login_user(user)  # Kullanıcıyı giriş yapmış olarak işaretle
            return redirect(url_for('dashboard'))  # Dashboard'a yönlendir

        # Hatalı giriş durumu
        flash('E-posta veya şifre hatalı!', 'danger')

    return render_template('login.html')