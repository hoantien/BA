import pandas as pd

def change_ratio(data,columns_name):
    """
    The `change_ratio` function calculates the year-over-year change ratio of casualties for a specified grouping column 
    (e.g., 'Light Condition', 'District Area', etc.). It processes the data by grouping it by the specified column, 
    'Urban_or_Rural_Area', and 'Year', then calculates the percentage change in casualties for each year.

    :param data: pandas DataFrame containing the accident data.
    :param columns_name: The column name to group by (e.g., 'Light Condition', 'District Area').
    :return: A DataFrame with the calculated change ratios for each group.
    """
    # Ensure the 'Year' column exists by extracting it from the 'Accident Date' column
    if 'Accident Date' in data.columns:
        data['Year'] = pd.to_datetime(data['Accident Date'], format='%d-%m-%Y').dt.year
    else:
        raise ValueError("Missing required column: 'Accident Date'")

    # Ensure required columns exist
    required_columns = [columns_name, 'Urban_or_Rural_Area','Year', 'Number_of_Casualties']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    # Replace missing values in relevant columns with default values
    data[columns_name] = data[columns_name].fillna("Unknown")
    data['Number_of_Casualties'] = data['Number_of_Casualties'].fillna(0)

    # Group by Light Condition and Year, then sum the casualties
    grouped_data = data.groupby([columns_name, 'Urban_or_Rural_Area','Year'])['Number_of_Casualties'].sum().reset_index()

    # Pivot the table to have years as columns
    pivot_data = grouped_data.pivot_table(index=[columns_name,'Urban_or_Rural_Area'], columns='Year', values='Number_of_Casualties').reset_index()

    for i in range(0,3):
        pivot_data['Change_Ratio_'+str(2020+i)] = pivot_data.iloc[:, 2:6].pct_change(axis=1,fill_method=None).iloc[:,i-3]
    return pivot_data

