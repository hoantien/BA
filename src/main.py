import sys
import os
import sklearn.cluster as cluster
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.file_reader import read_csv
from describe_statistic import describe_statistic

def main():
    file_path = "../accident_data.csv"
    try:
        data = read_csv(file_path)
        data_statistic = describe_statistic(data)
        print(data_statistic)
        geolocator = Nominatim(user_agent="my_geopy_app")
        # Latitude & Longitude input
        Latitude = "51.495029"
        Longitude = "-0.202731"

        location = geolocator.reverse(Latitude+","+Longitude)
        address = location.raw['address']
        #print(address)
        address_data = {
            "House_number": [address['house_number']],
            "Road": [address['road']],
            "Suburb": [address['suburb']],
            "City_district": [address['city_district']],
            "City": [address['city']],
            "State_district": [address['state_district']],
            "State": [address['state']],
        }
        address_df = pd.DataFrame(address_data)
        address_df.to_csv("../address_data.csv", index=False)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()