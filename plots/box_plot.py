"""
📦 ЯЩИК С УСАМИ (Box Plot)

Описание:
    Показывает распределение данных через квартили.
    Отображает медиану, квартили, выбросы и разброс данных.

Когда использовать:
    ✓ Сравнить распределения между группами
    ✓ Найти выбросы (outliers)
    ✓ Понять разброс и асимметрию данных
    ✓ Сравнить медианы разных групп

Не использовать:
    ✗ Для небольших выборок (< 20 точек)
    ✗ Когда нужны точные значения
    ✗ Для временных рядов
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_box_plot(df, output_path='output/box_plot.png'):
    """
    Создание ящика с усами

    Args:
        df: DataFrame с данными
        output_path: путь для сохранения графика
    """
    print("\n" + "="*80)
    print("📦 ЯЩИК С УСАМИ (Box Plot)")
    print("="*80)

    print("\n💡 Box plot показывает распределение данных и выбросы.")
    print("   Линия внутри ящика = медиана, ящик = 50% данных, усы = основной разброс.\n")

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Box Plot: примеры использования', fontsize=16, fontweight='bold')

    # 1. Простой box plot
    data_to_plot = [df[df['Категория'] == cat]['Средняя_цена'].values
                    for cat in df['Категория'].unique()]
    bp = axes[0, 0].boxplot(data_to_plot, labels=df['Категория'].unique(),
                           patch_artist=True)

    # Раскрашиваем ящики
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    axes[0, 0].set_title('1️⃣ Простой Box Plot')
    axes[0, 0].set_ylabel('Средняя цена (руб.)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)

    # 2. Box plot с выделением выбросов
    data_regions = [df[df['Регион'] == region]['Продажи'].values
                   for region in df['Регион'].unique()]
    bp2 = axes[0, 1].boxplot(data_regions, labels=df['Регион'].unique(),
                            patch_artist=True, showfliers=True,
                            flierprops=dict(marker='o', markerfacecolor='red',
                                          markersize=8, alpha=0.5))

    for patch in bp2['boxes']:
        patch.set_facecolor('#3498DB')
        patch.set_alpha(0.6)

    axes[0, 1].set_title('2️⃣ С выделением выбросов')
    axes[0, 1].set_ylabel('Продажи (руб.)')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(axis='y', alpha=0.3)

    # 3. Горизонтальный box plot
    data_h = [df[df['Категория'] == cat]['Продажи'].values
             for cat in df['Категория'].unique()]
    bp3 = axes[1, 0].boxplot(data_h, labels=df['Категория'].unique(),
                            vert=False, patch_artist=True)

    for patch, color in zip(bp3['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    axes[1, 0].set_title('3️⃣ Горизонтальный Box Plot')
    axes[1, 0].set_xlabel('Продажи (руб.)')
    axes[1, 0].grid(axis='x', alpha=0.3)

    # 4. Box plot с отображением средних
    data_mean = [df[df['Категория'] == cat]['Средняя_цена'].values
                for cat in df['Категория'].unique()]
    bp4 = axes[1, 1].boxplot(data_mean, labels=df['Категория'].unique(),
                            patch_artist=True, showmeans=True,
                            meanprops=dict(marker='D', markerfacecolor='red',
                                         markeredgecolor='red', markersize=8))

    for patch, color in zip(bp4['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    axes[1, 1].set_title('4️⃣ С отображением средних значений')
    axes[1, 1].set_ylabel('Средняя цена (руб.)')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(axis='y', alpha=0.3)

    # Добавляем легенду для последнего графика
    axes[1, 1].plot([], [], 'D', color='red', label='Среднее', markersize=8)
    axes[1, 1].plot([], [], '_', color='orange', linewidth=2, label='Медиана')
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: {output_path}")

    # Статистика по категориям
    print("\n📊 Статистика по категориям:")
    for cat in df['Категория'].unique():
        cat_data = df[df['Категория'] == cat]['Средняя_цена']
        q1 = cat_data.quantile(0.25)
        q2 = cat_data.quantile(0.50)  # медиана
        q3 = cat_data.quantile(0.75)
        iqr = q3 - q1

        print(f"\n   {cat}:")
        print(f"      • Медиана (Q2): {q2:.2f} руб.")
        print(f"      • Q1 (25%): {q1:.2f} руб.")
        print(f"      • Q3 (75%): {q3:.2f} руб.")
        print(f"      • IQR: {iqr:.2f} руб.")

    print("\n💡 Что показывает Box Plot:")
    print("   • Ящик = 50% данных (между Q1 и Q3)")
    print("   • Линия в ящике = медиана (Q2)")
    print("   • Усы = основной разброс данных")
    print("   • Точки за усами = выбросы")

    plt.close()

    return output_path
