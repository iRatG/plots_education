"""
Генератор примерных данных для визуализации
"""

import pandas as pd
import numpy as np


def create_sample_data(num_records=300, seed=42):
    """
    Создание примерных данных для анализа

    Args:
        num_records: количество записей
        seed: seed для генератора случайных чисел

    Returns:
        DataFrame с колонками: Дата, Категория, Регион, Продажи, Количество, Средняя_цена
    """
    np.random.seed(seed)

    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    categories = ['Электроника', 'Одежда', 'Продукты', 'Книги']
    regions = ['Москва', 'Санкт-Петербург', 'Екатеринбург']

    data = {
        'Дата': np.random.choice(dates, num_records),
        'Категория': np.random.choice(categories, num_records),
        'Регион': np.random.choice(regions, num_records),
        'Продажи': np.random.randint(1000, 10000, num_records),
        'Количество': np.random.randint(1, 50, num_records)
    }

    df = pd.DataFrame(data)
    df['Средняя_цена'] = df['Продажи'] / df['Количество']

    return df


def create_time_series_data(days=60, categories=None, seed=42):
    """
    Создание данных временных рядов

    Args:
        days: количество дней
        categories: список категорий
        seed: seed для генератора

    Returns:
        DataFrame с временными рядами
    """
    np.random.seed(seed)

    if categories is None:
        categories = ['Смартфоны', 'Ноутбуки', 'Планшеты', 'Аксессуары']

    dates = pd.date_range('2024-01-01', periods=days, freq='D')

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
