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

# YENİ EKLENEN YÖNLENDİRME (Makine Parkuru yerine)
@app.route('/yedek-parca')
def spare_parts():
    return render_template('yedek_parca.html')

@app.route('/iletisim')
def contact():
    return render_template('iletisim.html')

if __name__ == '__main__':
    app.run(debug=True)
