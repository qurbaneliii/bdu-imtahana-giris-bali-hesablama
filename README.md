# Bakı Dövlət Universiteti - İmtahana Giriş Balı Hesablama Sistemi

Bu proqram BDU tələbələri üçün imtahana giriş balını hesablamaq üçün hazırlanmışdır.

## 🌐 Canlı Demo

**Web Versiyası:** [https://qurbaneliii.github.io/bdu-imtahana-giris-bali-hesablama/](https://qurbaneliii.github.io/bdu-imtahana-giris-bali-hesablama/)

## Xüsusiyyətlər

- ✅ İnteraktiv konsol interfeysi
- ✅ Dərs saatı seçimi (15, 30, 45, 60, 75, 90 saat)
- ✅ Kollekvium ballarının hesablanması (3 kollekvium)
- ✅ Seminar qiymətlərinin hesablanması (dəyişən sayda)
- ✅ Sərbəst iş balının daxil edilməsi
- ✅ Davamiyyət hesablaması (qayıblara görə)
- ✅ Input validasiyası
- ✅ 50 ballıq şkala ilə nəticə

## Hesablama Qaydaları

### 1. Kollekvium Balları
- 3 kollekvium balı daxil edilir (hər biri 0-10 arası)
- Ortalama hesablanır və 0.6 əmsalı ilə vurulur

### 2. Seminar Qiymətləri
- İstənilən sayda seminar balı daxil edilə bilər (hər biri 0-10 arası)
- Ortalama hesablanır və 0.4 əmsalı ilə vurulur

### 3. Sərbəst İş
- 0-10 arası bal daxil edilir

### 4. Davamiyyət
- Qayıb sayı daxil edilir
- **60+ saatlıq fənn üçün:** Hər qayıb üçün 0.33 bal çıxılır
- **15-45 saatlıq fənn üçün:** Hər qayıb üçün 0.5 bal çıxılır
- Maksimum davamiyyət balı: 10
- Mənfi nəticə 0 qəbul edilir

### 5. Yekun Bal
```
İmtahana Giriş Balı = (Kollekvium × 0.6) + (Seminar × 0.4) + Davamiyyət + Sərbəst İş
```
Maksimum: 50 bal

## İstifadə

### Proqramı işə salmaq:

```bash
python3 imtahan_hesablayici.py
```

və ya:

```bash
./imtahan_hesablayici.py
```

### İstifadə nümunəsi:

1. Dərs saatını seçin (15, 30, 45, 60, 75 və ya 90)
2. 3 kollekvium balını daxil edin
3. Seminar sayını və ballarını daxil edin
4. Sərbəst iş balını daxil edin
5. Qayıb sayını daxil edin
6. Yekun nəticəni görün

## Nəticə Formatı

```
==================================================
YEKUN NƏTİCƏLƏR
==================================================
Kollekvium balı: 5.40 (ortalama: 9.00)
Seminar balı: 3.33 (ortalama: 8.33)
Davamiyyət: 8.35
Sərbəst iş: 9.00
--------------------------------------------------
Yekun bal: 26.08 / 50
==================================================
```

## Tələblər

- Python 3.6 və ya daha yüksək versiya
- Heç bir əlavə kitabxana tələb olunmur

## Müəllif

Bakı Dövlət Universiteti üçün hazırlanmışdır.

## Lisenziya

Bu proqram BDU tələbələri üçün pulsuz istifadə üçün nəzərdə tutulmuşdur.