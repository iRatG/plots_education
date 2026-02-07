"""
📊 СТОЛБЧАТАЯ ДИАГРАММА (Bar Plot)

Описание:
    Отображает данные в виде вертикальных или горизонтальных столбцов.
    Используется для сравнения значений между различными категориями.

Когда использовать:
    ✓ Сравнение значений между категориями
    ✓ Ранжирование и показ топов
    ✓ Сравнение показателей по разным группам
    ✓ Отображение дискретных данных

Не использовать:
    ✗ Для непрерывных временных рядов (лучше линейный график)
    ✗ Для показа частей целого (лучше круговая диаграмма)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def create_bar_plot(df, output_path='output/bar_plot.png'):
    """
    Создание столбчатой диаграммы

    Args:
        df: DataFrame с данными
        output_path: путь для сохранения графика
    """
    print("\n" + "="*80)
    print("📊 СТОЛБЧАТАЯ ДИАГРАММА (Bar Plot)")
    print("="*80)

    print("\n💡 Столбчатая диаграмма - лучший способ сравнить значения по категориям.")
    print("   Высота столбца показывает величину значения.\n")

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Столбчатые диаграммы: примеры использования', fontsize=16, fontweight='bold')

    # 1. Простая столбчатая диаграмма
    category_sales = df.groupby('Категория')['Продажи'].sum().sort_values(ascending=False)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    axes[0, 0].bar(category_sales.index, category_sales.values,
                  color=colors, edgecolor='white', linewidth=2)
    axes[0, 0].set_title('1️⃣ Простая столбчатая диаграмма')
    axes[0, 0].set_ylabel('Продажи (руб.)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)

    # Добавляем значения на столбцы
    for i, (idx, value) in enumerate(category_sales.items()):
        axes[0, 0].text(i, value, f'{value/1000:.0f}K',
                       ha='center', va='bottom', fontweight='bold')

    # 2. Группированная столбчатая диаграмма
    pivot = df.pivot_table(values='Продажи', index='Категория',
                          columns='Регион', aggfunc='sum', fill_value=0)
    x = np.arange(len(pivot.index))
    width = 0.25
    for i, region in enumerate(pivot.columns):
        offset = (i - len(pivot.columns)/2 + 0.5) * width
        axes[0, 1].bar(x + offset, pivot[region], width,
                      label=region, alpha=0.8)
    axes[0, 1].set_title('2️⃣ Группированная диаграмма')
    axes[0, 1].set_ylabel('Продажи (руб.)')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(pivot.index, rotation=45)
    axes[0, 1].legend()
    axes[0, 1].grid(axis='y', alpha=0.3)

    # 3. Горизонтальная столбчатая диаграмма
    region_sales = df.groupby('Регион')['Продажи'].sum().sort_values()
    axes[1, 0].barh(region_sales.index, region_sales.values,
                   color='#54A0FF', edgecolor='white', linewidth=2)
    axes[1, 0].set_title('3️⃣ Горизонтальная диаграмма')
    axes[1, 0].set_xlabel('Продажи (руб.)')
    axes[1, 0].grid(axis='x', alpha=0.3)

    # Добавляем значения
    for i, (idx, value) in enumerate(region_sales.items()):
        axes[1, 0].text(value, i, f' {value/1000:.0f}K',
                       va='center', fontweight='bold')

    # 4. Накопительная столбчатая диаграмма (Stacked)
    pivot_stack = df.pivot_table(values='Продажи', index='Регион',
                                 columns='Категория', aggfunc='sum', fill_value=0)
    pivot_stack.plot(kind='bar', stacked=True, ax=axes[1, 1],
                    colormap='Set3', edgecolor='white', linewidth=1.5)
    axes[1, 1].set_title('4️⃣ Накопительная диаграмма')
    axes[1, 1].set_ylabel('Продажи (руб.)')
    axes[1, 1].set_xlabel('')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].legend(title='Категория', bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1, 1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: {output_path}")

    # Статистика
    print("\n📊 Статистика по категориям:")
    for cat, value in category_sales.items():
        percentage = (value / category_sales.sum()) * 100
        print(f"   • {cat}: {value:,.0f} руб. ({percentage:.1f}%)")

    plt.close()

    return output_path


def get_code_example():
    """Возвращает примеры кода для обучения"""
    return {
        'title': 'Столбчатая диаграмма (Bar Plot)',
        'description': 'Сравнение значений по категориям',
        'when_use': 'Сравнение категорий, рейтинги, топы',
        'examples': [
            {
                'name': '1️⃣ Простая столбчатая',
                'code': '''# Подготовка данных
category_sales = df.groupby('Категория')['Продажи'].sum()
category_sales = category_sales.sort_values(ascending=False)

# Создание графика
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(category_sales.index,      # Категории (X)
       category_sales.values,       # Значения (Y)
       color='skyblue',             # Цвет столбцов
       edgecolor='navy',            # Цвет границ
       alpha=0.8)                   # Прозрачность

# Настройка
ax.set_title('Продажи по категориям')
ax.set_xlabel('Категория')
ax.set_ylabel('Продажи (руб.)')
ax.grid(True, alpha=0.3, axis='y')  # Сетка только по Y
ax.tick_params(axis='x', rotation=45)  # Поворот подписей

plt.tight_layout()
plt.savefig('bar_plot.png', dpi=300)'''
            },
            {
                'name': '2️⃣ Горизонтальная (сравнение)',
                'code': '''# Подготовка данных
category_sales = df.groupby('Категория')['Продажи'].sum()
category_sales = category_sales.sort_values()  # Сортировка по возрастанию

# Создание графика
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(category_sales.index,    # Категории (Y)
               category_sales.values,     # Значения (X)
               color='coral',
               edgecolor='darkred',
               alpha=0.8)

# Добавление значений на столбцы
for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2,
            f'{width:,.0f}',
            ha='left', va='center', fontsize=10)

# Настройка
ax.set_title('Топ продаж по категориям')
ax.set_xlabel('Продажи (руб.)')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('bar_horizontal.png', dpi=300)'''
            },
            {
                'name': '3️⃣ Группированная (сравнение групп)',
                'code': '''# Подготовка данных
pivot = df.pivot_table(values='Продажи',
                       index='Категория',
                       columns='Регион',
                       aggfunc='sum')

# Создание графика
fig, ax = plt.subplots(figsize=(12, 6))

# Параметры
x = range(len(pivot.index))
width = 0.25  # Ширина одного столбца
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

# Рисуем столбцы для каждого региона
for i, region in enumerate(pivot.columns):
    offset = width * (i - 1)  # Смещение
    ax.bar([xi + offset for xi in x],
           pivot[region],
           width=width,
           label=region,
           color=colors[i],
           alpha=0.8)

# Настройка
ax.set_title('Продажи по категориям и регионам')
ax.set_xlabel('Категория')
ax.set_ylabel('Продажи (руб.)')
ax.set_xticks(x)
ax.set_xticklabels(pivot.index, rotation=45)
ax.legend(title='Регион')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('bar_grouped.png', dpi=300)'''
            },
            {
                'name': '4️⃣ С градиентной заливкой',
                'code': '''# Подготовка данных
category_sales = df.groupby('Категория')['Продажи'].sum()
category_sales = category_sales.sort_values(ascending=False)

# Создание графика
fig, ax = plt.subplots(figsize=(10, 6))

# Создаем градиентные цвета (от темного к светлому)
colors = plt.cm.viridis(range(len(category_sales)))

bars = ax.bar(category_sales.index,
              category_sales.values,
              color=colors,          # Разные цвета
              edgecolor='white',
              linewidth=2)

# Добавляем значения сверху столбцов
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height,
            f'{height/1000:.0f}K',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Настройка
ax.set_title('Рейтинг продаж (с градиентом)')
ax.set_ylabel('Продажи (руб.)')
ax.grid(True, alpha=0.3, axis='y')
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('bar_gradient.png', dpi=300)'''
            }
        ],
        'tips': [
            '💡 barh() создает горизонтальные столбцы',
            '💡 Используйте edgecolor для границ столбцов',
            '💡 ax.text() добавляет подписи на столбцы',
            '💡 Сортируйте данные для лучшей читаемости',
            '💡 width параметр задает ширину столбцов в группах'
        ]
    }

