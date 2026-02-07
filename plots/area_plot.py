"""
🌊 ПЛОЩАДНОЙ ГРАФИК (Area Plot)

Описание:
    Линейный график с заполненной областью под линией.
    Часто используется в накопительном виде (stacked area).

Когда использовать:
    ✓ Показать величину изменения во времени
    ✓ Показать вклад частей в общее (stacked)
    ✓ Подчеркнуть объем данных
    ✓ Сравнить накопительные тренды

Не использовать:
    ✗ Когда линии сильно пересекаются
    ✗ Для большого количества категорий (>5)
    ✗ Когда важны точные значения
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_area_plot(df, output_path='output/area_plot.png'):
    """
    Создание площадного графика

    Args:
        df: DataFrame с данными
        output_path: путь для сохранения графика
    """
    print("\n" + "="*80)
    print("🌊 ПЛОЩАДНОЙ ГРАФИК (Area Plot)")
    print("="*80)

    print("\n💡 Area plot показывает объем данных через заполненную область.")
    print("   Stacked area chart показывает вклад каждой части в общее.\n")

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Площадные графики: примеры использования', fontsize=16, fontweight='bold')

    # Подготовка данных
    daily_sales = df.groupby(['Дата', 'Категория'])['Продажи'].sum().unstack(fill_value=0)
    daily_sales = daily_sales.sort_index()

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

    # 1. Простой area plot (одна категория)
    total_sales = df.groupby('Дата')['Продажи'].sum().sort_index()
    axes[0, 0].fill_between(total_sales.index, total_sales.values,
                           alpha=0.7, color='#3498DB')
    axes[0, 0].plot(total_sales.index, total_sales.values,
                   color='#2874A6', linewidth=2)
    axes[0, 0].set_title('1️⃣ Простой площадной график')
    axes[0, 0].set_xlabel('Дата')
    axes[0, 0].set_ylabel('Продажи (руб.)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. Stacked area plot (накопительный)
    axes[0, 1].stackplot(daily_sales.index,
                        *[daily_sales[col] for col in daily_sales.columns],
                        labels=daily_sales.columns,
                        colors=colors[:len(daily_sales.columns)],
                        alpha=0.7)
    axes[0, 1].set_title('2️⃣ Накопительный (Stacked)')
    axes[0, 1].set_xlabel('Дата')
    axes[0, 1].set_ylabel('Продажи (руб.)')
    axes[0, 1].legend(loc='upper left', frameon=True, fancybox=True)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].tick_params(axis='x', rotation=45)

    # 3. Множественные area plot без stacking
    for i, col in enumerate(daily_sales.columns):
        axes[1, 0].fill_between(daily_sales.index, daily_sales[col],
                               alpha=0.4, color=colors[i], label=col)
        axes[1, 0].plot(daily_sales.index, daily_sales[col],
                       color=colors[i], linewidth=2)
    axes[1, 0].set_title('3️⃣ Множественные области (Overlapping)')
    axes[1, 0].set_xlabel('Дата')
    axes[1, 0].set_ylabel('Продажи (руб.)')
    axes[1, 0].legend(loc='upper left')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(axis='x', rotation=45)

    # 4. Area plot со сглаживанием
    daily_smooth = daily_sales.rolling(window=7).mean()
    axes[1, 1].stackplot(daily_smooth.index,
                        *[daily_smooth[col] for col in daily_smooth.columns],
                        labels=daily_smooth.columns,
                        colors=colors[:len(daily_smooth.columns)],
                        alpha=0.8)
    axes[1, 1].set_title('4️⃣ Сглаженный (7-дневное скользящее среднее)')
    axes[1, 1].set_xlabel('Дата')
    axes[1, 1].set_ylabel('Продажи (руб.)')
    axes[1, 1].legend(loc='upper left', frameon=True, fancybox=True)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: {output_path}")

    # Статистика по категориям
    print("\n📊 Вклад категорий в общие продажи:")
    category_totals = df.groupby('Категория')['Продажи'].sum().sort_values(ascending=False)
    total = category_totals.sum()

    for cat, value in category_totals.items():
        percentage = (value / total) * 100
        print(f"   • {cat}: {value:,.0f} руб. ({percentage:.1f}%)")

    print("\n💡 Когда использовать Area Plot:")
    print("   • Простой Area Plot - для одной переменной во времени")
    print("   • Stacked Area - для показа вклада частей в целое")
    print("   • Overlapping Area - для сравнения нескольких трендов")

    plt.close()

    return output_path


def get_code_example():
    """Возвращает примеры кода для обучения"""
    return {
        'title': 'Площадной график (Area Plot)',
        'description': 'Показывает объем данных во времени',
        'when_use': 'Накопительные данные, объемы',
        'examples': [
            {
                'name': '1️⃣ Простой area plot',
                'code': '''# Подготовка данных
daily_sales = df.groupby('Дата')['Продажи'].sum().sort_index()

# Создание графика
fig, ax = plt.subplots(figsize=(12, 6))
ax.fill_between(daily_sales.index,    # X
                daily_sales.values,     # Y
                alpha=0.5,              # Прозрачность
                color='skyblue')

# Добавляем линию сверху
ax.plot(daily_sales.index, daily_sales.values,
        color='blue', linewidth=2)

# Настройка
ax.set_title('Динамика продаж (площадь)')
ax.set_xlabel('Дата')
ax.set_ylabel('Продажи (руб.)')
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('area_simple.png', dpi=300)'''
            },
            {
                'name': '2️⃣ Накопительный (stacked)',
                'code': '''# Подготовка данных
pivot = df.groupby(['Дата', 'Категория'])['Продажи'].sum().unstack(fill_value=0)

# Создание графика
fig, ax = plt.subplots(figsize=(12, 6))

# Цвета
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

# Stacked area plot
ax.stackplot(pivot.index,
             *[pivot[col] for col in pivot.columns],
             labels=pivot.columns,
             colors=colors,
             alpha=0.7)

# Настройка
ax.set_title('Накопительная динамика продаж по категориям')
ax.set_xlabel('Дата')
ax.set_ylabel('Продажи (руб.)')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('area_stacked.png', dpi=300)'''
            },
            {
                'name': '3️⃣ С несколькими областями',
                'code': '''# Создание графика
fig, ax = plt.subplots(figsize=(12, 6))

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

# Рисуем область для каждой категории
for i, category in enumerate(df['Категория'].unique()):
    cat_data = df[df['Категория'] == category]
    cat_sales = cat_data.groupby('Дата')['Продажи'].sum().sort_index()

    ax.fill_between(cat_sales.index,
                    cat_sales.values,
                    alpha=0.3,
                    color=colors[i],
                    label=category)

    # Линия сверху
    ax.plot(cat_sales.index, cat_sales.values,
            color=colors[i], linewidth=2)

# Настройка
ax.set_title('Сравнение объемов продаж')
ax.set_xlabel('Дата')
ax.set_ylabel('Продажи (руб.)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('area_multiple.png', dpi=300)'''
            },
            {
                'name': '4️⃣ С градиентной заливкой',
                'code': '''# Подготовка данных
daily_sales = df.groupby('Дата')['Продажи'].sum().sort_index()

# Создание графика
fig, ax = plt.subplots(figsize=(12, 6))

# Рисуем область с градиентом
ax.fill_between(daily_sales.index,
                daily_sales.values,
                alpha=0.6,
                color='purple',
                label='Продажи')

# Добавляем среднюю линию
mean_line = daily_sales.mean()
ax.axhline(mean_line, color='red',
           linestyle='--', linewidth=2,
           label=f'Среднее: {mean_line:,.0f}')

# Закрашиваем область выше среднего
ax.fill_between(daily_sales.index,
                daily_sales.values,
                mean_line,
                where=(daily_sales.values >= mean_line),
                alpha=0.3,
                color='green',
                label='Выше среднего')

# Настройка
ax.set_title('Продажи относительно среднего')
ax.set_xlabel('Дата')
ax.set_ylabel('Продажи (руб.)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('area_gradient.png', dpi=300)'''
            }
        ],
        'tips': [
            '💡 fill_between() создает заливку между линиями',
            '💡 stackplot() для накопительных графиков',
            '💡 where параметр условно закрашивает области',
            '💡 alpha<1 для видимости наложений',
            '💡 Хорош для показа объемов и накоплений'
        ]
    }
