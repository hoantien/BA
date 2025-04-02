import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from utils.file_reader import read_csv

def main():
    file_path = input("Enter the path to the CSV file: ")
    try:
        data = read_csv(file_path)
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()