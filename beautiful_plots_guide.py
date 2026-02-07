"""
RUKOVODSTVO PO SOZDANIYU KRASIVYKH GRAFIKOV
Rasshirennye tekhniki stilizatsii matplotlib
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import patches
from matplotlib.gridspec import GridSpec
import sys
import io

# Nastroyka kodirovki dlya Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Настройка стиля
# plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def create_sample_data():
    """Создание данных для примеров"""
    np.random.seed(42)

    dates = pd.date_range('2024-01-01', periods=60, freq='D')
    categories = ['Смартфоны', 'Ноутбуки', 'Планшеты', 'Аксессуары']

    data = []
    for cat in categories:
        for date in dates:
            data.append({
                'Дата': date,
                'Категория': cat,
                'Продажи': np.random.randint(5000, 30000) + np.random.randn() * 2000,
                'Количество': np.random.randint(10, 100),
                'Рейтинг': np.random.uniform(3.5, 5.0)
            })

    return pd.DataFrame(data)


def style_1_modern_minimal(df):
    """
    [STYLE] СТИЛЬ 1: Современный минималистичный
    - Чистые линии
    - Пастельные цвета
    - Много белого пространства
    """
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('white')

    # Цветовая палитра
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

    # График 1: Элегантная линейная диаграмма
    ax1 = plt.subplot(2, 2, 1)
    for i, cat in enumerate(df['Категория'].unique()):
        data = df[df['Категория'] == cat].groupby('Дата')['Продажи'].mean()
        ax1.plot(data.index, data.values,
                color=colors[i], linewidth=2.5,
                label=cat, alpha=0.8,
                marker='o', markersize=3, markevery=5)

    ax1.set_title('[GRAPH] Динамика продаж по категориям',
                  fontsize=14, fontweight='600', pad=20)
    ax1.set_xlabel('')
    ax1.set_ylabel('Средние продажи (₽)', fontsize=11)
    ax1.legend(frameon=True, fancybox=True, shadow=True,
              loc='upper left', fontsize=10)
    ax1.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.tick_params(axis='x', rotation=30)

    # График 2: Градиентные столбцы
    ax2 = plt.subplot(2, 2, 2)
    category_sales = df.groupby('Категория')['Продажи'].sum().sort_values(ascending=False)
    bars = ax2.bar(range(len(category_sales)), category_sales.values,
                   color=colors, edgecolor='white', linewidth=2, alpha=0.85)

    # Добавляем значения на столбцы
    for i, (bar, value) in enumerate(zip(bars, category_sales.values)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{value/1000:.0f}K',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_title('[CHART] Общие продажи по категориям',
                  fontsize=14, fontweight='600', pad=20)
    ax2.set_xticks(range(len(category_sales)))
    ax2.set_xticklabels(category_sales.index, fontsize=10)
    ax2.set_ylabel('Продажи (₽)', fontsize=11)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='y', alpha=0.2, linestyle='--', linewidth=0.5)

    # График 3: Красивый scatter с градиентом
    ax3 = plt.subplot(2, 2, 3)
    for i, cat in enumerate(df['Категория'].unique()):
        data = df[df['Категория'] == cat]
        scatter = ax3.scatter(data['Количество'], data['Продажи'],
                            c=data['Рейтинг'], cmap='RdYlGn',
                            s=100, alpha=0.6, edgecolors='white',
                            linewidth=1.5, label=cat)

    ax3.set_title('[RADAR] Зависимость продаж от количества',
                  fontsize=14, fontweight='600', pad=20)
    ax3.set_xlabel('Количество единиц', fontsize=11)
    ax3.set_ylabel('Продажи (₽)', fontsize=11)
    ax3.legend(frameon=True, fancybox=True, shadow=True, fontsize=9)
    ax3.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    # График 4: Area chart с градиентом
    ax4 = plt.subplot(2, 2, 4)
    pivot = df.groupby(['Дата', 'Категория'])['Продажи'].sum().unstack(fill_value=0)
    pivot = pivot.rolling(window=7).mean()  # Сглаживание

    ax4.stackplot(pivot.index, *[pivot[col] for col in pivot.columns],
                 labels=pivot.columns, alpha=0.7, colors=colors)
    ax4.set_title('🌊 Накопительная динамика продаж',
                  fontsize=14, fontweight='600', pad=20)
    ax4.set_xlabel('')
    ax4.set_ylabel('Продажи (₽)', fontsize=11)
    ax4.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, fontsize=9)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.tick_params(axis='x', rotation=30)
    ax4.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('examples/style_1_modern_minimal.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Создан: examples/style_1_modern_minimal.png")
    plt.close()


def style_2_dark_theme(df):
    """
    [DARK] СТИЛЬ 2: Темная тема
    - Темный фон
    - Яркие контрастные цвета
    - Неоновый эффект
    """
    plt.style.use('dark_background')

    fig = plt.figure(figsize=(16, 10), facecolor='#1a1a1a')

    # Яркая неоновая палитра
    neon_colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00']

    # График 1: Неоновые линии
    ax1 = plt.subplot(2, 2, 1, facecolor='#0d0d0d')
    for i, cat in enumerate(df['Категория'].unique()):
        data = df[df['Категория'] == cat].groupby('Дата')['Продажи'].mean()
        ax1.plot(data.index, data.values,
                color=neon_colors[i], linewidth=3,
                label=cat, alpha=0.9, linestyle='-',
                marker='o', markersize=4, markevery=7)

    ax1.set_title('[*] Динамика продаж',
                  fontsize=14, fontweight='bold', color='white', pad=20)
    ax1.set_ylabel('Продажи (₽)', fontsize=11, color='white')
    ax1.legend(frameon=True, fancybox=True, fontsize=10,
              facecolor='#1a1a1a', edgecolor='cyan')
    ax1.grid(True, alpha=0.1, color='white', linestyle=':')
    ax1.tick_params(axis='x', rotation=30, colors='white')
    ax1.tick_params(axis='y', colors='white')

    # График 2: Светящиеся столбцы
    ax2 = plt.subplot(2, 2, 2, facecolor='#0d0d0d')
    category_sales = df.groupby('Категория')['Продажи'].sum().sort_values(ascending=False)
    bars = ax2.barh(range(len(category_sales)), category_sales.values,
                    color=neon_colors, edgecolor='white', linewidth=2, alpha=0.8)

    ax2.set_title('[TOP] Рейтинг категорий',
                  fontsize=14, fontweight='bold', color='white', pad=20)
    ax2.set_yticks(range(len(category_sales)))
    ax2.set_yticklabels(category_sales.index, fontsize=10, color='white')
    ax2.set_xlabel('Продажи (₽)', fontsize=11, color='white')
    ax2.grid(axis='x', alpha=0.1, color='white', linestyle=':')
    ax2.tick_params(colors='white')

    # График 3: Heatmap в темной теме
    ax3 = plt.subplot(2, 2, 3, facecolor='#0d0d0d')
    df['Неделя'] = df['Дата'].dt.isocalendar().week
    pivot = df.pivot_table(values='Продажи', index='Категория',
                          columns='Неделя', aggfunc='mean', fill_value=0)
    pivot = pivot.iloc[:, :8]  # Первые 8 недель

    im = ax3.imshow(pivot.values, cmap='plasma', aspect='auto', interpolation='bilinear')
    ax3.set_xticks(range(len(pivot.columns)))
    ax3.set_yticks(range(len(pivot.index)))
    ax3.set_xticklabels(pivot.columns, color='white')
    ax3.set_yticklabels(pivot.index, color='white')
    ax3.set_title('[HEAT] Heatmap продаж по неделям',
                  fontsize=14, fontweight='bold', color='white', pad=20)
    cbar = plt.colorbar(im, ax=ax3)
    cbar.ax.tick_params(colors='white')

    # График 4: Радиальная диаграмма
    ax4 = plt.subplot(2, 2, 4, projection='polar', facecolor='#0d0d0d')
    categories = df['Категория'].unique()
    values = [df[df['Категория'] == cat]['Продажи'].sum() for cat in categories]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    ax4.plot(angles, values, 'o-', linewidth=2, color='cyan', markersize=8)
    ax4.fill(angles, values, alpha=0.25, color='cyan')
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(categories, color='white', fontsize=10)
    ax4.set_title('[RADAR] Радар продаж', fontsize=14, fontweight='bold',
                  color='white', pad=30)
    ax4.grid(True, color='white', alpha=0.2)
    ax4.tick_params(colors='white')

    plt.tight_layout()
    plt.savefig('examples/style_2_dark_theme.png', dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    print("✅ Создан: examples/style_2_dark_theme.png")
    plt.close()

    # Возвращаем светлый стиль
    # plt.style.use('seaborn-v0_8-darkgrid')


def style_3_professional_report(df):
    """
    [CHART] СТИЛЬ 3: Профессиональный отчет
    - Корпоративные цвета
    - Аннотации и метрики
    - Информативный дизайн
    """
    fig = plt.figure(figsize=(18, 12), facecolor='white')
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

    # Корпоративная палитра
    corp_colors = ['#2E4057', '#048A81', '#54C6EB', '#F18F01']

    # Заголовок отчета
    fig.suptitle('[GRAPH] ЕЖЕМЕСЯЧНЫЙ ОТЧЕТ ПО ПРОДАЖАМ',
                fontsize=20, fontweight='bold', y=0.98)

    # КПИ панель
    ax_kpi = fig.add_subplot(gs[0, :])
    ax_kpi.axis('off')

    total_sales = df['Продажи'].sum()
    avg_sales = df['Продажи'].mean()
    total_items = df['Количество'].sum()
    avg_rating = df['Рейтинг'].mean()

    kpis = [
        ('[$] Общие продажи', f'{total_sales/1000000:.2f}М ₽', corp_colors[0]),
        ('[CHART] Средний чек', f'{avg_sales:,.0f} ₽', corp_colors[1]),
        ('[BOX] Продано единиц', f'{total_items:,}', corp_colors[2]),
        ('[*] Средний рейтинг', f'{avg_rating:.2f}/5.0', corp_colors[3])
    ]

    for i, (label, value, color) in enumerate(kpis):
        x = 0.125 + i * 0.22
        # Фон для KPI
        rect = patches.FancyBboxPatch((x-0.08, 0.3), 0.16, 0.4,
                                     boxstyle="round,pad=0.01",
                                     facecolor=color, alpha=0.15,
                                     edgecolor=color, linewidth=2,
                                     transform=ax_kpi.transAxes)
        ax_kpi.add_patch(rect)

        ax_kpi.text(x, 0.65, label, transform=ax_kpi.transAxes,
                   fontsize=11, ha='center', fontweight='600')
        ax_kpi.text(x, 0.4, value, transform=ax_kpi.transAxes,
                   fontsize=16, ha='center', fontweight='bold', color=color)

    # График 1: Тренд с доверительным интервалом
    ax1 = fig.add_subplot(gs[1, :2])
    daily_data = df.groupby('Дата')['Продажи'].agg(['mean', 'std']).reset_index()

    ax1.plot(daily_data['Дата'], daily_data['mean'],
            color=corp_colors[0], linewidth=2.5, label='Среднее')
    ax1.fill_between(daily_data['Дата'],
                     daily_data['mean'] - daily_data['std'],
                     daily_data['mean'] + daily_data['std'],
                     alpha=0.2, color=corp_colors[0], label='±1σ')

    ax1.set_title('Динамика продаж с доверительным интервалом',
                  fontsize=12, fontweight='600', pad=15)
    ax1.set_xlabel('Дата', fontsize=10)
    ax1.set_ylabel('Продажи (₽)', fontsize=10)
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='x', rotation=30)

    # График 2: Top категории с процентами
    ax2 = fig.add_subplot(gs[1, 2])
    category_sales = df.groupby('Категория')['Продажи'].sum().sort_values(ascending=True)
    percentages = (category_sales / category_sales.sum() * 100)

    bars = ax2.barh(category_sales.index, category_sales.values,
                   color=corp_colors, alpha=0.8, edgecolor='white', linewidth=2)

    for i, (bar, pct) in enumerate(zip(bars, percentages)):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2,
                f' {pct:.1f}%', va='center', fontsize=10, fontweight='bold')

    ax2.set_title('Распределение по категориям', fontsize=12, fontweight='600', pad=15)
    ax2.set_xlabel('Продажи (₽)', fontsize=10)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')

    # График 3: Детальный pivot анализ
    ax3 = fig.add_subplot(gs[2, :2])
    df['Месяц'] = df['Дата'].dt.month
    pivot = df.pivot_table(values='Продажи', index='Категория',
                          columns='Месяц', aggfunc='sum', fill_value=0)

    x = np.arange(len(pivot.columns))
    width = 0.2

    for i, cat in enumerate(pivot.index):
        offset = (i - len(pivot.index)/2) * width
        bars = ax3.bar(x + offset, pivot.loc[cat], width,
                      label=cat, color=corp_colors[i], alpha=0.8)

    ax3.set_title('Помесячная динамика по категориям',
                  fontsize=12, fontweight='600', pad=15)
    ax3.set_xlabel('Месяц', fontsize=10)
    ax3.set_ylabel('Продажи (₽)', fontsize=10)
    ax3.set_xticks(x)
    ax3.set_xticklabels([f'М{i}' for i in pivot.columns])
    ax3.legend(loc='upper left', frameon=True, ncol=2)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')

    # График 4: Scatter с трендом
    ax4 = fig.add_subplot(gs[2, 2])
    for i, cat in enumerate(df['Категория'].unique()):
        data = df[df['Категория'] == cat]
        ax4.scatter(data['Количество'], data['Продажи'],
                   color=corp_colors[i], s=50, alpha=0.6,
                   label=cat, edgecolors='white', linewidth=0.5)

        # Линия тренда
        z = np.polyfit(data['Количество'], data['Продажи'], 1)
        p = np.poly1d(z)
        ax4.plot(data['Количество'].sort_values(),
                p(data['Количество'].sort_values()),
                color=corp_colors[i], linestyle='--', linewidth=1.5, alpha=0.7)

    ax4.set_title('Корреляция: Количество vs Продажи',
                  fontsize=12, fontweight='600', pad=15)
    ax4.set_xlabel('Количество единиц', fontsize=10)
    ax4.set_ylabel('Продажи (₽)', fontsize=10)
    ax4.legend(loc='upper left', frameon=True, fontsize=9)
    ax4.grid(True, alpha=0.3, linestyle='--')

    plt.savefig('examples/style_3_professional_report.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Создан: examples/style_3_professional_report.png")
    plt.close()


def style_4_creative_infographic(df):
    """
    [STYLE] СТИЛЬ 4: Креативная инфографика
    - Необычные формы
    - Яркие цвета
    - Визуальные элементы
    """
    fig = plt.figure(figsize=(16, 12), facecolor='#f0f0f0')

    # Яркая палитра
    bright_colors = ['#FF6B9D', '#C44569', '#FFA07A', '#98D8C8', '#6C5CE7']

    # Заголовок с эффектом
    fig.suptitle('[STYLE] КРЕАТИВНАЯ ВИЗУАЛИЗАЦИЯ ДАННЫХ',
                fontsize=22, fontweight='bold', y=0.98,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#FF6B9D',
                         alpha=0.3, edgecolor='#FF6B9D', linewidth=3))

    # График 1: Пузырьковая диаграмма
    ax1 = plt.subplot(2, 2, 1, facecolor='white')
    for i, cat in enumerate(df['Категория'].unique()):
        data = df[df['Категория'] == cat].sample(50)  # Случайная выборка
        sizes = data['Количество'] * 5
        ax1.scatter(data['Дата'], data['Продажи'],
                   s=sizes, alpha=0.6, color=bright_colors[i],
                   edgecolors='white', linewidth=2, label=cat)

    ax1.set_title('[BUBBLE] Пузырьковая диаграмма продаж',
                  fontsize=13, fontweight='bold', pad=15)
    ax1.set_ylabel('Продажи (₽)', fontsize=11, fontweight='600')
    ax1.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
    ax1.grid(True, alpha=0.2, linestyle=':', color='gray')
    ax1.tick_params(axis='x', rotation=30)

    # График 2: Донатный график (donut)
    ax2 = plt.subplot(2, 2, 2, facecolor='white')
    category_sales = df.groupby('Категория')['Продажи'].sum()

    wedges, texts, autotexts = ax2.pie(category_sales.values,
                                        labels=category_sales.index,
                                        autopct='%1.1f%%',
                                        colors=bright_colors[:len(category_sales)],
                                        startangle=90,
                                        pctdistance=0.85,
                                        explode=[0.05] * len(category_sales),
                                        shadow=True)

    # Создаем "дырку" для donut эффекта
    centre_circle = plt.Circle((0, 0), 0.70, fc='white', linewidth=3, edgecolor='gray')
    ax2.add_artist(centre_circle)

    for text in texts:
        text.set_fontsize(10)
        text.set_fontweight('bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    ax2.set_title('[DONUT] Распределение продаж',
                  fontsize=13, fontweight='bold', pad=15)

    # График 3: Waterfall chart (имитация)
    ax3 = plt.subplot(2, 2, 3, facecolor='white')
    monthly_sales = df.groupby(df['Дата'].dt.to_period('M'))['Продажи'].sum()
    monthly_change = monthly_sales.diff().fillna(0)

    colors_waterfall = ['green' if x > 0 else 'red' for x in monthly_change]
    bars = ax3.bar(range(len(monthly_change)), monthly_change.values,
                   color=colors_waterfall, alpha=0.7, edgecolor='white', linewidth=2)

    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.set_title('[CHART] Изменение продаж (месяц к месяцу)',
                  fontsize=13, fontweight='bold', pad=15)
    ax3.set_ylabel('Изменение (₽)', fontsize=11, fontweight='600')
    ax3.set_xlabel('Период', fontsize=11, fontweight='600')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')

    # График 4: Многослойная воронка
    ax4 = plt.subplot(2, 2, 4, facecolor='white')
    category_avg = df.groupby('Категория')['Продажи'].mean().sort_values(ascending=False)

    # Создаем эффект воронки
    for i, (cat, value) in enumerate(category_avg.items()):
        width = value / category_avg.max()
        rect = patches.FancyBboxPatch((0.5 - width/2, i), width, 0.8,
                                     boxstyle="round,pad=0.05",
                                     facecolor=bright_colors[i],
                                     alpha=0.7, edgecolor='white', linewidth=3)
        ax4.add_patch(rect)

        ax4.text(0.5, i + 0.4, f'{cat}\n{value:,.0f} ₽',
                ha='center', va='center', fontsize=11,
                fontweight='bold', color='white')

    ax4.set_xlim(0, 1)
    ax4.set_ylim(-0.5, len(category_avg))
    ax4.set_title('[RADAR] Средние продажи (воронка)',
                  fontsize=13, fontweight='bold', pad=15)
    ax4.axis('off')

    plt.tight_layout()
    plt.savefig('examples/style_4_creative_infographic.png', dpi=300, bbox_inches='tight',
                facecolor='#f0f0f0')
    print("✅ Создан: examples/style_4_creative_infographic.png")
    plt.close()


def tips_and_tricks():
    """
    💡 ПОЛЕЗНЫЕ СОВЕТЫ И ТРЮКИ
    """
    tips = """

╔═══════════════════════════════════════════════════════════════════════╗
║           💡 СОВЕТЫ ПО СОЗДАНИЮ КРАСИВЫХ ГРАФИКОВ                    ║
╚═══════════════════════════════════════════════════════════════════════╝

📌 ЦВЕТА И ПАЛИТРЫ:
   • Используйте готовые палитры: viridis, plasma, Set2, tab10
   • Для корпоративного стиля: #2E4057, #048A81, #54C6EB
   • Для темной темы: #00ffff, #ff00ff, #ffff00
   • Сервис для палитр: coolors.co, colorhunt.co

📌 ШРИФТЫ И РАЗМЕРЫ:
   plt.rcParams['font.size'] = 12
   plt.rcParams['axes.titlesize'] = 14
   plt.rcParams['axes.labelsize'] = 12
   plt.rcParams['legend.fontsize'] = 10

📌 СТИЛИ MATPLOTLIB:
   plt.style.use('seaborn-v0_8-darkgrid')  # Красивая сетка
   plt.style.use('ggplot')                 # Стиль R
   plt.style.use('bmh')                    # Для презентаций
   plt.style.use('dark_background')        # Темная тема

📌 УЛУЧШЕНИЕ ГРАФИКОВ:
   • Убирайте лишние границы: ax.spines['top'].set_visible(False)
   • Добавляйте прозрачность: alpha=0.7
   • Используйте белые границы: edgecolor='white', linewidth=2
   • Добавляйте тени: shadow=True
   • Сглаживайте данные: .rolling(window=7).mean()

📌 СОХРАНЕНИЕ:
   plt.savefig('file.png', dpi=300,              # Высокое качество
               bbox_inches='tight',               # Обрезать пустое место
               facecolor='white',                 # Цвет фона
               transparent=False)                 # Прозрачность

📌 ИНТЕРАКТИВНОСТЬ (для Jupyter):
   %matplotlib widget  # Интерактивные графики
   import plotly.express as px  # Для веб-графиков

📌 КОМБИНАЦИИ С PANDAS:
   df.plot(kind='bar', ...)          # Быстрые графики
   df.pivot_table(...).plot()        # Из pivot таблиц
   df.groupby(...).plot()            # С группировкой

📌 ЭКСПОРТ ДЛЯ ПРЕЗЕНТАЦИЙ:
   • PowerPoint: PNG, 300 DPI, 16:9 (1920x1080)
   • Веб: PNG, 150 DPI, оптимизировать размер
   • Печать: PDF или PNG, 300+ DPI
   • Социальные сети: PNG, квадрат (1080x1080)

📌 АНИМАЦИЯ (advanced):
   from matplotlib.animation import FuncAnimation
   # Создание анимированных графиков

╔═══════════════════════════════════════════════════════════════════════╗
║  🔗 ПОЛЕЗНЫЕ РЕСУРСЫ:                                                 ║
║  • matplotlib.org/stable/gallery - Галерея примеров                   ║
║  • seaborn.pydata.org - Красивая статистическая графика              ║
║  • plotly.com - Интерактивные графики                                ║
║  • chartjs.org - Для веб-приложений                                  ║
╚═══════════════════════════════════════════════════════════════════════╝
    """
    print(tips)


def main():
    """Главная функция"""
    print("\n" + "="*80)
    print("[STYLE] РУКОВОДСТВО ПО СОЗДАНИЮ КРАСИВЫХ ГРАФИКОВ")
    print("="*80)

    print("\n[CHART] Создание примерных данных...")
    df = create_sample_data()
    print(f"✅ Создано {len(df)} записей\n")

    print("[STYLE] Генерация графиков в различных стилях...\n")

    print("1️⃣  Современный минималистичный стиль...")
    style_1_modern_minimal(df)

    print("2️⃣  Темная тема (dark mode)...")
    style_2_dark_theme(df)

    print("3️⃣  Профессиональный отчет...")
    style_3_professional_report(df)

    print("4️⃣  Креативная инфографика...")
    style_4_creative_infographic(df)

    print("\n" + "="*80)
    print("✅ ВСЕ ГРАФИКИ УСПЕШНО СОЗДАНЫ!")
    print("="*80)

    print("\n📁 Созданные файлы:")
    print("   • examples/style_1_modern_minimal.png - Современный минималистичный стиль")
    print("   • examples/style_2_dark_theme.png - Темная тема с неоновыми цветами")
    print("   • examples/style_3_professional_report.png - Корпоративный отчет")
    print("   • examples/style_4_creative_infographic.png - Креативная инфографика")

    tips_and_tricks()

    print("\n" + "="*80)
    print("🎓 Изучайте код, экспериментируйте с параметрами!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
