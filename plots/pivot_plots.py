"""
📊 ВИЗУАЛИЗАЦИЯ PIVOT ТАБЛИЦ

Описание:
    Специальные графики для многомерного анализа данных.
    Используют pivot таблицы pandas для агрегации и группировки.

Когда использовать:
    ✓ Многомерный анализ данных
    ✓ Сравнение значений по нескольким измерениям
    ✓ Агрегация данных (sum, mean, count)
    ✓ Бизнес-отчеты и дашборды

Типы:
    • Grouped bar chart - сравнение по группам
    • Heatmap - матричное представление
    • Stacked bar - вклад частей в целое
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def create_pivot_plots(df, output_path='output/pivot_plots.png'):
    """
    Создание графиков на основе pivot таблиц

    Args:
        df: DataFrame с данными
        output_path: путь для сохранения графика
    """
    print("\n" + "="*80)
    print("📊 ВИЗУАЛИЗАЦИЯ PIVOT ТАБЛИЦ")
    print("="*80)

    print("\n💡 Pivot таблицы позволяют агрегировать данные по нескольким измерениям.")
    print("   Это мощный инструмент для многомерного анализа!\n")

    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    fig.suptitle('Визуализация Pivot таблиц', fontsize=16, fontweight='bold')

    # 1. Группированная столбчатая диаграмма из pivot
    ax1 = fig.add_subplot(gs[0, 0])
    pivot1 = df.pivot_table(values='Продажи', index='Категория',
                           columns='Регион', aggfunc='sum', fill_value=0)
    pivot1.plot(kind='bar', ax=ax1, width=0.8, colormap='Set2', edgecolor='white', linewidth=1.5)
    ax1.set_title('1️⃣ Группированная диаграмма из Pivot')
    ax1.set_ylabel('Продажи (руб.)')
    ax1.set_xlabel('')
    ax1.legend(title='Регион', loc='upper right')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)

    # 2. Stacked bar chart из pivot
    ax2 = fig.add_subplot(gs[0, 1])
    pivot2 = df.pivot_table(values='Продажи', index='Регион',
                           columns='Категория', aggfunc='sum', fill_value=0)
    pivot2.plot(kind='bar', stacked=True, ax=ax2, colormap='Set3',
               edgecolor='white', linewidth=1.5)
    ax2.set_title('2️⃣ Накопительная диаграмма (Stacked)')
    ax2.set_ylabel('Продажи (руб.)')
    ax2.set_xlabel('')
    ax2.legend(title='Категория', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)

    # 3. Heatmap из pivot
    ax3 = fig.add_subplot(gs[1, :])
    pivot3 = df.pivot_table(values='Количество', index='Категория',
                           columns='Регион', aggfunc='mean', fill_value=0)
    im = ax3.imshow(pivot3.values, cmap='YlOrRd', aspect='auto')
    ax3.set_xticks(range(len(pivot3.columns)))
    ax3.set_yticks(range(len(pivot3.index)))
    ax3.set_xticklabels(pivot3.columns)
    ax3.set_yticklabels(pivot3.index)
    ax3.set_title('3️⃣ Heatmap: Среднее количество товаров по регионам')
    plt.colorbar(im, ax=ax3, label='Среднее количество')

    # Добавляем значения на heatmap
    for i in range(len(pivot3.index)):
        for j in range(len(pivot3.columns)):
            text_color = 'white' if pivot3.values[i, j] > pivot3.values.mean() else 'black'
            ax3.text(j, i, f'{pivot3.values[i, j]:.1f}',
                    ha='center', va='center', color=text_color,
                    fontweight='bold', fontsize=11)

    # 4. Множественные агрегации
    ax4 = fig.add_subplot(gs[2, 0])
    pivot4 = df.groupby('Категория').agg({
        'Продажи': ['sum', 'mean'],
        'Количество': 'sum'
    }).round(2)

    x = np.arange(len(pivot4.index))
    width = 0.35

    # Два набора столбцов
    ax4.bar(x - width/2, pivot4['Продажи']['sum']/1000, width,
           label='Сумма продаж (тыс.)', color='#3498DB', alpha=0.8)
    ax4_twin = ax4.twinx()
    ax4_twin.bar(x + width/2, pivot4['Количество']['sum'], width,
                label='Количество', color='#E74C3C', alpha=0.8)

    ax4.set_xlabel('Категория')
    ax4.set_ylabel('Продажи (тыс. руб.)', color='#3498DB')
    ax4_twin.set_ylabel('Количество', color='#E74C3C')
    ax4.set_title('4️⃣ График с двумя осями (множественные метрики)')
    ax4.set_xticks(x)
    ax4.set_xticklabels(pivot4.index, rotation=45)
    ax4.tick_params(axis='y', labelcolor='#3498DB')
    ax4_twin.tick_params(axis='y', labelcolor='#E74C3C')

    # Объединяем легенды
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    ax4.grid(axis='y', alpha=0.3)

    # 5. Временная pivot таблица
    ax5 = fig.add_subplot(gs[2, 1])
    df['Месяц'] = df['Дата'].dt.to_period('M')
    pivot5 = df.pivot_table(values='Продажи', index='Месяц',
                           columns='Категория', aggfunc='sum', fill_value=0)
    pivot5.plot(kind='line', ax=ax5, marker='o', linewidth=2.5, markersize=6)
    ax5.set_title('5️⃣ Временные ряды из Pivot')
    ax5.set_xlabel('Месяц')
    ax5.set_ylabel('Продажи (руб.)')
    ax5.legend(title='Категория', loc='best', frameon=True, fancybox=True)
    ax5.grid(True, alpha=0.3)
    ax5.tick_params(axis='x', rotation=45)

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: {output_path}")

    # Выводим примеры pivot таблиц
    print("\n📊 Пример 1: Продажи по категориям и регионам")
    print(pivot1.to_string())

    print("\n📊 Пример 2: Множественные агрегации")
    print(pivot4.to_string())

    print("\n💡 Основные функции агрегации в pivot:")
    print("   • sum - сумма")
    print("   • mean - среднее")
    print("   • count - количество")
    print("   • min/max - минимум/максимум")
    print("   • std - стандартное отклонение")

    print("\n💡 Примеры кода pivot таблиц:")
    print("   df.pivot_table(values='Продажи', index='Категория',")
    print("                  columns='Регион', aggfunc='sum')")

    plt.close()

    return output_path


def get_code_example():
    """Возвращает примеры кода для обучения"""
    return {
        'title': 'Pivot таблицы',
        'description': 'Многомерный анализ данных',
        'when_use': 'Агрегация, группировка, сводные таблицы',
        'examples': [
            {
                'name': '1️⃣ Простая pivot таблица',
                'code': '''# Создание pivot таблицы
pivot = df.pivot_table(
    values='Продажи',          # Что агрегируем
    index='Категория',          # Строки
    columns='Регион',           # Столбцы
    aggfunc='sum'              # Функция агрегации
)

# Визуализация
fig, ax = plt.subplots(figsize=(10, 6))
pivot.plot(kind='bar',
           ax=ax,
           color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
           width=0.8)

# Настройка
ax.set_title('Продажи: Категории × Регионы')
ax.set_xlabel('Категория')
ax.set_ylabel('Продажи (руб.)')
ax.legend(title='Регион')
ax.grid(True, alpha=0.3, axis='y')
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('pivot_simple.png', dpi=300)'''
            },
            {
                'name': '2️⃣ Накопительная pivot',
                'code': '''# Создание pivot таблицы
pivot = df.pivot_table(
    values='Продажи',
    index='Регион',
    columns='Категория',
    aggfunc='sum',
    fill_value=0              # Заполнить пропуски
)

# Визуализация stacked
fig, ax = plt.subplots(figsize=(10, 6))
pivot.plot(kind='bar',
           ax=ax,
           stacked=True,          # Накопительная
           colormap='Set3',
           edgecolor='white',
           linewidth=1.5)

# Настройка
ax.set_title('Структура продаж по регионам')
ax.set_xlabel('Регион')
ax.set_ylabel('Продажи (руб.)')
ax.legend(title='Категория', bbox_to_anchor=(1.05, 1))
ax.grid(True, alpha=0.3, axis='y')
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('pivot_stacked.png', dpi=300, bbox_inches='tight')'''
            },
            {
                'name': '3️⃣ Heatmap из pivot',
                'code': '''# Создание pivot таблицы
pivot = df.pivot_table(
    values='Продажи',
    index='Категория',
    columns='Регион',
    aggfunc='mean'
)

# Визуализация как heatmap
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(pivot.values,
               cmap='YlOrRd',
               aspect='auto')

# Настройка осей
ax.set_xticks(range(len(pivot.columns)))
ax.set_yticks(range(len(pivot.index)))
ax.set_xticklabels(pivot.columns)
ax.set_yticklabels(pivot.index)

# Добавляем значения
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        value = pivot.values[i, j]
        ax.text(j, i, f'{value:,.0f}',
                ha='center', va='center',
                color='white' if value > pivot.values.mean() else 'black')

# Colorbar
plt.colorbar(im, ax=ax, label='Средние продажи')

# Настройка
ax.set_title('Pivot Heatmap: Средние продажи')

plt.tight_layout()
plt.savefig('pivot_heatmap.png', dpi=300)'''
            },
            {
                'name': '4️⃣ Множественные агрегации',
                'code': '''# Pivot с несколькими функциями
pivot = df.pivot_table(
    values='Продажи',
    index='Категория',
    aggfunc=['sum', 'mean', 'count']  # Несколько функций
)

# Визуализация
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# График 1: Сумма
pivot['sum'].plot(kind='barh', ax=axes[0], color='skyblue')
axes[0].set_title('Сумма продаж')
axes[0].set_xlabel('Продажи (руб.)')
axes[0].grid(True, alpha=0.3, axis='x')

# График 2: Среднее
pivot['mean'].plot(kind='barh', ax=axes[1], color='coral')
axes[1].set_title('Среднее продаж')
axes[1].set_xlabel('Продажи (руб.)')
axes[1].grid(True, alpha=0.3, axis='x')

# График 3: Количество
pivot['count'].plot(kind='barh', ax=axes[2], color='lightgreen')
axes[2].set_title('Количество записей')
axes[2].set_xlabel('Записей')
axes[2].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('pivot_multi.png', dpi=300)'''
            }
        ],
        'tips': [
            '💡 aggfunc может быть: sum, mean, count, min, max, std',
            '💡 fill_value=0 заполняет пропущенные значения',
            '💡 margins=True добавляет итоговые строки',
            '💡 Можно использовать несколько функций в списке',
            '💡 pivot_table() мощнее чем groupby() для сложного анализа'
        ]
    }
