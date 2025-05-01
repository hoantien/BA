def write_csv_file(file_path, data, append=False):
    """
    Write data to a CSV file.

    :param file_path: Path to the CSV file.
    :param data: pandas DataFrame containing the data to write.
    :param append: If True, append to the file; otherwise, overwrite it.
    """
    import pandas as pd
    import os

    mode = 'a' if append else 'w'
    header = not append or not os.path.exists(file_path)  # Write header only if not appending or file doesn't exist

    data.to_csv(file_path, mode=mode, header=header, index=False)