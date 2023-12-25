import MyModule
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

need_dtypes = MyModule.read_types("data/vacancies/dtypes.json")

dataset = MyModule.read_filtered_file('data/vacancies/df.csv', need_dtypes)

# Распределение начальной зарплаты
plt.figure()
plt.hist(dataset['salary_from'], color='blue', edgecolor='black', bins=20)
plt.title('Распределение начальной зарплаты')
plt.xlabel('Зарплата')
plt.ylabel('Частота')
plt.savefig('graph/vacancies/graph1.png', dpi=300)

# Соотношение по schedule_id
schedule_id_count = dataset.groupby('schedule_id', observed=False).size()
plt.figure()
plt.pie(schedule_id_count, autopct='%d%%', pctdistance=1.12)
plt.legend(labels=schedule_id_count.index, loc='center right', bbox_to_anchor=(1.35, 0.5))
plt.title('Соотношение по schedule_id')
plt.savefig('graph/vacancies/graph2.png', dpi=300)

# Суммарное число вакансий по schedule_id
s_count = dataset.groupby('schedule_id', observed=False).size()
plt.figure()
plt.bar(s_count.index, s_count.values, zorder=2)
plt.grid(True)
plt.title('Суммарное число вакансий по schedule_id')
plt.xlabel('schedule_id')
plt.ylabel('Число вакансий')
plt.savefig('graph/vacancies/graph3.png', dpi=300)

# Диаграмма рассеяния: area_id и salary_from
plt.figure()
plt.scatter(dataset['area_id'], dataset['salary_from'], alpha=0.5)
plt.xlabel('area_id')
plt.ylabel('salary_from')
plt.title('Диаграмма рассеяния: area_id и salary_from')
plt.savefig('graph/vacancies/graph4.png', dpi=300)
