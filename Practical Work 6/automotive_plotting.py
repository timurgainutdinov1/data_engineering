import MyModule
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

need_dtypes = MyModule.read_types("data/automotive/dtypes.json")

dataset = MyModule.read_filtered_file('data/automotive/df.csv', need_dtypes)

cars_to_remove = dataset.loc[(dataset['askPrice'] == 0) |
                             (dataset['askPrice'] > 100000)].index
dataset.drop(cars_to_remove, inplace=True)

# Распределение цены (askPrice)
plt.figure()
plt.hist(dataset['askPrice'], color='blue', edgecolor='black')
plt.title('Распределение цены (askPrice)')
plt.xlabel('Цена')
plt.ylabel('Частота')
plt.savefig('graph/automotive/graph1.png', dpi=300)

# Средняя цена по маркам машин
plt.figure(figsize=(12, 9))
mean_attendance = (dataset
                   .groupby('brandName', observed=False)['askPrice']
                   .mean())
plt.bar(mean_attendance.index, mean_attendance.values, zorder=2)
plt.grid(True)
plt.title('Средняя цена по маркам машин')
plt.xlabel('Марка')
plt.xticks(rotation=90)
plt.ylabel('Цена')
plt.savefig('graph/automotive/graph2.png', dpi=300)

# Диаграмма рассеяния: год и цена автомобиля
plt.figure()
plt.scatter(dataset['vf_ModelYear'],
            dataset['askPrice'], alpha=0.5)
plt.xlabel('Год')
plt.ylabel('Цена')
plt.title('Диаграмма рассеяния: год и цена автомобиля')
plt.savefig('graph/automotive/graph3.png', dpi=300)

# Средняя цена по годам
grouped_df = dataset.groupby('vf_ModelYear')['askPrice'].mean().reset_index()
plt.figure()
plt.plot(grouped_df['vf_ModelYear'], grouped_df['askPrice'], zorder=2)
plt.grid(True)
plt.title('Средняя цена по годам')
plt.xlabel('Год')
plt.ylabel('Цена')
plt.savefig('graph/automotive/graph4.png', dpi=300)

# Соотношение старых и новых автомобилей
counts = dataset['isNew'].value_counts().tolist()
labels = ['Cтарые', 'Новые']
plt.figure()
plt.pie(counts, labels=labels, autopct='%d%%')
plt.title('Соотношение старых и новых автомобилей')
plt.savefig('graph/automotive/graph5.png', dpi=300)
