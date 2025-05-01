import sys
import os
import time
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

parser = argparse.ArgumentParser()
parser.add_argument("-stc", "--statistic", help="Execute statistic function", action="store_true")
parser.add_argument("-adf", "--address_finder", help="Execute address finder function", action="store_true")


args = parser.parse_args()

def statistic_calculation(data,path):
    data_statistic = describe_statistic(data)
    print(data_statistic)
    write_csv_file(path, data_statistic, append=False)

def address_query(data,path):
    address=[]
    # Latitude & Longitude input
    for i in range(5296, len(data)-1):
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
            write_csv_file("../address_data.csv", address_data,append=True)
        except ValueError as ve:
            print(f"Skipping record {i}: Invalid coordinates - {ve}")


def main():
    file_path = "../accident_data.csv"
    try:
        data = read_csv(file_path)
        if args.statistic:
            statistic_calculation(data, "../statistic_data.csv")
        
        if args.address_finder:
            address_query(data, "../address_data.csv")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()