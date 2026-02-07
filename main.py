"""
Обучающий проект по matplotlib и pivot таблицам
Различные примеры визуализации данных
"""

import matplotlib
matplotlib.use('Agg')  # Использовать backend без GUI для Windows
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Настройка matplotlib для поддержки русского языка
plt.rcParams['font.family'] = 'DejaVu Sans'

def create_sample_data():
    """Создание примерных данных для анализа"""
    np.random.seed(42)

    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    categories = ['Электроника', 'Одежда', 'Продукты', 'Книги']
    regions = ['Москва', 'Санкт-Петербург', 'Екатеринбург']

    data = {
        'Дата': np.random.choice(dates, 300),
        'Категория': np.random.choice(categories, 300),
        'Регион': np.random.choice(regions, 300),
        'Продажи': np.random.randint(1000, 10000, 300),
        'Количество': np.random.randint(1, 50, 300)
    }

    df = pd.DataFrame(data)
    df['Средняя_цена'] = df['Продажи'] / df['Количество']

    return df

def example_1_basic_plots(df):
    """Пример 1: Базовые типы графиков"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Базовые типы графиков', fontsize=16, fontweight='bold')

    # 1. Линейный график
    daily_sales = df.groupby('Дата')['Продажи'].sum().sort_index()
    axes[0, 0].plot(daily_sales.index, daily_sales.values, marker='o', linewidth=2, markersize=4)
    axes[0, 0].set_title('Линейный график: Продажи по дням')
    axes[0, 0].set_xlabel('Дата')
    axes[0, 0].set_ylabel('Продажи (руб.)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. Столбчатая диаграмма
    category_sales = df.groupby('Категория')['Продажи'].sum().sort_values(ascending=False)
    axes[0, 1].bar(category_sales.index, category_sales.values, color='skyblue', edgecolor='navy')
    axes[0, 1].set_title('Столбчатая диаграмма: Продажи по категориям')
    axes[0, 1].set_ylabel('Продажи (руб.)')
    axes[0, 1].tick_params(axis='x', rotation=45)

    # 3. Круговая диаграмма
    region_sales = df.groupby('Регион')['Продажи'].sum()
    axes[1, 0].pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%',
                    startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99'])
    axes[1, 0].set_title('Круговая диаграмма: Распределение по регионам')

    # 4. Гистограмма
    axes[1, 1].hist(df['Средняя_цена'], bins=30, color='coral', edgecolor='black', alpha=0.7)
    axes[1, 1].set_title('Гистограмма: Распределение средней цены')
    axes[1, 1].set_xlabel('Средняя цена (руб.)')
    axes[1, 1].set_ylabel('Частота')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('examples/01_basic_plots.png', dpi=300, bbox_inches='tight')
    print("[OK] Сохранен: examples/01_basic_plots.png")
    plt.close()

def example_2_pivot_tables(df):
    """Пример 2: Работа с Pivot таблицами"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Визуализация Pivot таблиц', fontsize=16, fontweight='bold')

    # 1. Pivot: Категория vs Регион (продажи)
    pivot1 = df.pivot_table(values='Продажи', index='Категория',
                            columns='Регион', aggfunc='sum', fill_value=0)
    pivot1.plot(kind='bar', ax=axes[0, 0], width=0.8)
    axes[0, 0].set_title('Продажи по категориям и регионам')
    axes[0, 0].set_ylabel('Продажи (руб.)')
    axes[0, 0].legend(title='Регион', loc='upper right')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3, axis='y')

    # 2. Heatmap из pivot таблицы
    pivot2 = df.pivot_table(values='Количество', index='Категория',
                            columns='Регион', aggfunc='mean', fill_value=0)
    im = axes[0, 1].imshow(pivot2.values, cmap='YlOrRd', aspect='auto')
    axes[0, 1].set_xticks(range(len(pivot2.columns)))
    axes[0, 1].set_yticks(range(len(pivot2.index)))
    axes[0, 1].set_xticklabels(pivot2.columns)
    axes[0, 1].set_yticklabels(pivot2.index)
    axes[0, 1].set_title('Heatmap: Среднее количество товаров')
    plt.colorbar(im, ax=axes[0, 1], label='Количество')

    # Добавляем значения на heatmap
    for i in range(len(pivot2.index)):
        for j in range(len(pivot2.columns)):
            axes[0, 1].text(j, i, f'{pivot2.values[i, j]:.1f}',
                          ha='center', va='center', color='black', fontsize=10)

    # 3. Stacked bar chart из pivot
    pivot3 = df.pivot_table(values='Продажи', index='Регион',
                           columns='Категория', aggfunc='sum', fill_value=0)
    pivot3.plot(kind='bar', stacked=True, ax=axes[1, 0], colormap='Set3')
    axes[1, 0].set_title('Stacked Bar: Структура продаж по регионам')
    axes[1, 0].set_ylabel('Продажи (руб.)')
    axes[1, 0].legend(title='Категория', bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3, axis='y')

    # 4. Линейный график из pivot (временные ряды)
    df['Месяц'] = df['Дата'].dt.to_period('M')
    pivot4 = df.pivot_table(values='Продажи', index='Месяц',
                           columns='Категория', aggfunc='sum', fill_value=0)
    pivot4.plot(kind='line', ax=axes[1, 1], marker='o', linewidth=2)
    axes[1, 1].set_title('Динамика продаж по категориям')
    axes[1, 1].set_xlabel('Месяц')
    axes[1, 1].set_ylabel('Продажи (руб.)')
    axes[1, 1].legend(title='Категория', loc='best')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('examples/02_pivot_tables.png', dpi=300, bbox_inches='tight')
    print("[OK] Сохранен: examples/02_pivot_tables.png")
    plt.close()

def example_3_advanced_plots(df):
    """Пример 3: Продвинутые графики"""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    fig.suptitle('Продвинутые типы визуализации', fontsize=16, fontweight='bold')

    # 1. Scatter plot с размером точек
    ax1 = fig.add_subplot(gs[0, 0])
    for category in df['Категория'].unique():
        data = df[df['Категория'] == category]
        ax1.scatter(data['Количество'], data['Продажи'],
                   s=data['Средняя_цена']/10, alpha=0.6, label=category)
    ax1.set_xlabel('Количество')
    ax1.set_ylabel('Продажи (руб.)')
    ax1.set_title('Scatter: Продажи vs Количество')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Box plot
    ax2 = fig.add_subplot(gs[0, 1])
    data_to_plot = [df[df['Категория'] == cat]['Средняя_цена'].values
                    for cat in df['Категория'].unique()]
    bp = ax2.boxplot(data_to_plot, labels=df['Категория'].unique(), patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    ax2.set_title('Box Plot: Распределение цен по категориям')
    ax2.set_ylabel('Средняя цена (руб.)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')

    # 3. Violin plot (имитация)
    ax3 = fig.add_subplot(gs[0, 2])
    positions = []
    data_violin = []
    labels_violin = []
    for i, region in enumerate(df['Регион'].unique()):
        data = df[df['Регион'] == region]['Продажи'].values
        positions.append(i + 1)
        data_violin.append(data)
        labels_violin.append(region)
    parts = ax3.violinplot(data_violin, positions=positions, showmeans=True, showmedians=True)
    ax3.set_xticks(positions)
    ax3.set_xticklabels(labels_violin, rotation=45)
    ax3.set_title('Violin Plot: Распределение продаж')
    ax3.set_ylabel('Продажи (руб.)')
    ax3.grid(True, alpha=0.3, axis='y')

    # 4. Area plot
    ax4 = fig.add_subplot(gs[1, :])
    pivot_time = df.groupby(['Дата', 'Категория'])['Продажи'].sum().unstack(fill_value=0)
    pivot_time = pivot_time.sort_index()
    ax4.stackplot(pivot_time.index, *[pivot_time[col] for col in pivot_time.columns],
                 labels=pivot_time.columns, alpha=0.7)
    ax4.set_title('Area Plot: Накопительные продажи по времени')
    ax4.set_xlabel('Дата')
    ax4.set_ylabel('Продажи (руб.)')
    ax4.legend(loc='upper left')
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='x', rotation=45)

    # 5. Многоуровневый pivot - heatmap
    ax5 = fig.add_subplot(gs[2, :2])
    df['Неделя'] = df['Дата'].dt.isocalendar().week
    pivot_complex = df.pivot_table(values='Продажи', index='Категория',
                                   columns='Неделя', aggfunc='sum', fill_value=0)
    # Берем только первые 10 недель для наглядности
    pivot_complex = pivot_complex.iloc[:, :10]
    im = ax5.imshow(pivot_complex.values, cmap='viridis', aspect='auto')
    ax5.set_xticks(range(len(pivot_complex.columns)))
    ax5.set_yticks(range(len(pivot_complex.index)))
    ax5.set_xticklabels(pivot_complex.columns)
    ax5.set_yticklabels(pivot_complex.index)
    ax5.set_xlabel('Неделя')
    ax5.set_title('Heatmap: Продажи по неделям и категориям')
    plt.colorbar(im, ax=ax5, label='Продажи (руб.)')

    # 6. Horizontal bar with error
    ax6 = fig.add_subplot(gs[2, 2])
    category_stats = df.groupby('Категория')['Продажи'].agg(['mean', 'std'])
    ax6.barh(category_stats.index, category_stats['mean'],
            xerr=category_stats['std'], color='teal', alpha=0.7, capsize=5)
    ax6.set_xlabel('Средние продажи (руб.)')
    ax6.set_title('Продажи с погрешностью')
    ax6.grid(True, alpha=0.3, axis='x')

    plt.savefig('examples/03_advanced_plots.png', dpi=300, bbox_inches='tight')
    print("[OK] Сохранен: examples/03_advanced_plots.png")
    plt.close()

def example_4_interactive_pivot(df):
    """Пример 4: Интерактивные pivot таблицы и подграфики"""
    # Создаем сложную pivot таблицу
    pivot = df.pivot_table(
        values=['Продажи', 'Количество'],
        index=['Категория', 'Регион'],
        aggfunc={'Продажи': ['sum', 'mean'], 'Количество': ['sum', 'mean']},
        fill_value=0
    )

    print("\n" + "="*80)
    print("МНОГОУРОВНЕВАЯ PIVOT ТАБЛИЦА")
    print("="*80)
    print(pivot)
    print("\n")

    # Визуализация
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Анализ многоуровневой Pivot таблицы', fontsize=16, fontweight='bold')

    # 1. Сумма продаж
    pivot_sales_sum = df.pivot_table(values='Продажи', index='Категория',
                                     columns='Регион', aggfunc='sum', fill_value=0)
    pivot_sales_sum.plot(kind='barh', ax=axes[0, 0], width=0.7)
    axes[0, 0].set_title('Сумма продаж по категориям и регионам')
    axes[0, 0].set_xlabel('Продажи (руб.)')
    axes[0, 0].legend(title='Регион')
    axes[0, 0].grid(True, alpha=0.3, axis='x')

    # 2. Средние продажи
    pivot_sales_mean = df.pivot_table(values='Продажи', index='Категория',
                                      columns='Регион', aggfunc='mean', fill_value=0)
    pivot_sales_mean.plot(kind='bar', ax=axes[0, 1], width=0.7, colormap='Set2')
    axes[0, 1].set_title('Средние продажи по категориям и регионам')
    axes[0, 1].set_ylabel('Продажи (руб.)')
    axes[0, 1].legend(title='Регион')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True, alpha=0.3, axis='y')

    # 3. Сумма количества
    pivot_qty_sum = df.pivot_table(values='Количество', index='Категория',
                                   columns='Регион', aggfunc='sum', fill_value=0)
    pivot_qty_sum.plot(kind='area', ax=axes[1, 0], alpha=0.7, stacked=False)
    axes[1, 0].set_title('Количество товаров по категориям')
    axes[1, 0].set_xlabel('Категория')
    axes[1, 0].set_ylabel('Количество')
    axes[1, 0].legend(title='Регион', loc='upper left')
    axes[1, 0].grid(True, alpha=0.3)

    # 4. Комбинированный анализ
    combined = df.groupby('Категория').agg({
        'Продажи': ['sum', 'mean'],
        'Количество': ['sum', 'mean']
    }).round(2)

    ax = axes[1, 1]
    x = np.arange(len(combined.index))
    width = 0.35

    bars1 = ax.bar(x - width/2, combined['Продажи']['sum']/1000, width,
                   label='Сумма продаж (тыс. руб.)', color='skyblue')
    ax.set_ylabel('Продажи (тыс. руб.)', color='skyblue')
    ax.tick_params(axis='y', labelcolor='skyblue')

    ax2 = ax.twinx()
    bars2 = ax2.bar(x + width/2, combined['Количество']['sum'], width,
                    label='Сумма количества', color='coral')
    ax2.set_ylabel('Количество', color='coral')
    ax2.tick_params(axis='y', labelcolor='coral')

    ax.set_xlabel('Категория')
    ax.set_title('Двойная ось: Продажи и Количество')
    ax.set_xticks(x)
    ax.set_xticklabels(combined.index, rotation=45)

    # Объединяем легенды
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    plt.savefig('examples/04_interactive_pivot.png', dpi=300, bbox_inches='tight')
    print("[OK] Сохранен: examples/04_interactive_pivot.png")
    plt.close()

def print_pivot_examples(df):
    """Примеры использования pivot таблиц"""
    print("\n" + "="*80)
    print("ПРИМЕРЫ PIVOT ТАБЛИЦ")
    print("="*80)

    print("\n1. Простая pivot таблица (Категория x Регион):")
    pivot1 = df.pivot_table(values='Продажи', index='Категория',
                           columns='Регион', aggfunc='sum')
    print(pivot1)

    print("\n2. Pivot с несколькими агрегациями:")
    pivot2 = df.pivot_table(values='Продажи', index='Категория',
                           aggfunc=['sum', 'mean', 'count'])
    print(pivot2)

    print("\n3. Pivot с несколькими значениями:")
    pivot3 = df.pivot_table(values=['Продажи', 'Количество'],
                           index='Регион', aggfunc='sum')
    print(pivot3)

    print("\n4. Многоуровневая pivot таблица:")
    pivot4 = df.pivot_table(values='Продажи',
                           index=['Категория', 'Регион'],
                           aggfunc=['sum', 'mean', 'count'])
    print(pivot4)

    print("\n" + "="*80 + "\n")

def main():
    """Главная функция"""
    print("\n" + "="*80)
    print("ОБУЧАЮЩИЙ ПРОЕКТ: MATPLOTLIB И PIVOT ТАБЛИЦЫ")
    print("="*80)

    # Создаем данные
    print("\n[DATA] Создание примерных данных...")
    df = create_sample_data()
    print(f"[OK] Создано {len(df)} записей")
    print("\nПервые 10 строк данных:")
    print(df.head(10))

    # Примеры pivot таблиц
    print_pivot_examples(df)

    # Генерируем графики
    print("\n[PLOT] Генерация графиков...\n")

    print("1. Базовые графики...")
    example_1_basic_plots(df)

    print("\n2. Визуализация pivot таблиц...")
    example_2_pivot_tables(df)

    print("\n3. Продвинутые графики...")
    example_3_advanced_plots(df)

    print("\n4. Интерактивные pivot таблицы...")
    example_4_interactive_pivot(df)

    print("\n" + "="*80)
    print("[SUCCESS] ВСЕ ГРАФИКИ УСПЕШНО СОЗДАНЫ!")
    print("="*80)
    print("\nСозданные файлы:")
    print("  - examples/01_basic_plots.png - Базовые типы графиков")
    print("  - examples/02_pivot_tables.png - Визуализация pivot таблиц")
    print("  - examples/03_advanced_plots.png - Продвинутые графики")
    print("  - examples/04_interactive_pivot.png - Интерактивные pivot таблицы")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
