#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BDU İmtahana Giriş Balı Hesablama Sistemi

Bu modul BDU tələbələri üçün imtahana giriş balını hesablamaq üçün
nəzərdə tutulmuşdur. Həm interaktiv konsol proqramı, həm də
import edilə bilən modul kimi istifadə oluna bilər.

Hesablama Qaydaları:
    - Kollekvium: 3 balın ortalaması × 0.6 (max 6 bal)
    - Seminar: n balın ortalaması × 0.4 (max 4 bal)
    - Davamiyyət: 10 - (qayıb × penalty) (max 10 bal)
    - Sərbəst iş: birbaşa bal (max 10 bal)
    - Cəmi: 30 ballıq sistem → 50 ballıq şkalaya çevrilir

Author: BDU Calculator Team
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional


# ============================================================
# Configuration Constants
# ============================================================

class Config:
    """Hesablama konfiqurasiyası və sabitləri."""
    
    # Valid course hour options
    VALID_HOURS: Tuple[int, ...] = (15, 30, 45, 60, 75, 90)
    
    # Score weights
    COLLOQUIUM_WEIGHT: float = 0.6
    SEMINAR_WEIGHT: float = 0.4
    
    # Attendance penalty rates
    PENALTY_HIGH_HOURS: float = 0.33  # 60+ hours
    PENALTY_LOW_HOURS: float = 0.5    # 15-45 hours
    HOURS_THRESHOLD: int = 60
    
    # Score limits
    MIN_SCORE: float = 0.0
    MAX_SCORE: float = 10.0
    MAX_ATTENDANCE: float = 10.0
    MAX_TOTAL_30: float = 30.0
    MAX_TOTAL_50: float = 50.0
    
    # Number of colloquiums required
    COLLOQUIUM_COUNT: int = 3


# ============================================================
# Data Classes
# ============================================================

@dataclass
class ScoreResult:
    """Hesablama nəticəsini saxlayan data class."""
    
    colloquium_average: float
    colloquium_weighted: float
    seminar_average: float
    seminar_weighted: float
    attendance_score: float
    independent_work: float
    total_30: float
    total_50: float
    
    @property
    def display_10(self) -> float:
        """10 ballıq şkalaya çevrilmiş nəticə."""
        return self.total_50 / 5
    
    def __str__(self) -> str:
        """Nəticəni formatlanmış string kimi qaytarır."""
        return (
            f"Kollekvium: {self.colloquium_weighted:.2f} "
            f"(ort: {self.colloquium_average:.2f})\n"
            f"Seminar: {self.seminar_weighted:.2f} "
            f"(ort: {self.seminar_average:.2f})\n"
            f"Davamiyyət: {self.attendance_score:.2f}\n"
            f"Sərbəst iş: {self.independent_work:.2f}\n"
            f"{'─' * 30}\n"
            f"Yekun: {self.total_50:.2f} / 50"
        )


# ============================================================
# Core Calculation Functions (Importable)
# ============================================================

def calculate_colloquium(scores: List[float]) -> Tuple[float, float]:
    """
    Kollekvium balını hesablayır.
    
    Args:
        scores: 3 kollekvium balının siyahısı (hər biri 0-10)
    
    Returns:
        Tuple[average, weighted_score]
    
    Raises:
        ValueError: Əgər bal sayı 3 deyilsə və ya aralıqdan kənardırsa
    """
    if len(scores) != Config.COLLOQUIUM_COUNT:
        raise ValueError(
            f"Kollekvium sayı {Config.COLLOQUIUM_COUNT} olmalıdır, "
            f"{len(scores)} verildi"
        )
    
    for i, score in enumerate(scores):
        if not (Config.MIN_SCORE <= score <= Config.MAX_SCORE):
            raise ValueError(
                f"Kollekvium {i + 1} balı 0-10 arasında olmalıdır: {score}"
            )
    
    average = sum(scores) / len(scores)
    weighted = average * Config.COLLOQUIUM_WEIGHT
    
    return average, weighted


def calculate_seminar(scores: List[float]) -> Tuple[float, float]:
    """
    Seminar balını hesablayır.
    
    Args:
        scores: Seminar ballarının siyahısı (hər biri 0-10)
    
    Returns:
        Tuple[average, weighted_score]
    
    Raises:
        ValueError: Əgər siyahı boşdursa və ya bal aralıqdan kənardırsa
    """
    if not scores:
        raise ValueError("Ən azı 1 seminar balı tələb olunur")
    
    for i, score in enumerate(scores):
        if not (Config.MIN_SCORE <= score <= Config.MAX_SCORE):
            raise ValueError(
                f"Seminar {i + 1} balı 0-10 arasında olmalıdır: {score}"
            )
    
    average = sum(scores) / len(scores)
    weighted = average * Config.SEMINAR_WEIGHT
    
    return average, weighted


def calculate_attendance(course_hours: int, absences: int) -> float:
    """
    Davamiyyət balını hesablayır.
    
    Formula:
        score = 10 - (absences × penalty)
        penalty = 0.33 (60+ saat) və ya 0.5 (15-45 saat)
    
    Args:
        course_hours: Dərs saatı (15, 30, 45, 60, 75, 90)
        absences: Qayıb sayı
    
    Returns:
        Davamiyyət balı (0-10 arasında)
    
    Raises:
        ValueError: Əgər dərs saatı etibarlı deyilsə
    """
    if course_hours not in Config.VALID_HOURS:
        raise ValueError(
            f"Dərs saatı {Config.VALID_HOURS} dəyərlərindən biri olmalıdır: "
            f"{course_hours}"
        )
    
    if absences < 0:
        raise ValueError(f"Qayıb sayı mənfi ola bilməz: {absences}")
    
    # Select penalty based on hours
    if course_hours >= Config.HOURS_THRESHOLD:
        penalty = Config.PENALTY_HIGH_HOURS
    else:
        penalty = Config.PENALTY_LOW_HOURS
    
    # Calculate and clamp score
    score = Config.MAX_ATTENDANCE - (absences * penalty)
    score = max(0.0, min(Config.MAX_ATTENDANCE, score))
    
    return score


def calculate_total(
    colloquium_scores: List[float],
    seminar_scores: List[float],
    independent_work: float,
    course_hours: int,
    absences: int
) -> ScoreResult:
    """
    Tam hesablama aparır və ScoreResult qaytarır.
    
    Args:
        colloquium_scores: 3 kollekvium balı
        seminar_scores: Seminar balları
        independent_work: Sərbəst iş balı (0-10)
        course_hours: Dərs saatı
        absences: Qayıb sayı
    
    Returns:
        ScoreResult obyekti
    
    Raises:
        ValueError: Əgər hər hansı parametr etibarsızdırsa
    """
    # Validate independent work
    if not (Config.MIN_SCORE <= independent_work <= Config.MAX_SCORE):
        raise ValueError(
            f"Sərbəst iş balı 0-10 arasında olmalıdır: {independent_work}"
        )
    
    # Calculate components
    coll_avg, coll_weighted = calculate_colloquium(colloquium_scores)
    sem_avg, sem_weighted = calculate_seminar(seminar_scores)
    attendance = calculate_attendance(course_hours, absences)
    
    # Calculate totals
    # Base total is on 30-point scale:
    #   Colloquium: max 6 (10 × 0.6)
    #   Seminar: max 4 (10 × 0.4)
    #   Attendance: max 10
    #   Independent: max 10
    #   Total: max 30
    total_30 = coll_weighted + sem_weighted + attendance + independent_work
    total_30 = min(total_30, Config.MAX_TOTAL_30)
    
    # Convert to 50-point scale
    total_50 = total_30 * (Config.MAX_TOTAL_50 / Config.MAX_TOTAL_30)
    total_50 = min(total_50, Config.MAX_TOTAL_50)
    
    return ScoreResult(
        colloquium_average=coll_avg,
        colloquium_weighted=coll_weighted,
        seminar_average=sem_avg,
        seminar_weighted=sem_weighted,
        attendance_score=attendance,
        independent_work=independent_work,
        total_30=total_30,
        total_50=total_50
    )


# ============================================================
# Interactive CLI Functions
# ============================================================

def get_valid_input(
    prompt: str,
    min_val: float,
    max_val: float,
    is_int: bool = False
) -> float:
    """
    Validasiya ilə istifadəçidən input alır.
    
    Args:
        prompt: Göstəriləcək mesaj
        min_val: Minimum qəbul edilən dəyər
        max_val: Maksimum qəbul edilən dəyər
        is_int: True olsa, integer tələb olunur
    
    Returns:
        Validasiya edilmiş rəqəm
    """
    while True:
        try:
            raw = input(prompt).strip()
            value = int(raw) if is_int else float(raw)
            
            if min_val <= value <= max_val:
                return value
            else:
                print(f"❌ Xəta: Dəyər {min_val} ilə {max_val} arasında olmalıdır!")
        except ValueError:
            print("❌ Xəta: Düzgün rəqəm daxil edin!")


def get_course_hours() -> int:
    """İstifadəçidən dərs saatını seçməsini tələb edir."""
    print("\n" + "═" * 50)
    print("📚 DƏRS SAATINI SEÇİN")
    print("═" * 50)
    
    for i, hours in enumerate(Config.VALID_HOURS, 1):
        print(f"  {i}. {hours} saat")
    
    hours_map = {str(i): h for i, h in enumerate(Config.VALID_HOURS, 1)}
    
    while True:
        choice = input(f"\nSeçiminiz (1-{len(Config.VALID_HOURS)}): ").strip()
        if choice in hours_map:
            return hours_map[choice]
        print(f"❌ Xəta: 1 ilə {len(Config.VALID_HOURS)} arasında seçim edin!")


def get_colloquium_scores() -> List[float]:
    """İstifadəçidən 3 kollekvium balını alır."""
    print("\n" + "═" * 50)
    print("📝 KOLLEKVİUM BALLARI")
    print("═" * 50)
    print("  (Hər bal 0-10 arasında olmalıdır)")
    
    scores = []
    ordinals = ["1-ci", "2-ci", "3-cü"]
    
    for i in range(Config.COLLOQUIUM_COUNT):
        score = get_valid_input(
            f"  {ordinals[i]} kollekvium balı: ",
            Config.MIN_SCORE,
            Config.MAX_SCORE
        )
        scores.append(score)
    
    return scores


def get_seminar_scores() -> List[float]:
    """İstifadəçidən seminar ballarını alır."""
    print("\n" + "═" * 50)
    print("💬 SEMİNAR QİYMƏTLƏRİ")
    print("═" * 50)
    
    count = int(get_valid_input(
        "  Neçə seminar qiyməti daxil edəcəksiniz? (1-10): ",
        1, 10, is_int=True
    ))
    
    print("  (Hər bal 0-10 arasında olmalıdır)")
    
    scores = []
    for i in range(1, count + 1):
        score = get_valid_input(
            f"  {i}-ci seminar balı: ",
            Config.MIN_SCORE,
            Config.MAX_SCORE
        )
        scores.append(score)
    
    return scores


def get_independent_work() -> float:
    """İstifadəçidən sərbəst iş balını alır."""
    print("\n" + "═" * 50)
    print("📚 SƏRBƏST İŞ")
    print("═" * 50)
    
    return get_valid_input(
        "  Sərbəst iş balı (0-10): ",
        Config.MIN_SCORE,
        Config.MAX_SCORE
    )


def get_absences() -> int:
    """İstifadəçidən qayıb sayını alır."""
    print("\n" + "═" * 50)
    print("📅 DAVAMİYYƏT")
    print("═" * 50)
    
    return int(get_valid_input(
        "  Qayıb sayını daxil edin: ",
        0, 100, is_int=True
    ))


def display_results(result: ScoreResult) -> None:
    """Nəticəni formatlanmış şəkildə göstərir."""
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║" + " " * 14 + "YEKUN NƏTİCƏLƏR" + " " * 15 + "║")
    print("╠" + "═" * 48 + "╣")
    print(f"║  📝 Kollekvium: {result.colloquium_weighted:5.2f} "
          f"(ortalama: {result.colloquium_average:.2f})" + " " * 5 + "║")
    print(f"║  💬 Seminar:    {result.seminar_weighted:5.2f} "
          f"(ortalama: {result.seminar_average:.2f})" + " " * 5 + "║")
    print(f"║  📅 Davamiyyət: {result.attendance_score:5.2f}" + " " * 24 + "║")
    print(f"║  📚 Sərbəst iş: {result.independent_work:5.2f}" + " " * 24 + "║")
    print("╠" + "═" * 48 + "╣")
    print(f"║  🎯 YEKUN BAL:  {result.total_50:5.2f} / 50" + " " * 18 + "║")
    print("╚" + "═" * 48 + "╝")


def print_header() -> None:
    """Proqram başlığını göstərir."""
    print()
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 6 + "🎓 BAKI DÖVLƏT UNİVERSİTETİ" + " " * 9 + "║")
    print("║" + " " * 4 + "İmtahana Giriş Balı Hesablama Sistemi" + " " * 3 + "║")
    print("╚" + "═" * 48 + "╝")


def main() -> None:
    """
    Əsas interaktiv proqram döngüsü.
    
    İstifadəçidən bütün lazımi məlumatları alır,
    hesablamanı aparır və nəticəni göstərir.
    """
    print_header()
    
    while True:
        # Collect all inputs
        course_hours = get_course_hours()
        colloquium_scores = get_colloquium_scores()
        seminar_scores = get_seminar_scores()
        independent_work = get_independent_work()
        absences = get_absences()
        
        # Calculate result
        try:
            result = calculate_total(
                colloquium_scores=colloquium_scores,
                seminar_scores=seminar_scores,
                independent_work=independent_work,
                course_hours=course_hours,
                absences=absences
            )
            
            # Display results
            display_results(result)
            
        except ValueError as e:
            print(f"\n❌ Hesablama xətası: {e}")
        
        # Ask to continue
        print("\n" + "─" * 50)
        restart = input("Yenidən hesablamaq istəyirsiniz? (b/x): ").strip().lower()
        
        if restart != 'b':
            print("\n✨ Təşəkkür edirik! Uğurlar! 🎓\n")
            break
        
        print("\n" * 2)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proqram istifadəçi tərəfindən dayandırıldı.")
    except Exception as e:
        print(f"\n❌ Gözlənilməz xəta: {e}")
        raise
