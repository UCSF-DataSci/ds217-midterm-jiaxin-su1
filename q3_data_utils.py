#!/usr/bin/env python3
# TODO: Add shebang line: #!/usr/bin/env python3

# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.

    Args:
        filepath: Path to CSV file

    Returns:
        pd.DataFrame: Loaded data

    Example:
        >>> df = load_data('data/clinical_trial_raw.csv')
        >>> df.shape
        (10000, 18)
    """
    return(pd.read_csv(filepath))


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.

    Args:
        df: Input DataFrame
        remove_duplicates: Whether to drop duplicate rows
        sentinel_value: Value to replace with NaN (e.g., -999, -1)

    Returns:
        pd.DataFrame: Cleaned data

    Example:
        >>> df_clean = clean_data(df, sentinel_value=-999)
    """
    df_clean = df.copy()
    if remove_duplicates:
        df_clean .drop_duplicates(inplace=True)    
    df_clean.replace(sentinel_value, np.nan,inplace=True)
    return df_clean


def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.

    Args:
        df: Input DataFrame

    Returns:
        pd.Series: Count of missing values for each column

    Example:
        >>> missing = detect_missing(df)
        >>> missing['age']
        15
    """
    return df.isnull().sum()
    

def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.

    Args:
        df: Input DataFrame
        column: Column name to fill
        strategy: Fill strategy - 'mean', 'median', or 'ffill'

    Returns:
        pd.DataFrame: DataFrame with filled values

    Example:
        >>> df_filled = fill_missing(df, 'age', strategy='median')
    """
    df_copy = df.copy() # make a copy to avoid modifying original DataFrame
    if strategy == 'mean':
        fill_value = df_copy[column].mean()
    elif strategy == 'median':
        fill_value = df_copy[column].median()
    elif strategy == 'ffill':
        df_copy[column] = df_copy[column].fillna(method='ffill')
        return df_copy
    df_copy[column] = df_copy[column].fillna(fill_value)
    return df_copy


def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.

    Args:
        df: Input DataFrame
        filters: List of filter dictionaries, each with keys:
                'column', 'condition', 'value'
                Conditions: 'equals', 'greater_than', 'less_than', 'in_range', 'in_list'

    Returns:
        pd.DataFrame: Filtered data

    Examples:
        >>> # Single filter
        >>> filters = [{'column': 'site', 'condition': 'equals', 'value': 'Site A'}]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Multiple filters applied in order
        >>> filters = [
        ...     {'column': 'age', 'condition': 'greater_than', 'value': 18},
        ...     {'column': 'age', 'condition': 'less_than', 'value': 65},
        ...     {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
        ... ]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Range filter example
        >>> filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 65]}]
        >>> df_filtered = filter_data(df, filters)
    """
    
    df_filtered = df.copy()
    for f in filters:
        col = f['column']
        cond = f['condition']
        val = f['value']

        if cond == 'equals':
            df_filtered = df_filtered[df_filtered[col] == val]
        elif cond == 'greater_than':
            df_filtered = df_filtered[df_filtered[col] > val]
        elif cond == 'less_than':
            df_filtered = df_filtered[df_filtered[col] < val]
        elif cond == 'in_range':
            df_filtered = df_filtered[(df_filtered[col] >= val[0]) & (df_filtered[col] <= val[1])]
        elif cond == 'in_list':
            df_filtered = df_filtered[df_filtered[col].isin(val)]

    return df_filtered

    


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.

    Args:
        df: Input DataFrame
        type_map: Dict mapping column names to target types
                  Supported types: 'datetime', 'numeric', 'category', 'string'

    Returns:
        pd.DataFrame: DataFrame with converted types

    Example:
        >>> type_map = {
        ...     'enrollment_date': 'datetime',
        ...     'age': 'numeric',
        ...     'site': 'category'
        ... }
        >>> df_typed = transform_types(df, type_map)
    """
    df_types = df.copy()
    for col, co_type in type_map.items():
        if co_type == 'datetime':
            df_types[col] = pd.to_datetime(df_types[col], errors='coerce')
        elif co_type == 'numeric':
            df_types[col] = pd.to_numeric(df_types[col], errors='coerce')
        elif co_type == 'category':
            df_types[col] = df_types[col].astype('category')
        elif co_type == 'string':
            df_types[col] = df_types[col].astype('string')

    return df_types


def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().

    Args:
        df: Input DataFrame
        column: Column to bin
        bins: List of bin edges
        labels: List of bin labels
        new_column: Name for new binned column (default: '{column}_binned')

    Returns:
        pd.DataFrame: DataFrame with new binned column

    Example:
        >>> df_binned = create_bins(
        ...     df,
        ...     column='age',
        ...     bins=[0, 18, 35, 50, 65, 100],
        ...     labels=['<18', '18-34', '35-49', '50-64', '65+']
        ... )
    """
    df_binned = df.copy()
    if new_column is None:
        new_column = f"{column}_binned"
        df_binned[new_column] = pd.cut(df_binned[column], bins=bins, labels=labels)
    else:
        df_binned[new_column] = pd.cut(df_binned[column], bins=bins, labels=labels)
    return df_binned



def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.

    Args:
        df: Input DataFrame
        group_col: Column to group by
        agg_dict: Dict of {column: aggregation_function(s)}
                  If None, uses .describe() on numeric columns

    Returns:
        pd.DataFrame: Grouped and aggregated data

    Examples:
        >>> # Simple summary
        >>> summary = summarize_by_group(df, 'site')
        >>>
        >>> # Custom aggregations
        >>> summary = summarize_by_group(
        ...     df,
        ...     'site',
        ...     {'age': ['mean', 'std'], 'bmi': 'mean'}
        ... )
    """
    
    df_summary = df.copy()
    if agg_dict is None: 
        num_cols = df_summary.select_dtypes(include="number").columns # get numeric columns and its index
        return df_summary.groupby(group_col)[num_cols].describe()
    return df_summary.groupby(group_col).agg(agg_dict) # if agg_dict is provided
    # agg() can take a dict mapping columns to agg functions
 



if __name__ == '__main__':
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")   
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")
    
    # TODO: Add simple test example here
    # Example:
    # test_df = pd.DataFrame({'age': [25, 30, 35], 'bmi': [22, 25, 28]})
    # print("Test DataFrame created:", test_df.shape)
    # print("Test detect_missing:", detect_missing(test_df))



    data = {
    "id": ["p001", "p002", "p002", "p003", "p004", "p005", "p005"],
    "age": [25, 17, 35, -999, 68, 29,29],
    "site": ["Site C", "Site B", "Site A", "Site C", "Site B", "Site A","Site A"],
    "diastolic_bp": [88, 75, 92, 65, 70, 95,95]
}

    df = pd.DataFrame(data)
    print(df)
    df_clean = clean_data(df, sentinel_value=-999)
    print(df_clean)
    missing = detect_missing(df_clean)
    print("Missing values:\n", missing)
    df_filled = fill_missing(df_clean, 'age', strategy='median')
    print(df_filled)
    # filter example
    filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 65]}]
    df_filtered = filter_data(df_filled, filters)
    print(df_filtered)
    #  type transformation example
    type_map = {
        'id': 'string',
        'age': 'numeric',
        'site': 'category'
    }
    df_typed = transform_types(df_filled, type_map)

    # binning example
    df_binned = create_bins(
        df_filled,
        column='age',
        bins=[0, 18, 35, 50, 65, 100],
        labels=['<18', '18-34', '35-49', '50-64', '65+'])
    print(df_binned['age'])
    # grouping and summarization example
    df_summarized = summarize_by_group(df_filled, "site", {'age': ['mean', 'std'], 'diastolic_bp': 'mean'})
    print(df_summarized)