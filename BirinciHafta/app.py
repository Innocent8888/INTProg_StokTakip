from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/gunluk/ekle')
def gunluk_ekle():
    return render_template('gunluk_ekle.html')

@app.route('/gunluk/duzenle/<int:id>')
def gunluk_duzenle(id):
    return render_template('gunluk_duzenle.html')

if __name__ == '__main__':
    app.run(debug=True) 