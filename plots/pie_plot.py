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


def get_code_example():
    """Возвращает примеры кода для обучения"""
    return {
        'title': 'Круговая диаграмма (Pie Chart)',
        'description': 'Показывает части от целого',
        'when_use': 'Доли и проценты (3-7 категорий)',
        'examples': [
            {
                'name': '1️⃣ Простая круговая',
                'code': '''# Подготовка данных
region_sales = df.groupby('Регион')['Продажи'].sum()

# Создание графика
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(region_sales.values,         # Значения
       labels=region_sales.index,    # Подписи
       autopct='%1.1f%%',            # Формат процентов
       startangle=90,                # Начальный угол
       colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])  # Цвета

ax.set_title('Распределение продаж по регионам')

plt.tight_layout()
plt.savefig('pie_simple.png', dpi=300)'''
            },
            {
                'name': '2️⃣ С выделенным сектором',
                'code': '''# Подготовка данных
region_sales = df.groupby('Регион')['Продажи'].sum()
region_sales = region_sales.sort_values(ascending=False)

# Создание графика
fig, ax = plt.subplots(figsize=(8, 8))

# Выделяем самый большой сектор
explode = [0.1] + [0] * (len(region_sales) - 1)  # Первый выделен

ax.pie(region_sales.values,
       labels=region_sales.index,
       autopct='%1.1f%%',
       explode=explode,              # Выделение секторов
       shadow=True,                  # Тень
       startangle=90,
       colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])

ax.set_title('Лидер по продажам (выделен)')

plt.tight_layout()
plt.savefig('pie_exploded.png', dpi=300)'''
            },
            {
                'name': '3️⃣ Донатная диаграмма',
                'code': '''# Подготовка данных
category_sales = df.groupby('Категория')['Продажи'].sum()

# Создание графика
fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct='%1.1f%%',
    startangle=90,
    pctdistance=0.85,                # Расстояние процентов
    colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
)

# Создаем "дырку" в центре (donut)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
ax.add_artist(centre_circle)

# Стилизация текста
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax.set_title('Структура продаж (донат)')

plt.tight_layout()
plt.savefig('pie_donut.png', dpi=300)'''
            },
            {
                'name': '4️⃣ С подписями снаружи',
                'code': '''# Подготовка данных
category_sales = df.groupby('Категория')['Продажи'].sum()

# Создание графика
fig, ax = plt.subplots(figsize=(10, 8))

wedges, texts, autotexts = ax.pie(
    category_sales.values,
    autopct='%1.1f%%',
    startangle=90,
    colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)

# Добавляем подписи снаружи
ax.legend(wedges, category_sales.index,
          title="Категории",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

ax.set_title('Продажи по категориям')

plt.tight_layout()
plt.savefig('pie_legend.png', dpi=300, bbox_inches='tight')'''
            }
        ],
        'tips': [
            '💡 Используйте 3-7 категорий максимум',
            '💡 explode выделяет важные сектора',
            '💡 startangle=90 начинает с 12 часов',
            '💡 pctdistance регулирует положение процентов',
            '💡 Добавьте Circle для донатной диаграммы'
        ]
    }
