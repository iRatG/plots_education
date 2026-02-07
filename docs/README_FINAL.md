# 📊 Matplotlib Learning Project - Modular Structure

Interactive learning project for data visualization with matplotlib and pandas.

## ✨ What's New?

✅ **Modular structure** - each plot type in a separate file
✅ **Interactive menu** - choose which plot to learn
✅ **4 examples** for each plot type
✅ **Detailed explanations** - when to use each type
✅ **Russian language support** with fallback to English

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the test

```bash
python test_simple.py
```

This will create 2 test plots in the `output/` folder.

### 3. Explore plot types

Each plot module can be used independently:

```python
from utils.data_generator import create_sample_data
from plots import create_line_plot, create_bar_plot

# Generate data
df = create_sample_data()

# Create plots
create_line_plot(df)
create_bar_plot(df)
```

## 📂 Project Structure

```
plotlib/
├── test_simple.py       # ⭐ START HERE - Simple test
├── main.py              # Old version (all plots at once)
├── main_menu.py         # Interactive menu (may have encoding issues on Windows)
│
├── plots/               # 📊 Plot modules
│   ├── line_plot.py     # Line plots (time series)
│   ├── bar_plot.py      # Bar charts (comparisons)
│   ├── pie_plot.py      # Pie charts (parts of whole)
│   ├── histogram.py     # Histograms (distributions)
│   ├── scatter_plot.py  # Scatter plots (correlations)
│   ├── box_plot.py      # Box plots (statistics)
│   ├── heatmap.py       # Heatmaps (matrices)
│   ├── area_plot.py     # Area plots (volume)
│   ├── violin_plot.py   # Violin plots (distributions)
│   └── pivot_plots.py   # Pivot tables
│
├── utils/               # 🛠️ Utilities
│   └── data_generator.py
│
└── output/              # 📁 Generated plots
```

## 📊 Plot Types Overview

| Plot Type | Best For | Example Use Case |
|-----------|----------|------------------|
| **Line Plot** | Time series, trends | Sales over time, temperature |
| **Bar Plot** | Comparing categories | Sales by region, ratings |
| **Pie Chart** | Parts of whole (3-7 categories) | Market share, budget allocation |
| **Histogram** | Data distribution | Age distribution, price ranges |
| **Scatter Plot** | Correlations | Price vs quality, height vs weight |
| **Box Plot** | Statistical analysis | Comparing salary ranges |
| **Heatmap** | Matrices, patterns | Correlation matrix, sales calendar |
| **Area Plot** | Volume over time | Cumulative sales, stacked revenue |
| **Violin Plot** | Distribution density | Response time analysis |
| **Pivot Tables** | Multi-dimensional analysis | Sales by category and region |

## 💻 Usage Examples

### Example 1: Create a single plot

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from utils.data_generator import create_sample_data
from plots import create_line_plot

# Generate sample data
df = create_sample_data(num_records=300, seed=42)

# Create line plot
create_line_plot(df, output_path='output/my_line_plot.png')

print("Plot saved to output/my_line_plot.png")
```

### Example 2: Create multiple plots

```python
from utils.data_generator import create_sample_data
from plots import (create_line_plot, create_bar_plot,
                   create_scatter_plot, create_heatmap)

df = create_sample_data()

# Create different plot types
create_line_plot(df, 'output/line.png')
create_bar_plot(df, 'output/bar.png')
create_scatter_plot(df, 'output/scatter.png')
create_heatmap(df, 'output/heatmap.png')
```

### Example 3: Use your own data

```python
import pandas as pd
from plots import create_line_plot

# Load your data
df = pd.read_csv('your_data.csv')

# Make sure you have columns: Дата, Категория, Регион, Продажи, Количество
# Or modify the plot functions to match your column names

create_line_plot(df)
```

## 🎓 Learning Path

### Day 1: Basic Plots
1. Run `test_simple.py` to understand the basics
2. Explore `plots/line_plot.py` - understand time series
3. Explore `plots/bar_plot.py` - understand comparisons
4. Explore `plots/pie_plot.py` - understand proportions

### Day 2: Statistical Plots
5. Study `plots/histogram.py` - distributions
6. Study `plots/box_plot.py` - statistics
7. Study `plots/scatter_plot.py` - correlations

### Day 3: Advanced Plots
8. Study `plots/heatmap.py` - matrices
9. Study `plots/area_plot.py` - stacked data
10. Study `plots/violin_plot.py` - density
11. Study `plots/pivot_plots.py` - multi-dimensional

### Day 4: Styling
- Run `beautiful_plots_guide.py` for styling examples
- Customize colors, fonts, and layouts
- Create your own templates

## 🔧 Customization

### Change Data

Edit `utils/data_generator.py`:

```python
def create_sample_data(num_records=300, seed=42):
    categories = ['Electronics', 'Clothing', 'Food', 'Books']
    regions = ['Moscow', 'SPB', 'Ekaterinburg']
    # ... customize as needed
```

### Change Plot Style

Each plot file in `plots/` can be customized:
- Colors: Change the `colors` list
- Size: Modify `figsize=(width, height)`
- Font: Change `fontsize` parameters
- Grid: Adjust `alpha` values

## 📚 Additional Resources

- [Matplotlib Documentation](https://matplotlib.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Pandas Pivot Tables](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot_table.html)
- [Seaborn](https://seaborn.pydata.org/) - Higher-level plotting library

## 🐛 Troubleshooting

### Issue: Encoding errors on Windows

**Solution:** Use `test_simple.py` instead of `main_menu.py`

### Issue: "No module named 'plots'"

**Solution:** Make sure you're in the `plotlib/` directory when running scripts

### Issue: Plots not displaying

**Solution:** Plots are saved to `output/` folder. Check there for PNG files.

### Issue: Font warnings

**Solution:** This is normal. The default font will be used if DejaVu Sans is not available.

## 💡 Tips

1. **Start simple**: Begin with `test_simple.py`
2. **One at a time**: Study one plot type per day
3. **Read the code**: Each plot file has detailed comments
4. **Experiment**: Change parameters and see what happens
5. **Use your data**: Adapt the examples to your own datasets

## 📝 File Descriptions

| File | Description |
|------|-------------|
| `test_simple.py` | ⭐ Simple test - START HERE |
| `main.py` | Original version - creates all plots |
| `main_menu.py` | Interactive menu (encoding issues possible) |
| `beautiful_plots_guide.py` | Styling examples |
| `plots/*.py` | Individual plot modules |
| `utils/data_generator.py` | Sample data generation |

## 🎯 Project Goals

- ✅ Understand when to use each plot type
- ✅ Learn matplotlib fundamentals
- ✅ Master pivot tables
- ✅ Create beautiful visualizations
- ✅ Build reusable templates

## 🤝 How to Use This Project

1. **For Learning**: Start with `test_simple.py`, then explore individual plot files
2. **For Reference**: Check `plots/` folder for code examples
3. **For Projects**: Copy relevant plot functions to your project
4. **For Experimentation**: Modify parameters and see results

---

**Happy plotting! 📊🚀**

*Questions or improvements? Experiment with the code!*
