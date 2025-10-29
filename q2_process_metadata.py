#!/usr/bin/env python3
# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.
import numpy as np

def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    # TODO: Read file, split on '=', create dict
    
    with open(filepath, "r") as f:
        lines = f.readlines()
        dict = {}
        for line in lines:
            dict[line.split("=")[0]] = line.split("=")[1].strip()
        return (dict)

def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    # TODO: Implement with if/elif/else
    # return false if not interger
    result = {}
    for key in config:
        if type(int(config[key]))is int:
            if key == 'sample_data_rows' and int(config[key]) > 0:
                result[key] = True
            elif key == 'sample_data_min' and int(config[key]) >= 1:
                result[key] = True  
            elif key == 'sample_data_max' and int(config[key]) > int(config['sample_data_min']):
                result[key] = True
            else:
                result[key] = False
    return result


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    import random
    # TODO: Parse config values (convert strings to int)
    rows = int(config['sample_data_rows'])
    min_val = int(config['sample_data_min'])
    max_val = int(config['sample_data_max'])
    # TODO: Generate random numbers and save to file
    # only one number per row in the csv file and nothing else
    # store the numbers here 
    with open(filename, "w") as f:
        for i in range(rows):
            f.write(str(random.randint(min_val, max_val)) + "\n")
    # TODO: Use random module with config-specified range
    random.randint(min_val, max_val)


def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    # TODO: Calculate stats
    mean = np.mean(data)
    median = np.median(data)
    sum_val = np.sum(data)
    count = len(data)
    return {'mean': round(mean, 2), 'median':round(median, 2) , 'sum': sum_val, 'count':count}


if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 

    config = parse_config('q2_config.txt')
    validation = validate_config(config)
    generate_sample_data('data/sample_data.csv', config)

    # TODO: Read the generated file and calculate statistics
    with open('data/sample_data.csv', 'r') as f:
        data = f.readlines()
        data_list = [int(num.strip()) for num in data]

    # TODO: Save statistics to output/statistics.txt
    with open("output/statistics.txt", "w") as f:
        for key, value in calculate_statistics(data_list).items():
            f.write(f"{key}: {value}\n") # write() argument must be str, not dict


