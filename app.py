from flask import Flask, render_template

app = Flask(__name__)

# Sayfa Yönlendirmeleri
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/kurumsal')
def corporate():
    return render_template('kurumsal.html')

@app.route('/urunler')
def products():
    return render_template('urunler.html')

@app.route('/makine-parkuru')
def machine_park():
    return render_template('makine_parkuru.html')

@app.route('/iletisim')
def contact():
    return render_template('iletisim.html')

if __name__ == '__main__':
    app.run(debug=True)
