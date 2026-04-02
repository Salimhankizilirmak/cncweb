import os
from flask import Flask, render_template, send_from_directory, abort

app = Flask(__name__)

# Resimlerin bulunduğu ana dizin
IMAGES_DIR = os.path.join(app.root_path, 'images', 'ana sayfa')

REFERENCES_LIST = [
    "ALK DEĞİRMEN",
    "MİRAN MAKİNA ARAÇ ÜSTÜ EKİPMAN YEDEK PARÇA",
    "ÇORUM MİLLİNG MAKİNA İMALATI SAN. VE TİC. LTD. ŞTİ.",
    "Emta Makina",
    "CLAY TECH - YAŞAR OKUMUŞ MÜHENDİSLİK MAK. İMAL. SAN. ve TİC.LTD.ŞTİ.",
    "Delta dişli cnc",
    "Boyraz Grup",
    "Oms Okur Makina",
    "Güven Makina Hırdavat",
    "Arn Makina",
    "Kaya Makina",
    "TAŞ DEGİRMEN MAKİNA",
    "İnomeka makina",
    "Erdacrane",
    "Deniz Değirmen Makina",
    "Murat Çelik",
    "POREM PORSELEN ELEKTRİK SAN.TİC.AŞ.(644)",
    "FİDOTECH MAKİNA",
    "Hayranoğlu CNC Torna",
    "Grindex Milling Machine",
    "MTM kesici takımları oke Çorum bölge bayi",
    "OZN Makina",
    "Balaban makina patates yıkama makinaları",
    "Metsan makina"
]

def get_images_from_folder(folder_name):
    folder_path = os.path.join(IMAGES_DIR, folder_name)
    images = []
    if os.path.exists(folder_path):
        for f in os.listdir(folder_path):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                # URL path oluştur
                images.append(f'ana sayfa/{folder_name}/{f}')
    return images

@app.route('/images/<path:filename>')
def serve_images(filename):
    # Tüm images klasörü altından dosya servisi
    return send_from_directory('images', filename)

@app.route('/')
def home():
    # Üretimden kareler için
    uretimden_kareler = get_images_from_folder('üretimden kareler')
    return render_template('index.html', uretimden_kareler=uretimden_kareler, references=REFERENCES_LIST)

@app.route('/kurumsal')
def corporate():
    uretimden_kareler = get_images_from_folder('üretimden kareler')
    return render_template('kurumsal.html', uretimden_kareler=uretimden_kareler)

@app.route('/kategori/<cat_name>')
def category(cat_name):
    # URL dostu isimlerden gerçek klasör isimlerine eşleştirme
    folders = {
        'hidrolik-sistemler': 'hidrolik-sistemler',
        'ozel-uretim': 'ozel uretim',
        'talasli-imalat': 'talaşlı imalat'
    }
    
    if cat_name not in folders:
        abort(404)
        
    folder = folders[cat_name]
    images = get_images_from_folder(folder)
    
    # Basitçe kategori adını başlık için düzeltelim
    title = folder.replace('-', ' ').title()
    
    return render_template('kategori.html', images=images, category_title=title)

@app.route('/urunler')
def products():
    # 3 kategorinin toplamı
    images = []
    images.extend(get_images_from_folder('hidrolik-sistemler'))
    images.extend(get_images_from_folder('ozel uretim'))
    images.extend(get_images_from_folder('talaşlı imalat'))
    return render_template('urunler.html', images=images)

@app.route('/yedek-parca')
def spare_parts():
    images = get_images_from_folder('yedek parça')
    return render_template('yedek_parca.html', images=images)

@app.route('/iletisim')
def contact():
    return render_template('iletisim.html')

@app.route('/referanslar')
def references():
    return render_template('referanslar.html', references=REFERENCES_LIST)

if __name__ == '__main__':
    app.run(debug=True)
