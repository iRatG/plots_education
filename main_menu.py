"""
INTERAKTIVNOE MENYU DLYA IZUCHENIYA MATPLOTLIB

Obuchayushchiy proyekt po vizualizatsii dannykh
Vybirayete tipy grafikov i izuchayte ikh osobennosti
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import io

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Настройка matplotlib для русского языка
plt.rcParams['font.family'] = 'DejaVu Sans'

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_generator import create_sample_data
from plots import (
    create_line_plot,
    create_bar_plot,
    create_pie_plot,
    create_histogram,
    create_scatter_plot,
    create_box_plot,
    create_heatmap,
    create_area_plot,
    create_violin_plot,
    create_pivot_plots
)


def print_header():
    """Красивый заголовок программы"""
    print("\n" + "="*80)
    print("=" + " "*78 + "=")
    print("=" + " "*78 + "=")
    print("=" + " "*15 + "OBUCHENIE MATPLOTLIB I VIZUALIZACII" + " "*14 + "=")
    print("=" + " "*78 + "=")
    print("=" + " "*78 + "=")
    print("="*80 + "\n")


def print_menu():
    """Вывод главного меню"""
    print("\n" + "-"*80)
    print("  GLAVNOE MENYU - Vyberite tip grafika:")
    print("-"*80)
    print()
    print("  BAZOVYE GRAFIKI:")
    print("    1.  Lineyny grafik (Line Plot) - dlya vremennykh ryadov")
    print("    2.  Stolbchataya diagramma (Bar Plot) - dlya sravneniya kategoriy")
    print("    3.  Krugovaya diagramma (Pie Chart) - dlya pokaza doley")
    print("    4.  Gistogramma (Histogram) - dlya raspredeleniy")
    print()
    print("  ANALITICHESKIE GRAFIKI:")
    print("    5.  Tochechnaya diagramma (Scatter Plot) - dlya korrelyatsiy")
    print("    6.  Yashchik s usami (Box Plot) - dlya statistiki")
    print("    7.  Skripichnaya diagramma (Violin Plot) - dlya raspredeleniy")
    print()
    print("  PRODVINUTYE:")
    print("    8.  Teplovaya karta (Heatmap) - dlya matrits i patternov")
    print("    9.  Ploshchadnoy grafik (Area Plot) - dlya ob'ema dannykh")
    print("    10. Pivot tablitsy - dlya mnogomernogo analiza")
    print()
    print("  DOPOLNITELNO:")
    print("    11  Sozdat' VSE grafiki")
    print("    12  Informatsiya o proekte")
    print("     0  Vykhod")
    print()
    print("-"*80)


def create_all_plots(df):
    """Создание всех типов графиков"""
    print("\n" + "="*80)
    print("SOZDANIE VSEKH GRAFIKOV")
    print("="*80 + "\n")

    plots = [
        ("Линейный график", create_line_plot),
        ("Столбчатая диаграмма", create_bar_plot),
        ("Круговая диаграмма", create_pie_plot),
        ("Гистограмма", create_histogram),
        ("Точечная диаграмма", create_scatter_plot),
        ("Ящик с усами", create_box_plot),
        ("Тепловая карта", create_heatmap),
        ("Площадной график", create_area_plot),
        ("Скрипичная диаграмма", create_violin_plot),
        ("Pivot таблицы", create_pivot_plots)
    ]

    for i, (name, func) in enumerate(plots, 1):
        print(f"\n[{i}/{len(plots)}] Создание: {name}...")
        try:
            func(df)
        except Exception as e:
            print(f"❌ Ошибка при создании {name}: {e}")

    print("\n" + "="*80)
    print("VSE GRAFIKI USPESHNO SOZDANY!")
    print("="*80)
    print("\nGrafiki sokhraneny v papke: output/")


def show_project_info():
    """Показать информацию о проекте"""
    print("\n" + "="*80)
    print("INFORMATSIYA O PROEKTE")
    print("="*80)
    print()
    print("Chto eto za proyekt?")
    print("   Interaktivnyy obuchayushchiy proyekt dlya izucheniya vizualizatsii dannykh")
    print("   s pomoshch'yu biblioteki matplotlib i pandas.")
    print()
    print("Tsel' proekta:")
    print("   - Ponyat', kogda kakoy tip grafika ispol'zovat'")
    print("   - Nauchit'sya sozdavat' krasivye vizualizatsii")
    print("   - Osvoit' rabotu s pivot tablitsami")
    print("   - Izuchit' luchshie praktiki vizualizatsii dannykh")
    print()
    print("Chto vklyucheno:")
    print("   - 10 tipov grafikov s primerami")
    print("   - Podrobnye ob'yasneniya kazhdogo tipa")
    print("   - Kogda ispol'zovat' i kogda NE ispol'zovat'")
    print("   - Statisticheskiy analiz dannykh")
    print("   - Primery koda s kommentariyami")
    print()
    print("Struktura proekta:")
    print("   - plots/ - moduli dlya kazhdogo tipa grafika")
    print("   - utils/ - utility dlya generatsii dannykh")
    print("   - output/ - sgenerirova nnye grafiki")
    print()
    print("Tekhnologii:")
    print("   - matplotlib >= 3.7.0 - vizualizatsiya")
    print("   - pandas >= 2.0.0 - rabota s dannymi")
    print("   - numpy >= 1.24.0 - vychisleniya")
    print()
    print("Kak ispol'zovat':")
    print("   1. Vyberite tip grafika iz menyu")
    print("   2. Izuchite sozdannyy grafik v papke output/")
    print("   3. Chitayte ob'yasneniya v konsoli")
    print("   4. Smotrite kod v faylakh plots/*.py")
    print("   5. Eksperimentiruyte s parametrami!")
    print()
    print("Sovet:")
    print("   Nachnite s bazovykh grafikov (1-4), zatem perekhodite k analiticheskim.")
    print("   Kazhdyy grafik soderzhit 4 varianta ispol'zovaniya!")
    print()
    print("="*80)


def main():
    """Главная функция с меню"""
    # Создаем выходную папку
    os.makedirs('output', exist_ok=True)

    # Печатаем заголовок
    print_header()

    print("Dobro pozhalovat' v interaktivnyy obuchayushchiy proyekt!")
    print("Vy nauchites' sozdavat' razlichnye tipy grafikov i poymete,")
    print("kogda kakoy grafik ispol'zovat'.\n")

    # Создаем данные один раз
    print("[DATA] Sozdanie primernykh dannykh...")
    df = create_sample_data()
    print(f"Sozdano {len(df)} zapisey dlya analiza\n")

    # Главный цикл меню
    while True:
        print_menu()

        try:
            choice = input("Ваш выбор: ").strip()

            if choice == '0':
                print("\nSpasibo za ispol'zovanie! Udachi v izuchenii vizualizatsii dannykh!\n")
                break

            elif choice == '1':
                create_line_plot(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '2':
                create_bar_plot(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '3':
                create_pie_plot(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '4':
                create_histogram(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '5':
                create_scatter_plot(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '6':
                create_box_plot(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '7':
                create_violin_plot(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '8':
                create_heatmap(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '9':
                create_area_plot(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '10':
                create_pivot_plots(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '11':
                create_all_plots(df)
                input("\n[Нажмите Enter для продолжения...]")

            elif choice == '12':
                show_project_info()
                input("\n[Нажмите Enter для продолжения...]")

            else:
                print("\nNevernyy vybor! Pozhaluysta, vvedite chislo ot 0 do 12.")
                input("\n[Nazhmite Enter dlya prodolzheniya...]")

        except KeyboardInterrupt:
            print("\n\nProgramma prervana. Do svidaniya!")
            break
        except Exception as e:
            print(f"\nProizoshla oshibka: {e}")
            input("\n[Nazhmite Enter dlya prodolzheniya...]")


if __name__ == "__main__":
    main()
