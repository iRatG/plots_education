"""
🎻 СКРИПИЧНАЯ ДИАГРАММА (Violin Plot)

Описание:
    Комбинация box plot и kernel density plot.
    Показывает распределение данных в виде "скрипки" - ширина = плотность.

Когда использовать:
    ✓ Показать полное распределение данных
    ✓ Сравнить распределения между группами
    ✓ Увидеть бимодальность и мультимодальность
    ✓ Когда box plot недостаточно информативен

Не использовать:
    ✗ Для небольших выборок (< 30 точек)
    ✗ Когда достаточно простого box plot
    ✗ Для категориальных данных
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_violin_plot(df, output_path='output/violin_plot.png'):
    """
    Создание скрипичной диаграммы

    Args:
        df: DataFrame с данными
        output_path: путь для сохранения графика
    """
    print("\n" + "="*80)
    print("🎻 СКРИПИЧНАЯ ДИАГРАММА (Violin Plot)")
    print("="*80)

    print("\n💡 Violin plot = box plot + показ плотности распределения.")
    print("   Ширина 'скрипки' показывает, где сконцентрировано больше данных.\n")

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Скрипичные диаграммы: примеры использования', fontsize=16, fontweight='bold')

    # 1. Простой violin plot (по категориям)
    positions = []
    data_violin = []
    labels_violin = []

    for i, cat in enumerate(df['Категория'].unique()):
        data = df[df['Категория'] == cat]['Средняя_цена'].values
        positions.append(i + 1)
        data_violin.append(data)
        labels_violin.append(cat)

    parts1 = axes[0, 0].violinplot(data_violin, positions=positions,
                                   showmeans=True, showmedians=True)

    # Раскрашиваем скрипки
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    for pc, color in zip(parts1['bodies'], colors):
        pc.set_facecolor(color)
        pc.set_alpha(0.7)

    axes[0, 0].set_xticks(positions)
    axes[0, 0].set_xticklabels(labels_violin, rotation=45)
    axes[0, 0].set_title('1️⃣ Простой Violin Plot')
    axes[0, 0].set_ylabel('Средняя цена (руб.)')
    axes[0, 0].grid(axis='y', alpha=0.3)

    # 2. Violin plot по регионам (продажи)
    positions2 = []
    data_violin2 = []
    labels_violin2 = []

    for i, region in enumerate(df['Регион'].unique()):
        data = df[df['Регион'] == region]['Продажи'].values
        positions2.append(i + 1)
        data_violin2.append(data)
        labels_violin2.append(region)

    parts2 = axes[0, 1].violinplot(data_violin2, positions=positions2,
                                   showmeans=True, showmedians=True,
                                   showextrema=True)

    for pc in parts2['bodies']:
        pc.set_facecolor('#3498DB')
        pc.set_alpha(0.6)
        pc.set_edgecolor('black')
        pc.set_linewidth(1.5)

    axes[0, 1].set_xticks(positions2)
    axes[0, 1].set_xticklabels(labels_violin2, rotation=45)
    axes[0, 1].set_title('2️⃣ С выделением экстремумов')
    axes[0, 1].set_ylabel('Продажи (руб.)')
    axes[0, 1].grid(axis='y', alpha=0.3)

    # 3. Горизонтальный violin plot
    parts3 = axes[1, 0].violinplot(data_violin, positions=positions,
                                   vert=False, showmeans=True, showmedians=True)

    for pc, color in zip(parts3['bodies'], colors):
        pc.set_facecolor(color)
        pc.set_alpha(0.7)

    axes[1, 0].set_yticks(positions)
    axes[1, 0].set_yticklabels(labels_violin)
    axes[1, 0].set_title('3️⃣ Горизонтальный Violin Plot')
    axes[1, 0].set_xlabel('Средняя цена (руб.)')
    axes[1, 0].grid(axis='x', alpha=0.3)

    # 4. Сравнение: Box vs Violin
    # Левая половина - box plot
    bp_data = [df[df['Категория'] == cat]['Количество'].values
              for cat in df['Категория'].unique()]
    bp = axes[1, 1].boxplot(bp_data, positions=[p - 0.2 for p in positions],
                           widths=0.3, patch_artist=True,
                           boxprops=dict(facecolor='lightblue', alpha=0.7))

    # Правая половина - violin plot
    vp_data = [df[df['Категория'] == cat]['Количество'].values
              for cat in df['Категория'].unique()]
    parts4 = axes[1, 1].violinplot(vp_data, positions=[p + 0.2 for p in positions],
                                   widths=0.3, showmeans=True)

    for pc in parts4['bodies']:
        pc.set_facecolor('lightcoral')
        pc.set_alpha(0.7)

    axes[1, 1].set_xticks(positions)
    axes[1, 1].set_xticklabels(labels_violin, rotation=45)
    axes[1, 1].set_title('4️⃣ Сравнение: Box vs Violin')
    axes[1, 1].set_ylabel('Количество товаров')
    axes[1, 1].legend([bp["boxes"][0], parts4['bodies'][0]], ['Box Plot', 'Violin Plot'])
    axes[1, 1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: {output_path}")

    # Статистика
    print("\n📊 Статистика распределений по категориям:")
    for cat in df['Категория'].unique():
        cat_data = df[df['Категория'] == cat]['Средняя_цена']
        print(f"\n   {cat}:")
        print(f"      • Среднее: {cat_data.mean():.2f} руб.")
        print(f"      • Медиана: {cat_data.median():.2f} руб.")
        print(f"      • Стд. откл.: {cat_data.std():.2f} руб.")

    print("\n💡 Violin Plot vs Box Plot:")
    print("   • Box Plot - показывает квартили и выбросы")
    print("   • Violin Plot - показывает полное распределение")
    print("   • Violin лучше для больших датасетов (>100 точек)")
    print("   • Box лучше для быстрого сравнения медиан")

    plt.close()

    return output_path
