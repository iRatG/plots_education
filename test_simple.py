"""
Simple test for plot generation
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'DejaVu Sans'

from utils.data_generator import create_sample_data
import os

# Create output directory
os.makedirs('output', exist_ok=True)

# Generate data
print("Creating sample data...")
df = create_sample_data()
print(f"Created {len(df)} records")

# Test Line Plot
print("\nCreating line plot...")
fig, ax = plt.subplots(figsize=(10, 6))
daily_sales = df.groupby('Дата')['Продажи'].sum().sort_index()
ax.plot(daily_sales.index, daily_sales.values, marker='o', linewidth=2)
ax.set_title('Line Plot: Daily Sales', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Sales (rub.)')
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('output/test_line.png', dpi=300, bbox_inches='tight')
print("Saved: output/test_line.png")
plt.close()

# Test Bar Plot
print("\nCreating bar plot...")
fig, ax = plt.subplots(figsize=(10, 6))
category_sales = df.groupby('Категория')['Продажи'].sum().sort_values(ascending=False)
ax.bar(category_sales.index, category_sales.values, color='skyblue', edgecolor='navy')
ax.set_title('Bar Plot: Sales by Category', fontsize=14)
ax.set_ylabel('Sales (rub.)')
plt.xticks(rotation=45)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('output/test_bar.png', dpi=300, bbox_inches='tight')
print("Saved: output/test_bar.png")
plt.close()

print("\n" + "="*60)
print("SUCCESS! Plots created successfully.")
print("Check the output/ folder for generated plots.")
print("="*60)
