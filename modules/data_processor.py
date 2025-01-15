import pandas as pd

def clean_data(data: pd.DataFrame):
    """Clean and preprocess data."""
    data['SkyBOSS'] = data['SkyBOSS'].replace('Hết chỗ', None)
    data['Deluxe'] = data['Deluxe'].replace('Hết chỗ', None)
    data['Eco'] = data['Eco'].replace('Hết chỗ', None)
    return data


def save_to_csv(data: pd.DataFrame, filename: str):
    """Save data to CSV."""
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
