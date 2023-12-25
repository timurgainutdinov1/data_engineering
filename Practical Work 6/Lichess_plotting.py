import MyModule
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option("display.max_rows", 20, "display.max_columns", 60)

need_dtypes = MyModule.read_types("data/Lichess/dtypes.json")

dataset = MyModule.read_filtered_file('data/Lichess/df.csv', need_dtypes)

dataset['Date'] = pd.to_datetime(dataset['Date'], format='%Y.%m.%d').dt.day

# Распределение количества ходов (Total_moves)
plt.figure()
plt.hist(dataset['Total_moves'], color='blue', edgecolor='black')
plt.title('Распределение количества ходов (Total_moves)')
plt.xlabel('Количество ходов')
plt.ylabel('Частота')
plt.savefig('graph/Lichess/graph1.png', dpi=300)

# Соотношение типов игр (Game_type)
game_types = dataset.groupby('Game_type', observed=False).size()
plt.figure(figsize=(12,8))
plt.pie(game_types, autopct='%.1f%%', pctdistance=1.1, radius=1.1)
plt.legend(labels=game_types.index, loc='center right', bbox_to_anchor=(1.25, 0.5))
plt.title('Соотношение типов игр (Game_type)')
plt.savefig('graph/Lichess/graph2.png', dpi=300)

# Суммарное количество игр в каждый день
games_per_day = dataset.groupby('Date', observed=False).size()
plt.figure(figsize=(9, 4.8))
plt.bar(games_per_day.index, games_per_day.values, zorder=2)
plt.grid(True)
plt.title('Суммарное количество игр в каждый день')
plt.xlabel('День')
plt.xticks(games_per_day.index)
plt.ylabel('Число игр')
plt.savefig('graph/Lichess/graph3.png', dpi=300)

# Диаграмма рассеяния: общее число ходов и количество раз изменения баланса в игре
# для первого дня и партий с числом ходов больше 200
dataset_first_day = dataset[(dataset['Date'] == 1) & (dataset['Total_moves'] > 200)]
plt.figure()
plt.scatter(dataset_first_day['Game_flips'], dataset_first_day['Total_moves'], alpha=0.5)
plt.xlabel('Количество раз изменения баланса в игре')
plt.ylabel('Общее число ходов')
plt.title('Диаграмма рассеяния: общее число ходов\n'
          'и количество раз изменения баланса в игре\n'
          'для первого дня и партий с числом ходов больше 200',
          fontsize=10)
plt.savefig('graph/Lichess/graph4.png', dpi=300)

# Количество ничьих в каждый день
draw_result_per_day = (dataset.loc[dataset['Result'] == '1/2-1/2']
                       .groupby('Date', observed=False)['Result']
                       .count().reset_index())
plt.figure()
plt.plot(draw_result_per_day['Date'], draw_result_per_day['Result'], zorder=2)
plt.grid(True)
plt.xlabel('День')
plt.ylabel('Количество ничьих')
plt.title('Количество ничьих в каждый день')
plt.savefig('graph/Lichess/graph5.png', dpi=300)
