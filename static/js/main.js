// Dark/Light Tema Sistemi
const themeBtn = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme') || 'dark'; // Varsayılanı karanlık yapıyoruz (daha cool)
document.documentElement.setAttribute('data-theme', currentTheme);

themeBtn.addEventListener('click', () => {
    let theme = document.documentElement.getAttribute('data-theme');
    let targetTheme = theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', targetTheme);
    localStorage.setItem('theme', targetTheme);
});

// Scroll Animasyonları (Ekrana girince beliren elemanlar)
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

// --- CNC KIVILCIM SİMÜLASYONU MOTORU ---

const canvas = document.getElementById('spark-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    const brandContainer = document.querySelector('.brand-cut-container');
    const brandGlow = document.querySelector('.brand-glow');
    let sparks = [];

    // Canvas boyutunu ayarla
    function resizeCanvas() {
        if (canvas.parentElement) {
            canvas.width = canvas.parentElement.offsetWidth;
            canvas.height = canvas.parentElement.offsetHeight;
        }
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Kıvılcım Sınıfı
    class Spark {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            // Gerçekçi fışkırma açısı ve hızı (Aşağıya doğru ve dağınık)
            this.speedX = (Math.random() - 0.5) * 8; // Hafif sağ/sol dağolım
            this.speedY = Math.random() * 12 + 5; // Güçlü aşağı fışkırma
            this.gravity = 0.2;
            this.friction = 0.98; // Hava direnci
            this.color = getComputedStyle(document.documentElement).getPropertyValue('--spark-outer').trim() || '#f59e0b';
            this.coreColor = getComputedStyle(document.documentElement).getPropertyValue('--spark-core').trim() || '#fff';
            this.size = Math.random() * 2 + 1; // Rastgele boyut
            this.alpha = 1;
            this.decay = Math.random() * 0.02 + 0.01; // Sönme hızı
        }

        update() {
            this.speedY += this.gravity; // Yerçekimi
            this.speedX *= this.friction; // Hava direnci
            this.x += this.speedX;
            this.y += this.speedY;
            this.alpha -= this.decay; // Sönme
        }

        draw() {
            ctx.globalAlpha = this.alpha;
            // Çekirdek (parlak beyaz)
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.5, 0, Math.PI * 2);
            ctx.fillStyle = this.coreColor;
            ctx.fill();
            // Dış (Sıcak turuncu/sarı parıltı)
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
            // Hafif hareket izi (Lineer bulanıklık)
            ctx.beginPath();
            ctx.moveTo(this.x, this.y);
            ctx.lineTo(this.x - this.speedX * 2, this.y - this.speedY * 2);
            ctx.strokeStyle = this.color;
            ctx.lineWidth = this.size * 0.5;
            ctx.stroke();
        }
    }

    // Kıvılcım Oluşturma Döngüsü
    function generateSparks() {
        if (!brandContainer || !brandGlow) return;

        // CSS animasyonunun mevcut X pozisyonunu takip et
        const computedStyle = window.getComputedStyle(brandGlow);
        const backgroundPosition = computedStyle.getPropertyValue('background-position-x');
        const containerWidth = brandContainer.offsetWidth;
        const currentAlpha = computedStyle.getPropertyValue('opacity');

        if (currentAlpha > 0.1) { // Sadece parıltı görünürken kıvılcım çıkar
            // background-position'ı (200% ile -200%) X koordinatına çevir (0 ile containerWidth)
            const percentPos = (parseFloat(backgroundPosition) + 200) / 400; // 0 to 1
            const invertedPos = 1 - percentPos; // Animasyon ters yönde gidiyor olabilir
            const cutX = (invertedPos * containerWidth) + brandContainer.offsetLeft;
            const cutY = brandContainer.offsetTop + (brandContainer.offsetHeight * 0.5);

            // Her döngüde 3-7 arası kıvılcım ekle
            for (let i = 0; i < Math.random() * 4 + 3; i++) {
                sparks.push(new Spark(cutX, cutY));
            }
        }
    }

    // Animasyon Döngüsü
    function animateSparks() {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Canvas'ı temizle
        generateSparks();

        for (let i = 0; i < sparks.length; i++) {
            sparks[i].update();
            sparks[i].draw();
            // Sönen kıvılcımları sil
            if (sparks[i].alpha <= 0 || sparks[i].y > canvas.height) {
                sparks.splice(i, 1);
                i--;
            }
        }
        requestAnimationFrame(animateSparks);
    }

    animateSparks();
}
