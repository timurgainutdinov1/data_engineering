import MyModule
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option("display.max_rows", 20, "display.max_columns", 60)

need_dtypes = MyModule.read_types("data/asteroid/dtypes.json")

dataset = MyModule.read_filtered_file('data/asteroid/df.csv', need_dtypes)

# Соотношение по классам
flights_counts_AL = dataset.groupby('class', observed=False).size()
plt.figure(figsize=(8, 4.8))
plt.pie(flights_counts_AL, autopct='%d%%', pctdistance=1.2, radius=1.2)
plt.legend(labels=flights_counts_AL.index, loc='center right', bbox_to_anchor=(1.5, 0.5))
plt.title('Соотношение по классам')
plt.savefig('graph/asteroid/graph1.png', dpi=300)

# Тепловая карта корреляции числовых колонок
plt.figure(figsize=(10, 6))
sns.heatmap(dataset.select_dtypes(include=['int', 'float']).corr(), annot=True,
            vmin=-1, vmax=1, center=0, cmap='coolwarm')
plt.title('Тепловая карта корреляции числовых колонок')
plt.savefig('graph/asteroid/graph2.png', dpi=300)

# Распределение diameter
plt.figure()
plt.hist(dataset['diameter'], color='blue', edgecolor='black', bins=100)
plt.title('Распределение diameter')
plt.xlabel('diameter')
plt.ylabel('Частота')
plt.savefig('graph/asteroid/graph3.png', dpi=300)

# Количество астероидов по классам
class_count = dataset.groupby('class', observed=False).size()
plt.figure()
plt.bar(class_count.index, class_count.values, zorder=2)
plt.grid(True)
plt.title('Количество астероидов по классам')
plt.xlabel('Классы')
plt.ylabel('Количество астероидов')
plt.savefig('graph/asteroid/graph4.png', dpi=300)

# Диаграмма рассеяния: diameter и rms для класса ATE
plt.figure()
filtered_dataset = dataset.loc[dataset['class'] == 'ATE']
plt.scatter(filtered_dataset['diameter'],
            filtered_dataset['rms'], alpha=0.5)
plt.xlabel('diameter')
plt.ylabel('rms')
plt.title('Диаграмма рассеяния: diameter и rms для класса ATE')
plt.savefig('graph/asteroid/graph5.png', dpi=300)

