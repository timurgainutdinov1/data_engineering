import MyModule
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option("display.max_rows", 20, "display.max_columns", 60)

need_dtypes = MyModule.read_types("data/flights/dtypes.json")

dataset = MyModule.read_filtered_file('data/flights/df.csv', need_dtypes)

# Соотношение рейсов по каждой авиакомпании
flights_counts_AL = dataset.groupby('AIRLINE', observed=False).size()
plt.figure()
plt.pie(flights_counts_AL, autopct='%d%%', pctdistance=1.12)
plt.legend(labels=flights_counts_AL.index, loc='center right', bbox_to_anchor=(1.25, 0.5))
plt.title('Соотношение рейсов по авиакомпаниям')
plt.savefig('graph/flights/graph1.png', dpi=300)

# Диаграмма рассеяния для колонок 'AIR_TIME' и 'DISTANCE'
dataset['DATE'] = pd.to_datetime(dataset['DATE'], format='%Y%m%d')
dataset_2015_jan = dataset[dataset['DATE'].dt.month == 1]
dataset_2015_jan_first = dataset_2015_jan[dataset_2015_jan['DATE'].dt.day == 1]
plt.figure()
plt.scatter(dataset_2015_jan_first['AIR_TIME'], dataset_2015_jan_first['DISTANCE'], alpha=0.5)
plt.title('Диаграмма рассеяния для колонок "AIR_TIME" и "DISTANCE"')
plt.xlabel('AIR_TIME')
plt.ylabel('DISTANCE')
plt.savefig('graph/flights/graph2.png', dpi=300)

# Суммарное число полетов в каждый день недели
flights_counts_DOW = dataset.groupby('DAY_OF_WEEK', observed=False).size()
plt.figure()
plt.bar(flights_counts_DOW.index, flights_counts_DOW.values, zorder=2)
plt.grid(True)
plt.title('Суммарное число полетов в каждый день недели')
plt.xlabel('День недели')
plt.ylabel('Число полетов')
plt.savefig('graph/flights/graph3.png', dpi=300)

# Зависимость суммарного числа полетов за день от времени (дней) за январь 2015
flights_per_day = dataset_2015_jan.groupby('DATE', observed=False).size()
plt.figure(figsize=(15, 5))
plt.plot(flights_per_day.index, flights_per_day.values, zorder=2)
plt.scatter(flights_per_day.index, flights_per_day.values, zorder=3)
plt.grid(True)
plt.xlabel('День')
plt.ylabel('Число полетов за день')
plt.title('Зависимость суммарного числа полетов за день от времени (дней) за январь 2015')
plt.savefig('graph/flights/graph4.png', dpi=300)

# Распределение времени полета
plt.figure()
plt.hist(dataset['AIR_TIME'], color='blue', edgecolor='black')
plt.title('Распределение времени полета')
plt.xlabel('Время полета')
plt.ylabel('Частота')
plt.savefig('graph/flights/graph5.png', dpi=300)