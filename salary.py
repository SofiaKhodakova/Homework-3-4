# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('Зарплаты.xlsx', sheet_name='Зарплаты')

data = {
    'Экономическая деятельность': [
        'Добыча полезных ископаемых',
        'Строительство',
        'Образование',
        'Инфляция'
    ],
    '2013': [47629, 24305, 19368, 7.07],
    '2014': [51851, 25498, 22945, 6.05],
    '2015': [56536, 26867, 24342, 14.97],
    '2016': [62498, 27603, 25133, 9.77],
    '2017': [65663, 29872, 26471, 5.02],
    '2018': [73237, 34318, 31141, 2.21],
    '2019': [79484, 37671, 33582, 5.00],
    '2020': [84860, 39934, 36327, 3.51],
    '2021': [90063, 43323, 38730, 5.19],
    '2022': [103380, 49308, 42050, 17.83],
    '2023': [115662, 56191, 47382, 3.51],
    '2024': [130433, 69735, 53974, 7.69],
    '2025': [151764, 84591, 63055, 8.58]
}

df = pd.DataFrame(data)

# Отделяем данные по отраслям
industries = df[df['Экономическая деятельность'].isin([
    'Добыча полезных ископаемых',
    'Строительство',
    'Образование'
])]

# Отделяем данные по инфляции
inflation = df[df['Экономическая деятельность'] == 'Инфляция'].drop(
    'Экономическая деятельность', axis=1
).T
inflation.columns = ['Инфляция']

salaries = industries.drop('Экономическая деятельность', axis=1).T
salaries.columns = industries['Экономическая деятельность']

# Пересчет реальных зарплат с учетом инфляции
real_salaries = salaries.copy()
for year in salaries.index:
    inflation_rate = inflation.loc[year, 'Инфляция'] / 100
    real_salaries.loc[year] = salaries.loc[year] / (1 + inflation_rate)

# Визуализация
plt.figure(figsize=(14, 8))

# График номинальных зарплат
for industry in salaries.columns:
    plt.plot(salaries.index, salaries[industry],
             label=f'{industry} (номинальная)',
             linestyle='--', alpha=0.7)

# График реальных зарплат
for industry in real_salaries.columns:
    plt.plot(real_salaries.index, real_salaries[industry],
             label=f'{industry} (реальная)',
             linewidth=2)

plt.title('Динамика номинальных и реальных зарплат по отраслям (2013-2025)', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Средняя зарплата, руб.', fontsize=12)
plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()

# Сохранение графика
plt.savefig('salary_dynamics.png', dpi=300, bbox_inches='tight')
plt.show()

# Дополнительный анализ: темпы роста
growth = (real_salaries.pct_change() * 100).dropna()

plt.figure(figsize=(14, 6))
growth.plot(kind='bar')
plt.title('Годовые темпы роста реальных зарплат (%)', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Изменение, %', fontsize=12)
plt.legend(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('salary_growth.png', dpi=300, bbox_inches='tight')
plt.show()

# Вывод результатов
print("Средние зарплаты по отраслям (2025 год):")
print(salaries.loc['2025'])

print("\nРеальные зарплаты с учетом инфляции (2025 год):")
print(real_salaries.loc['2025'])

print("\nСреднегодовой рост реальных зарплат:")
print(growth.mean())
