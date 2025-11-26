#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bakı Dövlət Universiteti
İmtahana Giriş Balı Hesablama Sistemi
"""

def get_valid_input(prompt, min_val, max_val, is_int=False):
    """Validasiya ilə input almaq üçün yardımçı funksiya"""
    while True:
        try:
            if is_int:
                value = int(input(prompt))
            else:
                value = float(input(prompt))
            
            if min_val <= value <= max_val:
                return value
            else:
                print(f"❌ Xəta: Dəyər {min_val} ilə {max_val} arasında olmalıdır!")
        except ValueError:
            print("❌ Xəta: Düzgün rəqəm daxil edin!")

def get_course_hours():
    """Dərs saatını seçmək"""
    print("\n" + "="*50)
    print("DƏRS SAATINI SEÇİN")
    print("="*50)
    print("1. 15 saat")
    print("2. 30 saat")
    print("3. 45 saat")
    print("4. 60 saat")
    print("5. 75 saat")
    print("6. 90 saat")
    
    hours_map = {
        "1": 15,
        "2": 30,
        "3": 45,
        "4": 60,
        "5": 75,
        "6": 90
    }
    
    while True:
        choice = input("\nSeçiminiz (1-6): ")
        if choice in hours_map:
            return hours_map[choice]
        else:
            print("❌ Xəta: 1 ilə 6 arasında seçim edin!")

def get_colloquium_scores():
    """3 kollekvium balını almaq və hesablamaq"""
    print("\n" + "="*50)
    print("KOLLEKVİUM BALLARI")
    print("="*50)
    
    scores = []
    for i in range(1, 4):
        score = get_valid_input(f"{i}-ci kollekvium balı (0-10): ", 0, 10)
        scores.append(score)
    
    average = sum(scores) / len(scores)
    weighted_score = average * 0.6
    
    return weighted_score, average

def get_seminar_scores():
    """Seminar ballarını almaq və hesablamaq"""
    print("\n" + "="*50)
    print("SEMİNAR QİYMƏTLƏRİ")
    print("="*50)
    
    count = get_valid_input("Neçə seminar qiyməti daxil edəcəksiniz? ", 1, 20, is_int=True)
    
    scores = []
    for i in range(1, count + 1):
        score = get_valid_input(f"{i}-ci seminar balı (0-10): ", 0, 10)
        scores.append(score)
    
    average = sum(scores) / len(scores)
    weighted_score = average * 0.4
    
    return weighted_score, average

def get_independent_work_score():
    """Sərbəst iş balını almaq"""
    print("\n" + "="*50)
    print("SƏRBƏST İŞ")
    print("="*50)
    
    score = get_valid_input("Sərbəst iş balı (0-10): ", 0, 10)
    return score

def calculate_attendance(course_hours):
    """Davamiyyət balını hesablamaq"""
    print("\n" + "="*50)
    print("DAVAMİYYƏT")
    print("="*50)
    
    absences = get_valid_input("Qayıb sayını daxil edin: ", 0, 100, is_int=True)
    
    # Dərs saatına görə penalty müəyyənləşdirmək
    if course_hours >= 60:
        penalty_per_absence = 0.33
    else:  # 15, 30, 45
        penalty_per_absence = 0.5
    
    # Davamiyyət balını hesablamaq
    attendance_score = 10 - (absences * penalty_per_absence)
    
    # Mənfi olarsa 0 qəbul et
    if attendance_score < 0:
        attendance_score = 0
    
    # Maksimum 10 bal
    if attendance_score > 10:
        attendance_score = 10
    
    return attendance_score

def display_results(colloquium_score, colloquium_avg, seminar_score, seminar_avg, 
                   attendance_score, independent_work_score, final_score):
    """Nəticələri formatlanmış şəkildə göstərmək"""
    print("\n" + "="*50)
    print("YEKUN NƏTİCƏLƏR")
    print("="*50)
    print(f"Kollekvium balı: {colloquium_score:.2f} (ortalama: {colloquium_avg:.2f})")
    print(f"Seminar balı: {seminar_score:.2f} (ortalama: {seminar_avg:.2f})")
    print(f"Davamiyyət: {attendance_score:.2f}")
    print(f"Sərbəst iş: {independent_work_score:.2f}")
    print("-" * 50)
    print(f"Yekun bal: {final_score:.2f} / 50")
    print("=" * 50)

def main():
    """Əsas proqram"""
    print("╔" + "="*48 + "╗")
    print("║  BAKI DÖVLƏT UNİVERSİTETİ                     ║")
    print("║  İmtahana Giriş Balı Hesablama Sistemi        ║")
    print("╚" + "="*48 + "╝")
    
    # 1. Dərs saatını almaq
    course_hours = get_course_hours()
    
    # 2. Kollekvium ballarını almaq
    colloquium_score, colloquium_avg = get_colloquium_scores()
    
    # 3. Seminar ballarını almaq
    seminar_score, seminar_avg = get_seminar_scores()
    
    # 4. Sərbəst iş balını almaq
    independent_work_score = get_independent_work_score()
    
    # 5. Davamiyyət balını hesablamaq
    attendance_score = calculate_attendance(course_hours)
    
    # 6. Yekun balı hesablamaq
    final_score = colloquium_score + seminar_score + attendance_score + independent_work_score
    
    # Maksimum 50 bal ilə məhdudlaşdırmaq
    if final_score > 50:
        final_score = 50
    
    # 7. Nəticələri göstərmək
    display_results(colloquium_score, colloquium_avg, seminar_score, seminar_avg,
                   attendance_score, independent_work_score, final_score)
    
    # Yenidən hesablamaq istəyir?
    print("\n" + "="*50)
    restart = input("Yenidən hesablamaq istəyirsiniz? (b/x): ").lower()
    if restart == 'b':
        print("\n" * 2)
        main()
    else:
        print("\nTəşəkkür edirik! Uğurlar! 🎓")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProqram istifadəçi tərəfindən dayandırıldı.")
    except Exception as e:
        print(f"\n❌ Xəta baş verdi: {e}")
