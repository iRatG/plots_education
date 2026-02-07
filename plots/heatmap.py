"""
🔥 ТЕПЛОВАЯ КАРТА (Heatmap)

Описание:
    Отображает данные в виде матрицы с цветовой кодировкой.
    Цвет каждой ячейки соответствует ее значению.

Когда использовать:
    ✓ Показать корреляции между переменными
    ✓ Визуализировать матрицы и таблицы
    ✓ Показать паттерны в данных
    ✓ Сравнить значения в двумерной сетке

Не использовать:
    ✗ Для одномерных данных
    ✗ Когда важны точные значения
    ✗ Для временных рядов (лучше line plot)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def create_heatmap(df, output_path='output/heatmap.png'):
    """
    Создание тепловой карты

    Args:
        df: DataFrame с данными
        output_path: путь для сохранения графика
    """
    print("\n" + "="*80)
    print("🔥 ТЕПЛОВАЯ КАРТА (Heatmap)")
    print("="*80)

    print("\n💡 Heatmap показывает данные через цвет.")
    print("   Чем ярче цвет - тем больше значение!\n")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Тепловые карты: примеры использования', fontsize=16, fontweight='bold')

    # 1. Простая heatmap (Продажи по категориям и регионам)
    pivot1 = df.pivot_table(values='Продажи', index='Категория',
                           columns='Регион', aggfunc='sum', fill_value=0)

    im1 = axes[0, 0].imshow(pivot1.values, cmap='YlOrRd', aspect='auto')
    axes[0, 0].set_xticks(range(len(pivot1.columns)))
    axes[0, 0].set_yticks(range(len(pivot1.index)))
    axes[0, 0].set_xticklabels(pivot1.columns)
    axes[0, 0].set_yticklabels(pivot1.index)
    axes[0, 0].set_title('1️⃣ Простая тепловая карта')
    plt.colorbar(im1, ax=axes[0, 0], label='Продажи (руб.)')

    # Добавляем значения на карту
    for i in range(len(pivot1.index)):
        for j in range(len(pivot1.columns)):
            text = axes[0, 0].text(j, i, f'{pivot1.values[i, j]/1000:.0f}K',
                                  ha='center', va='center',
                                  color='white' if pivot1.values[i, j] > pivot1.values.mean() else 'black',
                                  fontweight='bold', fontsize=10)

    # 2. Heatmap с другой цветовой схемой
    pivot2 = df.pivot_table(values='Количество', index='Категория',
                           columns='Регион', aggfunc='mean', fill_value=0)

    im2 = axes[0, 1].imshow(pivot2.values, cmap='viridis', aspect='auto')
    axes[0, 1].set_xticks(range(len(pivot2.columns)))
    axes[0, 1].set_yticks(range(len(pivot2.index)))
    axes[0, 1].set_xticklabels(pivot2.columns)
    axes[0, 1].set_yticklabels(pivot2.index)
    axes[0, 1].set_title('2️⃣ С цветовой схемой Viridis')
    plt.colorbar(im2, ax=axes[0, 1], label='Среднее количество')

    # Аннотации
    for i in range(len(pivot2.index)):
        for j in range(len(pivot2.columns)):
            axes[0, 1].text(j, i, f'{pivot2.values[i, j]:.1f}',
                          ha='center', va='center', color='white',
                          fontweight='bold', fontsize=10)

    # 3. Корреляционная матрица
    # Создаем числовые данные для корреляции
    numeric_data = df[['Продажи', 'Количество', 'Средняя_цена']].corr()

    im3 = axes[1, 0].imshow(numeric_data.values, cmap='coolwarm',
                           aspect='auto', vmin=-1, vmax=1)
    axes[1, 0].set_xticks(range(len(numeric_data.columns)))
    axes[1, 0].set_yticks(range(len(numeric_data.index)))
    axes[1, 0].set_xticklabels(numeric_data.columns, rotation=45, ha='right')
    axes[1, 0].set_yticklabels(numeric_data.index)
    axes[1, 0].set_title('3️⃣ Корреляционная матрица')
    plt.colorbar(im3, ax=axes[1, 0], label='Корреляция')

    # Добавляем значения корреляции
    for i in range(len(numeric_data.index)):
        for j in range(len(numeric_data.columns)):
            axes[1, 0].text(j, i, f'{numeric_data.values[i, j]:.2f}',
                          ha='center', va='center',
                          color='white' if abs(numeric_data.values[i, j]) > 0.5 else 'black',
                          fontweight='bold', fontsize=12)

    # 4. Heatmap по неделям
    df['Неделя'] = df['Дата'].dt.isocalendar().week
    pivot4 = df.pivot_table(values='Продажи', index='Категория',
                           columns='Неделя', aggfunc='sum', fill_value=0)
    pivot4 = pivot4.iloc[:, :10]  # Первые 10 недель

    im4 = axes[1, 1].imshow(pivot4.values, cmap='plasma', aspect='auto')
    axes[1, 1].set_xticks(range(len(pivot4.columns)))
    axes[1, 1].set_yticks(range(len(pivot4.index)))
    axes[1, 1].set_xticklabels(pivot4.columns)
    axes[1, 1].set_yticklabels(pivot4.index)
    axes[1, 1].set_xlabel('Неделя')
    axes[1, 1].set_title('4️⃣ Продажи по неделям')
    plt.colorbar(im4, ax=axes[1, 1], label='Продажи (руб.)')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: {output_path}")

    # Корреляционная статистика
    print("\n📊 Корреляционная матрица:")
    print(numeric_data.to_string())

    print("\n💡 Популярные цветовые схемы:")
    print("   • YlOrRd - желтый-оранжевый-красный (для позитивных значений)")
    print("   • viridis - универсальная, хорошая для дальтоников")
    print("   • coolwarm - синий-белый-красный (для корреляций)")
    print("   • plasma - яркая, современная")

    plt.close()

    return output_path


def get_code_example():
    """Возвращает примеры кода для обучения"""
    return {
        'title': 'Тепловая карта (Heatmap)',
        'description': 'Визуализация матричных данных',
        'when_use': 'Корреляции, паттерны, матрицы',
        'examples': [
            {
                'name': '1️⃣ Простая heatmap',
                'code': '''# Подготовка данных
pivot = df.pivot_table(values='Продажи',
                       index='Категория',
                       columns='Регион',
                       aggfunc='mean')

# Создание графика
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(pivot.values,
               cmap='YlOrRd',          # Цветовая карта
               aspect='auto')          # Автоподбор пропорций

# Настройка осей
ax.set_xticks(range(len(pivot.columns)))
ax.set_yticks(range(len(pivot.index)))
ax.set_xticklabels(pivot.columns)
ax.set_yticklabels(pivot.index)

# Colorbar
plt.colorbar(im, ax=ax, label='Средние продажи')

# Настройка
ax.set_title('Средние продажи: Категории x Регионы')

plt.tight_layout()
plt.savefig('heatmap_simple.png', dpi=300)'''
            },
            {
                'name': '2️⃣ С аннотациями',
                'code': '''# Подготовка данных
pivot = df.pivot_table(values='Продажи',
                       index='Категория',
                       columns='Регион',
                       aggfunc='sum')

# Создание графика
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(pivot.values, cmap='viridis', aspect='auto')

# Настройка осей
ax.set_xticks(range(len(pivot.columns)))
ax.set_yticks(range(len(pivot.index)))
ax.set_xticklabels(pivot.columns)
ax.set_yticklabels(pivot.index)

# Добавляем значения в ячейки
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        value = pivot.values[i, j]
        ax.text(j, i, f'{value/1000:.0f}K',
                ha='center', va='center',
                color='white' if value > pivot.values.mean() else 'black',
                fontweight='bold')

# Colorbar
plt.colorbar(im, ax=ax, label='Продажи (руб.)')

# Настройка
ax.set_title('Heatmap с аннотациями')

plt.tight_layout()
plt.savefig('heatmap_annotated.png', dpi=300)'''
            },
            {
                'name': '3️⃣ Корреляционная матрица',
                'code': '''# Подготовка данных - корреляции числовых столбцов
numeric_cols = ['Продажи', 'Количество', 'Средняя_цена']
correlation = df[numeric_cols].corr()

# Создание графика
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(correlation,
               cmap='coolwarm',        # Красный-синий
               vmin=-1, vmax=1,        # Диапазон от -1 до 1
               aspect='auto')

# Настройка осей
ax.set_xticks(range(len(correlation.columns)))
ax.set_yticks(range(len(correlation.index)))
ax.set_xticklabels(correlation.columns, rotation=45, ha='right')
ax.set_yticklabels(correlation.index)

# Добавляем значения корреляций
for i in range(len(correlation)):
    for j in range(len(correlation.columns)):
        value = correlation.iloc[i, j]
        ax.text(j, i, f'{value:.2f}',
                ha='center', va='center',
                color='white' if abs(value) > 0.5 else 'black',
                fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Корреляция')

# Настройка
ax.set_title('Корреляционная матрица')

plt.tight_layout()
plt.savefig('heatmap_correlation.png', dpi=300)'''
            },
            {
                'name': '4️⃣ Временной heatmap',
                'code': '''# Подготовка данных по дням недели
df['День_недели'] = df['Дата'].dt.day_name()
df['Неделя'] = df['Дата'].dt.isocalendar().week

pivot_time = df.pivot_table(
    values='Продажи',
    index='День_недели',
    columns='Неделя',
    aggfunc='sum'
)

# Правильный порядок дней
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
             'Friday', 'Saturday', 'Sunday']
pivot_time = pivot_time.reindex(day_order)

# Создание графика
fig, ax = plt.subplots(figsize=(14, 6))
im = ax.imshow(pivot_time.values, cmap='RdYlGn', aspect='auto')

# Настройка осей
ax.set_xticks(range(len(pivot_time.columns)))
ax.set_yticks(range(len(pivot_time.index)))
ax.set_xticklabels(pivot_time.columns)
ax.set_yticklabels(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'])

# Colorbar
plt.colorbar(im, ax=ax, label='Продажи (руб.)')

# Настройка
ax.set_title('Продажи по дням недели и неделям года')
ax.set_xlabel('Номер недели')
ax.set_ylabel('День недели')

plt.tight_layout()
plt.savefig('heatmap_time.png', dpi=300)'''
            }
        ],
        'tips': [
            '💡 cmap задает цветовую схему (viridis, YlOrRd, coolwarm)',
            '💡 aspect="auto" автоматически подбирает пропорции',
            '💡 vmin/vmax фиксируют диапазон значений',
            '💡 Добавляйте аннотации для точных значений',
            '💡 Корреляции лучше в coolwarm (красный-синий)'
        ]
    }
