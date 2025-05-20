import pandas as pd

def change_ratio(data,columns_name,columns_name2="null"):
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

    # Prepare required columns
    required_columns = [columns_name, 'Year', 'Number_of_Casualties', 'Vehicle_Type']
    if columns_name2 and columns_name2 != "null":
        required_columns.insert(1, columns_name2)
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    # Replace missing values in relevant columns with default values
    data[columns_name] = data[columns_name].fillna("Unknown")
    data['Number_of_Casualties'] = data['Number_of_Casualties'].fillna(0)

    if(columns_name == "Weather_Conditions"):
        data = data[data['Light_Conditions'].isin(['Daylight'])]
    # Filter for Vehicle_Type == 'Car' or 'Taxi/Privite hire car'
    data = data[data['Vehicle_Type'].isin(['Car', 'Taxi/Privite hire car'])]

    # Group and pivot depending on columns_name2
    if columns_name2 and columns_name2 != "null":
        group_cols = [columns_name, columns_name2, 'Year']
        pivot_index = [columns_name, columns_name2]
    else:
        group_cols = [columns_name, 'Year']
        pivot_index = [columns_name]
    
    grouped_data = data.groupby(group_cols)['Number_of_Casualties'].sum().reset_index()
    pivot_data = grouped_data.pivot_table(index=pivot_index, columns='Year', values='Number_of_Casualties').reset_index()

    # Calculate change ratios for available years
    year_cols = [col for col in pivot_data.columns if isinstance(col, int)]
    for i, year in enumerate(sorted(year_cols)[1:], 1):
        prev_year = sorted(year_cols)[i-1]
        pivot_data[f'Change_Ratio_{year}'] = (pivot_data[year] - pivot_data[prev_year]) / pivot_data[prev_year].replace(0, pd.NA)
    return pivot_data

def calculate_severty_ratio(data,condition):
    """
    This function calculates the ratio of 'Number_of_Casualties' for each 'Accident_Severity' 
    grouped by 'Light Condition'. The result is exported to a table with columns: 
    'Light Condition', 'Fatal', 'Serious', and 'Slight'.

    :param data: pandas DataFrame containing the accident data.
    :return: A DataFrame with the calculated ratios.
    """
    # Ensure required columns exist
    required_columns = ['Accident_Severity', condition, 'Number_of_Casualties']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    # Replace missing values in relevant columns with default values
    data.loc[:,'Accident_Severity'] = data['Accident_Severity'].fillna("Unknown")
    data.loc[:,condition] = data[condition].fillna("Unknown")
    data.loc[:,'Number_of_Casualties'] = data['Number_of_Casualties'].fillna(0)

    if(condition == "Weather_Conditions"):
        data = data[data['Light_Conditions'].isin(['Daylight'])]
        data = data[data['Vehicle_Type'].isin(['Car', 'Taxi/Privite hire car','Light_Conditions'])]
    else:
        data = data[data['Vehicle_Type'].isin(['Car', 'Taxi/Privite hire car'])]
    # Map Accident_Severity to Fatal, Serious, and Slight
    severity_mapping = {
        'Fatal': 'Fatal',
        'Serious': 'Serious',
        'Slight': 'Slight'
    }
    data.loc[:,'Accident_Severity'] = data['Accident_Severity'].map(severity_mapping).fillna("Unknown")

    # Group by 'Accident_Severity' and 'Light Condition', then sum the casualties
    grouped_data = data.groupby(['Accident_Severity', condition])['Number_of_Casualties'].sum().reset_index()

    # Calculate the total casualties for each 'Light Condition'
    total_casualties = grouped_data.groupby(condition)['Number_of_Casualties'].transform('sum')

    # Calculate the ratio of casualties for each severity level
    grouped_data['Ratio'] = grouped_data['Number_of_Casualties'] / total_casualties

    # Pivot the table to have 'Fatal', 'Serious', and 'Slight' as columns
    result = grouped_data.pivot(index=condition, columns='Accident_Severity', values='Ratio').reset_index()

    # Fill missing values with 0 (if any severity level is missing for a light condition)
    result = result.fillna(0)

    # Rename columns for clarity
    result.columns.name = None  # Remove the columns' name
    result = result.rename(columns={condition: condition})

    return result