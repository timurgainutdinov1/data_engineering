import MyModule
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option("display.max_rows", 20, "display.max_columns", 60)

need_dtypes = MyModule.read_types("data/game_logs/dtypes.json")

dataset = MyModule.read_filtered_file('data/game_logs/df.csv', need_dtypes)

# dataset['attendance'].fillna(dataset['attendance'].mean(), inplace=True)
dataset['length_minutes'].fillna(dataset['length_minutes'].mean(), inplace=True)
dataset['v_hits'].fillna(dataset['v_hits'].mean(), inplace=True)

# Распределение посещаемости
plt.figure()
plt.hist(dataset['attendance'], color='blue', edgecolor='black', bins=int(10000/1000))
plt.title('Распределение посещаемости')
plt.xlabel('Посещаемость')
plt.ylabel('Частота')
plt.savefig('graph/game_logs/graph1.png', dpi=300)

# Средняя посещаемость по дням недели
plt.figure()
mean_attendance = dataset.groupby('day_of_week', observed=False)['attendance'].mean()
plt.bar(mean_attendance.index, mean_attendance.values, zorder=2)
plt.grid(True)
plt.title('Средняя посещаемость по дням недели')
plt.xlabel('День недели')
plt.ylabel('Посещаемость')
plt.savefig('graph/game_logs/graph2.png', dpi=300)

# Тепловая карта корреляции числовых колонок
plt.figure()
sns.heatmap(dataset.select_dtypes(include=['int', 'float']).corr(), annot=True,
            vmin=-1, vmax=1, center=0, cmap='coolwarm')
plt.title('Построение тепловой карты корреляции числовых колонок')
plt.savefig('graph/game_logs/graph3.png', dpi=300)

# Соотношение очков v_score и h_score
plt.figure()
score_labels = ['v_score', 'h_score']
score_values = [dataset['v_score'].sum(), dataset['h_score'].sum()]
plt.pie(score_values, labels=score_labels, autopct='%1.1f%%')
plt.title('Соотношение очков v_score и h_score')
plt.savefig('graph/game_logs/graph4.png', dpi=300)

# Cуммарные посещаемости за год
dataset['date'] = pd.to_datetime(dataset['date'], format='%Y%m%d')
dataset['year'] = dataset['date'].dt.year
grouped_df = dataset.groupby('year')['attendance'].sum().reset_index()
plt.figure()
plt.plot(grouped_df['year'], grouped_df['attendance'], zorder=2)
plt.grid(True)
plt.xlabel('Год')
plt.ylabel('Суммарная посещаемость')
plt.title('Cуммарные посещаемости за год')
plt.savefig('graph/game_logs/graph5.png', dpi=300)
