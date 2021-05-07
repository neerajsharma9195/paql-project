import pandas as pd


def get_group_id(group_binary_arr, least_group_id):
    ans = 0
    power = 1
    for val in group_binary_arr:
        ans += val * power
        power *= 2
    return ans + least_group_id


def partition(input_dataframe, group_size_threshold, partitioning_attributes, initialize = True):
    if initialize is True:
        input_dataframe['gid'] = 1
        least_group_id = 0
    else:
        least_group_id = input_dataframe['gid'].max() + 1
    count = 0
    while True:
        for group_id, group_rows in input_dataframe.groupby('gid'):
            if len(group_rows) > group_size_threshold:
                mean_values = group_rows[partitioning_attributes].mean()
                for index, row in group_rows.iterrows():
                    new_group_id = get_group_id(
                        list((row[partitioning_attributes] < mean_values[partitioning_attributes]).astype(int)),
                        least_group_id)
                    input_dataframe.at[index, 'gid'] = new_group_id
                    # input_dataframe.set_value(index, 'gid', new_group_id)
                    least_group_id += 2 ** len(partitioning_attributes)
        group_sizes = [len(group_rows) for group_id, group_rows in input_dataframe.groupby('gid')]
        if all(group_size <= group_size_threshold for group_size in group_sizes):
            break
        print("all group sizes  after iteration {} is {}".format(count, group_sizes))
        count += 1
    return input_dataframe


def get_representative_for_group(input_dataframe, partitioning_attributes):
    # mean = input_dataframe.groupby('gid')[partitioning_attributes].mean().reset_index()
    min = input_dataframe.groupby('gid')[partitioning_attributes].min().reset_index()
    # max = input_dataframe.groupby('gid')[partitioning_attributes].max().reset_index()
    # df_rep = pd.concat([mean, min, max])
    df_rep = min
    counts = input_dataframe.groupby('gid').size().reset_index(name='counts')['counts']
    df_rep['counts'] = counts
    return df_rep.reset_index(drop=True)
