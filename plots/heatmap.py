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
