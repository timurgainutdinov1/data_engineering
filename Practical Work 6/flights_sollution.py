import MyModule
import pandas as pd
import json
import numpy as np

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

file_name = 'data/[3]flights.csv'

dataset = MyModule.read_file(file_name)
print(dataset.info())

MyModule.get_memory_stat_by_column(dataset, "flights", file_name=file_name)

optimized_dataset = MyModule.optimize_dataset(dataset, "flights")
optimized_dataset.drop(['YEAR', 'MONTH', 'DAY'], axis=1, inplace=True)

MyModule.get_memory_stat_by_column(optimized_dataset, "flights", new_df=False)

need_column = dict()
column_names = ['DATE', 'DAY_OF_WEEK', 'AIRLINE',
                'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'AIR_TIME',
                'TAIL_NUMBER', 'FLIGHT_NUMBER', 'DISTANCE', 'CANCELLED']
opt_dtypes = optimized_dataset.dtypes
for key in column_names:
    need_column[key] = opt_dtypes[key]
    print(f"{key}: {opt_dtypes[key]}")

with open("data/flights/dtypes.json", 'w') as file:
    dtype_json = need_column.copy()
    for key in dtype_json.keys():
        dtype_json[key] = str(dtype_json[key])

    json.dump(dtype_json, file)

has_header = True
chunks_info = list()
i = 1
for chunk in pd.read_csv(file_name,
                         usecols=(lambda x: x in (column_names + ['YEAR', 'MONTH', 'DAY'])),
                         dtype=need_column.update({'YEAR': np.uint16, 'MONTH': np.uint8, 'DAY': np.uint8}),
                         chunksize=100_000):
    chunk['DATE'] = pd.to_numeric(chunk.apply(lambda row:
                                              str(row['YEAR']) +
                                              "{:02d}".format(row['MONTH']) +
                                              "{:02d}".format(row['DAY']),
                                              axis=1), downcast='unsigned')
    chunk.drop(['YEAR', 'MONTH', 'DAY'], axis=1, inplace=True)
    chunks_info.append(
        {
            'chunk_number': i,
            'chunk_size_mb': MyModule.mem_usage(chunk)
        }
    )
    chunk.to_csv("data/flights/df.csv", mode='a', header=has_header)
    has_header = False
    i += 1

with open("data/flights/chunks_info.json", 'w', encoding='utf-8') as f:
    json.dump(chunks_info, f, default=lambda x: x.tolist())
