# BA Project

## Project Structure

```
BA
├── src
│   ├── main.py
│   ├── address_finder.py
│   ├── change_ratio_calculation.py
│   └── describe_statistic.py
├── utils
│   ├── file_reader.py
│   └── file_writer.py
├── requirements.txt
└── README.md
```

## Requirements

To run this project, you need to have Python installed along with the required dependencies. You can install the dependencies using the following command:

```
pip install -r requirements.txt
```

### Dependencies
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `geopy`

## Usage

1. Place your CSV file in an accessible directory.
2. Update the `file_path` variable in `src/main.py` with the path to your CSV file.
3. Run the application using one of the following commands based on the desired functionality:

### Available Commands
- **Generate Statistics**:
  ```
  python src/main.py -stc
  ```
  This will generate statistical summaries of the dataset and save them to `statistic_data.csv`.

- **Find Addresses**:
  ```
  python src/main.py -adf
  ```
  This will perform reverse geocoding for latitude and longitude in the dataset and save the results to `address_data.csv`.

- **Calculate Change Ratios**:
  - By District Area:
    ```
    python src/main.py -rdst
    ```
    This will calculate the change ratio by district area and save it to `change_ratio_by_area.csv`.

  - By Light Conditions:
    ```
    python src/main.py -rlght
    ```
    This will calculate the change ratio by light conditions and save it to `change_ratio_by_light.csv`.

  - By Weather Conditions:
    ```
    python src/main.py -rwth
    ```
    This will calculate the change ratio by weather conditions and save it to `change_ratio_by_weather.csv`.

  - By Vehicle Type:
    ```
    python src/main.py -rveh
    ```
    This will calculate the change ratio by vehicle type and save it to `change_ratio_by_vehicle.csv`.

## Debugging

To debug the project in Visual Studio Code, use the pre-configured debugger in `.vscode/launch.json`. Open the file you want to debug and press `F5` to start debugging.

## License
This project is licensed under the MIT License.

