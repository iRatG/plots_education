"""
🥧 КРУГОВАЯ ДИАГРАММА (Pie Chart)

Описание:
    Показывает части целого в виде секторов круга.
    Размер каждого сектора пропорционален его доле в общей сумме.

Когда использовать:
    ✓ Показать части от целого (проценты, доли)
    ✓ Для небольшого количества категорий (3-7)
    ✓ Когда важны пропорции, а не абсолютные значения
    ✓ Для простых сравнений долей

Не использовать:
    ✗ Для более чем 7 категорий (становится нечитаемым)
    ✗ Когда важны точные значения
    ✗ Для сравнения небольших различий
    ✗ Для временных рядов
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_pie_plot(df, output_path='output/pie_plot.png'):
    """
    Создание круговой диаграммы

    Args:
        df: DataFrame с данными
        output_path: путь для сохранения графика
    """
    print("\n" + "="*80)
    print("🥧 КРУГОВАЯ ДИАГРАММА (Pie Chart)")
    print("="*80)

    print("\n💡 Круговая диаграмма показывает части от целого.")
    print("   Размер каждого сектора = его доля в общей сумме.\n")

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Круговые диаграммы: примеры использования', fontsize=16, fontweight='bold')

    colors = ['#FF6B9D', '#C44569', '#FFA07A', '#98D8C8', '#6C5CE7']

    # 1. Простая круговая диаграмма
    region_sales = df.groupby('Регион')['Продажи'].sum()
    axes[0, 0].pie(region_sales.values, labels=region_sales.index,
                  autopct='%1.1f%%', startangle=90,
                  colors=colors[:len(region_sales)])
    axes[0, 0].set_title('1️⃣ Простая круговая диаграмма\n(Продажи по регионам)')

    # 2. Круговая диаграмма с взрывом (explode)
    category_sales = df.groupby('Категория')['Продажи'].sum()
    explode = [0.1 if i == category_sales.argmax() else 0
               for i in range(len(category_sales))]
    axes[0, 1].pie(category_sales.values, labels=category_sales.index,
                  autopct='%1.1f%%', startangle=90,
                  colors=colors[:len(category_sales)],
                  explode=explode, shadow=True)
    axes[0, 1].set_title('2️⃣ С выделением лидера\n(Продажи по категориям)')

    # 3. Донатная диаграмма (Donut Chart)
    wedges, texts, autotexts = axes[1, 0].pie(region_sales.values,
                                               labels=region_sales.index,
                                               autopct='%1.1f%%',
                                               startangle=90,
                                               colors=colors[:len(region_sales)],
                                               pctdistance=0.85)

    # Создаем "дырку" для donut эффекта
    centre_circle = plt.Circle((0, 0), 0.70, fc='white', linewidth=2, edgecolor='gray')
    axes[1, 0].add_artist(centre_circle)

    # Стилизуем текст
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    axes[1, 0].set_title('3️⃣ Донатная диаграмма\n(современный стиль)')

    # 4. Вложенная круговая диаграмма
    # Внешний круг - регионы
    region_data = df.groupby('Регион')['Продажи'].sum()
    size = 0.3

    # Внутренний круг
    axes[1, 1].pie(region_data.values, labels=region_data.index,
                  radius=1, colors=colors[:len(region_data)],
                  wedgeprops=dict(width=size, edgecolor='white', linewidth=2))

    # Внешний круг - категории
    category_data = df.groupby('Категория')['Продажи'].sum()
    axes[1, 1].pie(category_data.values, labels=category_data.index,
                  radius=1-size, colors=colors[:len(category_data)],
                  wedgeprops=dict(width=size, edgecolor='white', linewidth=2),
                  labeldistance=0.5)

    axes[1, 1].set_title('4️⃣ Вложенная диаграмма\n(регионы и категории)')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: {output_path}")

    # Статистика
    print("\n📊 Распределение по регионам:")
    total = region_sales.sum()
    for region, value in region_sales.items():
        percentage = (value / total) * 100
        print(f"   • {region}: {value:,.0f} руб. ({percentage:.1f}%)")

    print("\n⚠️  Совет: Используйте круговые диаграммы только для 3-7 категорий!")

    plt.close()

    return output_path
