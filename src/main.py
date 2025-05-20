import sys
import os
import sklearn.cluster as cluster
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tabula import read_pdf
from utils.file_reader import read_csv
from utils.file_writer import write_csv_file
from describe_statistic import describe_statistic
from address_finder import address_finder
from change_ratio_calculation import *

parser = argparse.ArgumentParser()
parser.add_argument("-data", "--data_file_path", help="Path to the input CSV file",action="store")
parser.add_argument("-pdf", "--read_pdf", help="Execute read pdf function",action="store_true")
parser.add_argument("-stc", "--statistic", help="Execute statistic function", action="store_true")
parser.add_argument("-adf", "--address_finder", help="Execute address finder function", action="store_true")
parser.add_argument("-rdst", "--change_ratio_district", help="Execute change_ratio_district function", action="store_true")
parser.add_argument("-rlght", "--change_ratio_light_condition", help="Execute change_ratio_light_condition function", action="store_true")
parser.add_argument("-rlgse", "--change_ratio_light_condition_severity", help="Execute change_ratio_light_condition_severity function", action="store_true")
parser.add_argument("-rwth", "--change_ratio_weather_condition", help="Execute change_ratio_weather_condition function", action="store_true")
parser.add_argument("-rveh", "--change_ratio_vehicle", help="Execute change_ratio_vehicle function", action="store_true")
parser.add_argument("-rrdt", "--change_ratio_road_type", help="Execute change_ratio_road_type function", action="store_true")
parser.add_argument("-rrds", "--change_ratio_road_surface", help="Execute change_ratio_road_surface function", action="store_true")
parser.add_argument("-slr", "--severity_light_ratio", help="Execute severity_light_ratio function", action="store_true")
parser.add_argument("-swr", "--severity_weather_ratio", help="Execute severity_weather_ratio function", action="store_true")

args = parser.parse_args()

def statistic_calculation(data,path):
    data_statistic = describe_statistic(data)
    print(data_statistic)
    write_csv_file(path, data_statistic, append=False)

def address_query(data,path,start_index=0):
    address=[]
    # Latitude & Longitude input
    for i in range(start_index, len(data)-1):
        try:
            Latitude = str(data.iloc[i]['Latitude'])
            Longitude = str(data.iloc[i]['Longitude'])
            address_data = address_finder(Latitude, Longitude)
            address_data['Index']=str(data.iloc[i]['Index'])
            address_data['No']=i
            address.append(address_data)
            print(f"Processed {i+1} out of {len(data)} records.")
            write_csv_file(path, address_data,append=True)
        except ValueError as ve:
            print(f"Skipping record {i}: Invalid coordinates - {ve}")

def extract_table_from_pdf(pdf_path, output_csv_path, page_number=1):
    """
    Extracts a table from a PDF and exports it to a CSV file.

    :param pdf_path: Path to the input PDF file.
    :param output_csv_path: Path to save the extracted table as a CSV file.
    :param page_number: Page number to extract the table from (default: 1).
    """
    try:
        # Read the table from the PDF
        tables = read_pdf(pdf_path, pages=page_number, multiple_tables=False, pandas_options={"header": None})

        if len(tables) > 0:
            # Save the first table to a CSV file
            tables[0].to_csv(output_csv_path, index=False)
            print(f"Table extracted and saved to {output_csv_path}")
        else:
            print("No tables found in the specified PDF page.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if args.data_file_path:
        file_path = args.data_file_path
        print(f"Using provided file path: {file_path}")
    else:
        file_path = "../accident_data.csv"
        print(f"Using default file path: {file_path}")
    try:
        data = read_csv(file_path)

        if args.severity_light_ratio:
            print(data.columns)
            ratio_data= calculate_severty_ratio(data,"Light_Conditions")
            write_csv_file("../severity_light_ratio.csv", ratio_data, append=False)
        
        if args.severity_weather_ratio:
            print(data.columns)
            ratio_data= calculate_severty_ratio(data,"Weather_Conditions")
            write_csv_file("../severity_weather_ratio.csv", ratio_data, append=False)
        
        if args.statistic:
            statistic_calculation(data, "../statistic_data.csv")
        
        if args.address_finder:
            address_query(data, "../address_data.csv",5296)
        
        if args.change_ratio_district:
            pivot_data = change_ratio(data,"District Area")
            write_csv_file("../change_ratio_by_area.csv", pivot_data, append=False)

        if args.change_ratio_light_condition:
            #print(data.columns)
            pivot_data = change_ratio(data,"Light_Conditions")
            print(pivot_data)
            write_csv_file("../change_ratio_by_light.csv", pivot_data, append=False)
        if args.change_ratio_light_condition_severity:
            #print(data.columns)
            pivot_data = change_ratio(data,"Light_Conditions","Accident_Severity")
            print(pivot_data)
            write_csv_file("../change_ratio_by_light_Ser.csv", pivot_data, append=False)

        if args.change_ratio_weather_condition:
            print(data.columns)
            pivot_data = change_ratio(data,"Weather_Conditions")
            write_csv_file("../change_ratio_by_weather.csv", pivot_data, append=False)

        if args.change_ratio_vehicle:
            print(data.columns)
            pivot_data = change_ratio(data,"Vehicle_Type")
            write_csv_file("../change_ratio_by_vehicle.csv", pivot_data, append=False)

        if args.change_ratio_road_type:
            print(data.columns)
            pivot_data = change_ratio(data,"Road_Type")
            write_csv_file("../change_ratio_by_roadtype.csv", pivot_data, append=False)

        if args.change_ratio_road_surface:
            print(data.columns)
            pivot_data = change_ratio(data,"Road_Surface_Conditions")
            write_csv_file("../change_ratio_by_roadsurface.csv", pivot_data, append=False)
        
        if args.read_pdf:
            pdf_path = "../List of English districts by area - Wikipedia.pdf"
            output_csv_path = "../output.csv"
            extract_table_from_pdf(pdf_path, output_csv_path)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()