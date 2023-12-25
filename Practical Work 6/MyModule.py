import json
import pandas as pd
import os
import numpy as np


def read_file(file_name, zip=False, gz=False, chunksize=None):
    if zip:
        return pd.read_csv(file_name, compression='zip', chunksize=chunksize)
    elif gz:
        return pd.read_csv(file_name, compression='gzip', chunksize=chunksize)
    else:
        return pd.read_csv(file_name)
    # df = pd.read_csv(datasets[year], chunksize=chunksize, compression='gzip'])


def get_memory_stat_by_column(df, explored_file_name, new_df=True, file_name=""):
    file_info = dict()
    if new_df:
        file_size = os.path.getsize(file_name)
        file_info["file_size_kb"] = int(file_size // 1024)
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    file_info["file_in_memory_size_kb"] = int(total_memory_usage // 1024)
    column_stat = list()
    for key in df.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs_kb": int(memory_usage_stat[key] // 1024),
            "memory_per": float(round(memory_usage_stat[key] / total_memory_usage * 100, 4)),
            "dtype": str(df.dtypes[key])
        })
    column_stat.sort(key=lambda x: x['memory_abs_kb'], reverse=True)
    data = list()
    data.append({"file_info": file_info})
    data.append({"column_stat": column_stat})
    if new_df:
        with open(f"data/{explored_file_name}/file_info.json", 'w', encoding='utf-8') as f:
            json.dump({"file_data_without_optimization": data}, f)
    else:
        with open(f"data/{explored_file_name}/file_info.json", 'r', encoding='utf-8') as f:
            info = list()
            info.append(json.load(f))
            info.append({"file_data_with_optimization": data})
        with open(f"data/{explored_file_name}/file_info.json", 'w', encoding='utf-8') as f:
            json.dump(info, f)

    return df


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2
    return "{:03.2f}".format(usage_mb)


def opt_obj(df, explored_file_name):
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if (num_unique_values / num_total_values) < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    data = list()
    data.append({"dataset_obj_size_mb": float(mem_usage(dataset_obj))})
    data.append({"converted_obj_size_mb": float(mem_usage(converted_obj))})

    compare_objs = pd.concat([dataset_obj.dtypes, converted_obj.dtypes], axis=1)
    compare_objs.columns = ['before', 'after']
    compare_objs_stats = list()
    for index, row in compare_objs.iterrows():
        compare_objs_stats.append({
            "column_name": index,
            "before": str(row['before']),
            "after": str(row['after'])
        })
    data.append({"optimization_results": compare_objs_stats})
    with open(f"data/{explored_file_name}/objs_optimization.json", 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return converted_obj


def opt_int(df, explored_file_name):
    dataset_int = df.select_dtypes(include=['int'])
    """
    downcast:
            - 'integer' or 'signed': smallest signed int dtype (min.: np.int8) 
            - 'unsigned': smallest unsigned int dtype (min.: np.uint8) 
            - 'float': smallest float dtype (min.: np.float32)
    """
    converted_int = dataset_int.apply(pd.to_numeric, downcast='unsigned')

    if explored_file_name == 'flights':
        converted_int['DATE'] = pd.to_numeric(converted_int.apply(lambda row:
                                              row['YEAR'].astype(str) + "{:02d}".format(row['MONTH']) + "{:02d}".format(row['DAY']),
                                              axis=1), downcast='unsigned')
        converted_int.drop(['YEAR', 'MONTH', 'DAY'], axis=1, inplace=True)
        converted_int['DAY_OF_WEEK'] = converted_int['DAY_OF_WEEK'].astype('category')
        converted_int['DIVERTED'] = converted_int['DIVERTED'].astype('category')
        converted_int['CANCELLED'] = converted_int['CANCELLED'].astype('category')

    data = list()
    data.append({"dataset_int_size_mb": float(mem_usage(dataset_int))})
    data.append({"converted_int_size_mb": float(mem_usage(converted_int))})

    if explored_file_name == 'flights':
        dataset_int["DATE"] = pd.Series().astype('int64')
        dataset_int.drop(['YEAR', 'MONTH', 'DAY'], axis=1, inplace=True)

    compare_ints = pd.concat([dataset_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ['before', 'after']
    compare_ints_stats = list()
    for index, row in compare_ints.iterrows():
        compare_ints_stats.append({
            "column_name": index,
            "before": str(row['before']),
            "after": str(row['after'])
        })
    data.append({"optimization_results": compare_ints_stats})
    with open(f"data/{explored_file_name}/ints_optimization.json", 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return converted_int


def opt_float(df, explored_file_name):
    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')

    data = list()
    data.append({"dataset_floats_size_mb": float(mem_usage(dataset_float))})
    data.append({"converted_floats_size_mb": float(mem_usage(converted_float))})

    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats_stats = list()
    for index, row in compare_floats.iterrows():
        compare_floats_stats.append({
            "column_name": index,
            "before": str(row['before']),
            "after": str(row['after'])
        })
    data.append({"optimization_results": compare_floats_stats})
    with open(f"data/{explored_file_name}/floats_optimization.json", 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return converted_float


def optimize_dataset(df, explored_file_name):
    optimized_dataset = df.copy()

    converted_obj = opt_obj(df, explored_file_name)
    converted_int = opt_int(df, explored_file_name)
    converted_float = opt_float(df, explored_file_name)

    optimized_dataset[converted_obj.columns] = converted_obj
    optimized_dataset[converted_int.columns] = converted_int
    optimized_dataset[converted_float.columns] = converted_float

    return optimized_dataset


def read_types(file_name):
    with open(file_name, "r") as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype
        else:
            dtypes[key] = np.dtype(dtypes[key])

    return dtypes


def read_filtered_file(file_name, need_dtypes):
    return pd.read_csv(file_name,
                       usecols=lambda x: x in need_dtypes.keys(),
                       dtype=need_dtypes)
