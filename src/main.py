import sys
import os
import sklearn.cluster as cluster
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.file_reader import read_csv
from utils.file_writer import write_csv_file
from describe_statistic import describe_statistic
from address_finder import address_finder
from change_ratio_calculation import *

parser = argparse.ArgumentParser()
parser.add_argument("-stc", "--statistic", help="Execute statistic function", action="store_true")
parser.add_argument("-adf", "--address_finder", help="Execute address finder function", action="store_true")
parser.add_argument("-rdst", "--change_ratio_district", help="Execute change_ratio_district function", action="store_true")
parser.add_argument("-rlght", "--change_ratio_light_condition", help="Execute change_ratio_light_condition function", action="store_true")
parser.add_argument("-rwth", "--change_ratio_weather_condition", help="Execute change_ratio_weather_condition function", action="store_true")
parser.add_argument("-rveh", "--change_ratio_vehicle", help="Execute change_ratio_vehicle function", action="store_true")

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
            #address_data_df = pd.concat(address, ignore_index=True)
            #print(address_data_df)
            write_csv_file(path, address_data,append=True)
        except ValueError as ve:
            print(f"Skipping record {i}: Invalid coordinates - {ve}")

def main():
    file_path = "../accident_data.csv"
    try:
        data = read_csv(file_path)
        if args.statistic:
            statistic_calculation(data, "../statistic_data.csv")
        
        if args.address_finder:
            address_query(data, "../address_data.csv",5296)
        
        if args.change_ratio_district:
            pivot_data = change_ratio(data,"District Area")
            write_csv_file("../change_ratio_by_area.csv", pivot_data, append=False)

        if args.change_ratio_light_condition:
            print(data.columns)
            pivot_data = change_ratio(data,"Light_Conditions")
            write_csv_file("../change_ratio_by_light.csv", pivot_data, append=False)

        if args.change_ratio_weather_condition:
            print(data.columns)
            pivot_data = change_ratio(data,"Weather_Conditions")
            write_csv_file("../change_ratio_by_weather.csv", pivot_data, append=False)

        if args.change_ratio_vehicle:
            print(data.columns)
            pivot_data = change_ratio(data,"Vehicle_Type")
            write_csv_file("../change_ratio_by_vehicle.csv", pivot_data, append=False)
            

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()