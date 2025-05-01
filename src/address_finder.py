def address_finder(Latitude, Longitude):
    """
    This function takes latitude and longitude as input and returns a formatted address.

    Args:
    Latitude (str): The latitude of the location.
    Longitude (str): The longitude of the location.

    Returns:
    pandas.DataFrame: A DataFrame containing the structured address components, such as house number, road, suburb, city, state, etc.

    Description:
    The function uses the geopy library to perform reverse geocoding, converting geographic coordinates into a human-readable address. 
    It extracts specific address components from the geocoded data and organizes them into a pandas DataFrame for further processing or export.
    """

    import pandas as pd 
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="my_geopy_app", timeout=15)
    location = geolocator.reverse(Latitude+","+Longitude, timeout=15)
    address = location.raw['address']
    address_data = {
        "House_number": [address.get('house_number', 'N/A')],
        "Road": [address.get('road','N/A')],
        "Suburb": [address.get('suburb', 'N/A')],
        "City_district": [address.get('city_district', 'N/A')],
        "City": [address.get('city', 'N/A')],
        "State_district": [address.get('state_district', 'N/A')],
        "State": [address.get('state', 'N/A')]
    }
    return pd.DataFrame(address_data)