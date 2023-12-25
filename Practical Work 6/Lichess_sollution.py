import MyModule
import pandas as pd
import json

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

file_name = 'data/Lichess.zip'

dataset = MyModule.read_file(file_name, zip=True)

MyModule.get_memory_stat_by_column(dataset, 'Lichess', file_name=file_name)

optimized_dataset = MyModule.optimize_dataset(dataset, 'Lichess')

MyModule.get_memory_stat_by_column(optimized_dataset, 'Lichess', new_df=False)

need_column = dict()
column_names = ['Date', 'Event', 'Opening',
                'Result', 'Game_type', 'Black_mistakes',
                'White_mistakes', 'Total_moves', 'Game_flips', 'Termination']
opt_dtypes = optimized_dataset.dtypes
for key in column_names:
    need_column[key] = opt_dtypes[key]
    print(f"{key}: {opt_dtypes[key]}")

with open("data/Lichess/dtypes.json", 'w') as file:
    dtype_json = need_column.copy()
    for key in dtype_json.keys():
        dtype_json[key] = str(dtype_json[key])

    json.dump(dtype_json, file)

has_header = True
chunks_info = list()
i = 1
for chunk in pd.read_csv(file_name,
                         usecols=lambda x: x in column_names,
                         dtype=need_column,
                         chunksize=100_000):
    chunks_info.append(
        {
            'chunk_number': i,
            'chunk_size_mb': MyModule.mem_usage(chunk)
        }
    )
    chunk.to_csv("data/Lichess/df.csv", mode='a', header=has_header)
    has_header = False
    i += 1

with open("data/Lichess/chunks_info.json", 'w', encoding='utf-8') as f:
    json.dump(chunks_info, f, default=lambda x: x.tolist())
