"""
📈 ЛИНЕЙНЫЙ ГРАФИК (Line Plot)

Описание:
    Отображает данные в виде линии, соединяющей точки.
    Идеален для показа тренда и динамики изменений во времени.

Когда использовать:
    ✓ Временные ряды (продажи по дням, температура, курсы валют)
    ✓ Показ тренда и динамики изменений
    ✓ Сравнение нескольких временных рядов
    ✓ Прогнозирование и анализ трендов

Не использовать:
    ✗ Для категориальных данных без порядка
    ✗ Для сравнения частей целого
    ✗ Для показа распределения данных
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_line_plot(df, output_path='output/line_plot.png'):
    """
    Создание линейного графика

    Args:
        df: DataFrame с данными
        output_path: путь для сохранения графика
    """
    print("\n" + "="*80)
    print("📈 ЛИНЕЙНЫЙ ГРАФИК (Line Plot)")
    print("="*80)

    print("\n💡 Линейный график показывает динамику изменения данных во времени.")
    print("   Идеально подходит для анализа трендов и временных рядов.\n")

    # Создаем figure с несколькими вариантами
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Линейные графики: примеры использования', fontsize=16, fontweight='bold')

    # 1. Простой линейный график
    daily_sales = df.groupby('Дата')['Продажи'].sum().sort_index()
    axes[0, 0].plot(daily_sales.index, daily_sales.values,
                   color='#2E86DE', linewidth=2, marker='o', markersize=4)
    axes[0, 0].set_title('1️⃣ Простой линейный график')
    axes[0, 0].set_xlabel('Дата')
    axes[0, 0].set_ylabel('Продажи (руб.)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. Множественные линии (сравнение категорий)
    for category in df['Категория'].unique():
        cat_data = df[df['Категория'] == category].groupby('Дата')['Продажи'].sum().sort_index()
        axes[0, 1].plot(cat_data.index, cat_data.values,
                       marker='o', linewidth=2, label=category, markersize=3)
    axes[0, 1].set_title('2️⃣ Сравнение категорий')
    axes[0, 1].set_xlabel('Дата')
    axes[0, 1].set_ylabel('Продажи (руб.)')
    axes[0, 1].legend(loc='best')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].tick_params(axis='x', rotation=45)

    # 3. Линейный график со сглаживанием
    daily_sales_smooth = df.groupby('Дата')['Продажи'].sum().sort_index()
    rolling_mean = daily_sales_smooth.rolling(window=7).mean()

    axes[1, 0].plot(daily_sales_smooth.index, daily_sales_smooth.values,
                   color='lightgray', linewidth=1, alpha=0.5, label='Исходные данные')
    axes[1, 0].plot(rolling_mean.index, rolling_mean.values,
                   color='#EE5A6F', linewidth=2.5, label='Скользящее среднее (7 дней)')
    axes[1, 0].set_title('3️⃣ Сглаживание данных')
    axes[1, 0].set_xlabel('Дата')
    axes[1, 0].set_ylabel('Продажи (руб.)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(axis='x', rotation=45)

    # 4. Линейный график с заливкой области
    axes[1, 1].plot(daily_sales.index, daily_sales.values,
                   color='#00D2D3', linewidth=2.5)
    axes[1, 1].fill_between(daily_sales.index, daily_sales.values,
                           alpha=0.3, color='#00D2D3')
    axes[1, 1].set_title('4️⃣ С заливкой области')
    axes[1, 1].set_xlabel('Дата')
    axes[1, 1].set_ylabel('Продажи (руб.)')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: {output_path}")

    # Выводим информацию о данных
    print("\n📊 Статистика данных:")
    print(f"   • Всего точек данных: {len(daily_sales)}")
    print(f"   • Минимум: {daily_sales.min():,.0f} руб.")
    print(f"   • Максимум: {daily_sales.max():,.0f} руб.")
    print(f"   • Среднее: {daily_sales.mean():,.0f} руб.")

    plt.close()

    return output_path
