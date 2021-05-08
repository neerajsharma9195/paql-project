import pandas as pd


def get_group_id(group_binary_arr, least_group_id):
    '''

    :param group_binary_arr: array of size partitoning_attributes having value 0 and 1 based on comparison with representative tuple
    :param least_group_id: initial group id from where new group id can be given
    :return: group id for the tuple
    '''
    ans = 0
    power = 1
    for val in group_binary_arr:
        ans += val * power
        power *= 2
    return ans + least_group_id


def partition(input_dataframe, group_size_threshold, partitioning_attributes, initialize = True):
    '''

    :param input_dataframe: dataframe
    :param group_size_threshold: partition size constraint
    :param partitioning_attributes: attributes need to consider for partitioning. Using these attributes per group can be separated in 2^(size(partitioning_attributes)).
    :param initialize: whether to start partitoning from start or not
    :return: partitioned dataframe
    '''
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


def get_representative_for_group(input_dataframe, partitioning_attributes, representative_type='min'):
    '''

    :param input_dataframe: data
    :param partitioning_attributes: attributes for representative tuples to consider
    :param representative_type: max, min, mean: how to select representative tuple from group
    :return: representative tuples
    '''
    if representative_type == 'mean':
        df_rep = input_dataframe.groupby('gid')[partitioning_attributes].mean().reset_index()
    elif representative_type == 'min':
        df_rep = input_dataframe.groupby('gid')[partitioning_attributes].min().reset_index()
    else:
        df_rep = input_dataframe.groupby('gid')[partitioning_attributes].max().reset_index()
    counts = input_dataframe.groupby('gid').size().reset_index(name='counts')['counts']
    df_rep['counts'] = counts
    return df_rep.reset_index(drop=True)
