"""
Flask Web Application for Interactive Data Visualization
"""

from flask import Flask, render_template, jsonify, request, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime
import os

from utils.data_generator import create_sample_data
from plots import (
    create_line_plot,
    create_bar_plot,
    create_pie_plot,
    create_histogram,
    create_scatter_plot,
    create_box_plot,
    create_heatmap,
    create_area_plot,
    create_violin_plot,
    create_pivot_plots
)
# Импорт функций для получения примеров кода
from plots.line_plot import get_code_example as get_line_code
from plots.bar_plot import get_code_example as get_bar_code
from plots.pie_plot import get_code_example as get_pie_code
from plots.scatter_plot import get_code_example as get_scatter_code
from plots.histogram import get_code_example as get_histogram_code
from plots.box_plot import get_code_example as get_box_code
from plots.heatmap import get_code_example as get_heatmap_code
from plots.area_plot import get_code_example as get_area_code
from plots.violin_plot import get_code_example as get_violin_code
from plots.pivot_plots import get_code_example as get_pivot_code

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Создаем папки если их нет
os.makedirs('static/plots', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Глобальная переменная для хранения данных
current_data = None


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/api/generate_data', methods=['POST'])
def generate_data():
    """Генерация новых данных"""
    global current_data

    try:
        data = request.get_json()
        num_records = int(data.get('num_records', 300))
        seed = int(data.get('seed', 42))

        # Генерируем данные
        current_data = create_sample_data(num_records=num_records, seed=seed)

        # Базовая статистика
        stats = {
            'total_records': len(current_data),
            'total_sales': float(current_data['Продажи'].sum()),
            'avg_sales': float(current_data['Продажи'].mean()),
            'categories': current_data['Категория'].unique().tolist(),
            'regions': current_data['Регион'].unique().tolist(),
            'date_range': {
                'start': current_data['Дата'].min().strftime('%Y-%m-%d'),
                'end': current_data['Дата'].max().strftime('%Y-%m-%d')
            }
        }

        # Первые 10 строк для предпросмотра
        preview = current_data.head(10).to_dict('records')

        # Форматируем даты
        for row in preview:
            row['Дата'] = row['Дата'].strftime('%Y-%m-%d')
            row['Продажи'] = f"{row['Продажи']:,.0f}"
            row['Средняя_цена'] = f"{row['Средняя_цена']:.2f}"

        return jsonify({
            'success': True,
            'stats': stats,
            'preview': preview
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/create_plot/<plot_type>', methods=['POST'])
def create_plot(plot_type):
    """Создание графика выбранного типа"""
    global current_data

    if current_data is None:
        return jsonify({
            'success': False,
            'error': 'Сначала сгенерируйте данные!'
        }), 400

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{plot_type}_{timestamp}.png'
        filepath = os.path.join('static', 'plots', filename)

        # Создаем график
        plot_functions = {
            'line': create_line_plot,
            'bar': create_bar_plot,
            'pie': create_pie_plot,
            'histogram': create_histogram,
            'scatter': create_scatter_plot,
            'box': create_box_plot,
            'heatmap': create_heatmap,
            'area': create_area_plot,
            'violin': create_violin_plot,
            'pivot': create_pivot_plots
        }

        if plot_type not in plot_functions:
            return jsonify({
                'success': False,
                'error': f'Неизвестный тип графика: {plot_type}'
            }), 400

        # Создаем график
        plot_functions[plot_type](current_data.copy(), filepath)

        return jsonify({
            'success': True,
            'image_url': f'/static/plots/{filename}',
            'plot_type': plot_type
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/data_table', methods=['GET'])
def get_data_table():
    """Получить полную таблицу данных"""
    global current_data

    if current_data is None:
        return jsonify({
            'success': False,
            'error': 'Данные не сгенерированы'
        }), 400

    try:
        # Преобразуем в список словарей
        data_list = current_data.to_dict('records')

        # Форматируем
        for row in data_list:
            row['Дата'] = row['Дата'].strftime('%Y-%m-%d')
            row['Продажи'] = f"{row['Продажи']:,.0f}"
            row['Средняя_цена'] = f"{row['Средняя_цена']:.2f}"

        return jsonify({
            'success': True,
            'data': data_list,
            'total': len(data_list)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Получить детальную статистику"""
    global current_data

    if current_data is None:
        return jsonify({
            'success': False,
            'error': 'Данные не сгенерированы'
        }), 400

    try:
        stats = {
            'общая_статистика': {
                'Всего записей': len(current_data),
                'Общие продажи': f"{current_data['Продажи'].sum():,.0f} ₽",
                'Средний чек': f"{current_data['Продажи'].mean():,.0f} ₽",
                'Общее количество': int(current_data['Количество'].sum())
            },
            'по_категориям': {},
            'по_регионам': {}
        }

        # Статистика по категориям
        for cat in current_data['Категория'].unique():
            cat_data = current_data[current_data['Категория'] == cat]
            stats['по_категориям'][cat] = {
                'Продажи': f"{cat_data['Продажи'].sum():,.0f} ₽",
                'Количество': int(cat_data['Количество'].sum()),
                'Записей': len(cat_data)
            }

        # Статистика по регионам
        for region in current_data['Регион'].unique():
            region_data = current_data[current_data['Регион'] == region]
            stats['по_регионам'][region] = {
                'Продажи': f"{region_data['Продажи'].sum():,.0f} ₽",
                'Количество': int(region_data['Количество'].sum()),
                'Записей': len(region_data)
            }

        return jsonify({
            'success': True,
            'statistics': stats
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/get_code/<plot_type>', methods=['GET'])
def get_code(plot_type):
    """Получить пример кода для типа графика"""
    try:
        # Словарь функций для получения кода
        code_functions = {
            'line': get_line_code,
            'bar': get_bar_code,
            'pie': get_pie_code,
            'scatter': get_scatter_code,
            'histogram': get_histogram_code,
            'box': get_box_code,
            'heatmap': get_heatmap_code,
            'area': get_area_code,
            'violin': get_violin_code,
            'pivot': get_pivot_code
        }

        if plot_type in code_functions:
            code_data = code_functions[plot_type]()
            return jsonify({
                'success': True,
                'code': code_data
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Примеры кода для {plot_type} пока не готовы'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Flask приложение запускается!")
    print("📊 Интерактивная визуализация данных")
    print("="*60)
    print("\n✅ Откройте в браузере: http://localhost:5000")
    print("⏹️  Нажмите Ctrl+C для остановки\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
