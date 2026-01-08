# BDU İmtahana Giriş Balı Kalkulyatoru

<div align="center">

![Baku State University](https://img.shields.io/badge/BDU-Bakı_Dövlət_Universiteti-1a5276?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**BDU tələbələri üçün imtahana giriş balını hesablayan müasir web və konsol əsaslı proqram**

[🌐 Canlı Demo](https://qurbaneliii.github.io/bdu-imtahana-giris-bali-hesablama/) • [📖 Dokumentasiya](#hesablama-qaydaları) • [🐛 Problem Bildirin](https://github.com/qurbaneliii/bdu-imtahana-giris-bali-hesablama/issues)

</div>

---

## Xüsusiyyətlər

| Xüsusiyyət | Web Versiya | Python CLI |
|------------|:-----------:|:----------:|
| İnteraktiv interfeys | ✅ | ✅ |
| Dərs saatı seçimi (15-90) | ✅ | ✅ |
| 3 kollekvium hesablaması | ✅ | ✅ |
| Dinamik seminar sayı | ✅ | ✅ |
| Davamiyyət hesablaması | ✅ | ✅ |
| Sərbəst iş balı | ✅ | ✅ |
| Input validasiyası | ✅ | ✅ |
| 50 və 10 şkala seçimi | ✅ | ✅ |
| Qaranlıq/İşıqlı rejim | ✅ | ❌ |
| Responsiv dizayn | ✅ | ❌ |
| Modul import | ❌ | ✅ |

## Canlı Demo

**Web Versiyası:** [https://qurbaneliii.github.io/bdu-imtahana-giris-bali-hesablama/](https://qurbaneliii.github.io/bdu-imtahana-giris-bali-hesablama/)

---

## Hesablama Qaydaları

İmtahana giriş balı **30 ballıq baza** sistemində hesablanır və **50 ballıq şkala**ya çevrilir.

### Komponent Paylanması (30 bal bazası)

| Komponent | Maks. Bal | Əmsal | Hesablama |
|-----------|:---------:|:-----:|-----------|
| **Kollekvium** | 6 | ×0.6 | 3 kollekviumun ortalaması × 0.6 |
| **Seminar** | 4 | ×0.4 | Seminar ortalaması × 0.4 |
| **Davamiyyət** | 10 | - | 10 − (qayıb × cərimə) |
| **Sərbəst iş** | 10 | - | Birbaşa bal (0-10) |
| **YEKUN** | **30** | | 50-yə konversiya |

### Davamiyyət Cərimələri

| Fənn Saatı | Cərimə (qayıb başına) |
|:----------:|:---------------------:|
| 60+ saat   | 0.33 bal              |
| 15-45 saat | 0.50 bal              |

### Formula

```
30-ballıq yekun = (Koll_ort × 0.6) + (Sem_ort × 0.4) + Davamiyyət + Sərbəst_iş
50-ballıq yekun = 30-ballıq_yekun × (50 / 30)
```

---

## İstifadə

### Web Versiyası

1. [Canlı demo](https://qurbaneliii.github.io/bdu-imtahana-giris-bali-hesablama/) səhifəsini açın
2. Dərs saatını seçin
3. Kollekvium, seminar və digər balları daxil edin
4. Nəticə şkalasını seçin (50 və ya 10)
5. "Hesabla" düyməsinə basın

### Python CLI Versiyası

```bash
# Əsas istifadə
python3 imtahan_hesablayici.py

# və ya icra edilə bilən kimi
chmod +x imtahan_hesablayici.py
./imtahan_hesablayici.py
```

### Python Modul Kimi İstifadə

```python
from imtahan_hesablayici import calculate_total, ScoreResult

# Tək hesablama funksiyaları
from imtahan_hesablayici import (
    calculate_colloquium,
    calculate_seminar,
    calculate_attendance,
    validate_score
)

# Nümunə
coll_result = calculate_colloquium(8.5, 9.0, 7.5)
print(f"Kollekvium: {coll_result['weighted']:.2f}")
```

---

## Fayl Strukturu

```
bdu-imtahana-giris-bali-hesablama/
├── index.html              # Əsas HTML səhifə
├── style.css               # CSS stilləri (qaranlıq rejim daxil)
├── app.js                  # JavaScript kalkulyator məntiqi
├── imtahan_hesablayici.py  # Python CLI versiyası
├── 404.html                # Xəta səhifəsi
├── _config.yml             # Jekyll konfiqurasiyası
├── .nojekyll               # Jekyll deaktiv faylı
└── README.md               # Bu sənəd
```

---

## Texnoloji Stek

- **Frontend:** Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Backend/CLI:** Python 3.7+ (standart kitabxana)
- **Hosting:** GitHub Pages
- **Dizayn:** CSS Custom Properties, Flexbox, Grid
- **Accessibility:** ARIA labels, semantic HTML

---

## Ekran Görüntüləri

<details>
<summary>İşıqlı Rejim</summary>

Dərs saatı seçimi, kollekvium və seminar girişləri, real-vaxt hesablama

</details>

<details>
<summary>Qaranlıq Rejim</summary>

Göz dostu qaranlıq tema, bütün funksiyalar mövcud

</details>

---

## Nümunə Hesablama

| Giriş | Dəyər |
|-------|-------|
| Dərs saatı | 60 saat |
| Kollekvium 1 | 9.0 |
| Kollekvium 2 | 8.5 |
| Kollekvium 3 | 9.5 |
| Seminar (3 ədəd) | 8.0, 9.0, 8.5 |
| Qayıb sayı | 2 |
| Sərbəst iş | 9.0 |

**Hesablama:**
```
Kollekvium: (9.0 + 8.5 + 9.5) / 3 × 0.6 = 5.40
Seminar: (8.0 + 9.0 + 8.5) / 3 × 0.4 = 3.40
Davamiyyət: 10 - (2 × 0.33) = 9.34
Sərbəst iş: 9.00

30-ballıq yekun: 5.40 + 3.40 + 9.34 + 9.00 = 27.14
50-ballıq yekun: 27.14 × (50/30) = 45.23
```

---

## Tələblər

### Web Versiyası
- Müasir brauzer (Chrome, Firefox, Safari, Edge)

### Python CLI
- Python 3.7 və ya daha yüksək
- Əlavə kitabxana tələb olunmur

---

## Töhfə Vermək

1. Repo-nu fork edin
2. Yeni branch yaradın (`git checkout -b feature/yeni-xususiyyet`)
3. Dəyişiklikləri commit edin (`git commit -m 'Yeni xüsusiyyət əlavə edildi'`)
4. Branch-ı push edin (`git push origin feature/yeni-xususiyyet`)
5. Pull Request açın

---

## Lisenziya

Bu layihə MIT lisenziyası altında yayımlanır. Ətraflı məlumat üçün [LICENSE](LICENSE) faylına baxın.

---

## Müəllif

Bakı Dövlət Universiteti tələbələri üçün hazırlanmışdır.

**Repo:** [qurbaneliii/bdu-imtahana-giris-bali-hesablama](https://github.com/qurbaneliii/bdu-imtahana-giris-bali-hesablama)

---

<div align="center">
  
⭐ Bu layihə faydalı oldusa, ulduz verməyi unutmayın!

</div>
