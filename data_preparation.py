"""
Phase 1: Data Preparation
Filters the world cities dataset to keep only Pakistani cities.
Extracts: City Name, Latitude, Longitude
"""

import pandas as pd

def filter_pakistani_cities(input_file, output_file):
    """
    Filter the world cities dataset to keep only Pakistani cities.
    
    Args:
        input_file: Path to the original worldcities.csv
        output_file: Path to save the filtered Pakistani cities
    
    Returns:
        DataFrame with Pakistani cities
    """
    # Step 1: Load the dataset
    print("Loading world cities dataset...")
    df = pd.read_csv(input_file)
    
    print(f"Total cities in dataset: {len(df)}")
    
    # Step 2: Filter for Pakistan only
    # Using the 'country' column to filter
    pakistan_df = df[df['country'] == 'Pakistan']
    
    print(f"Cities in Pakistan: {len(pakistan_df)}")
    
    # Step 3: Extract only the required columns
    # Rename columns to match project requirements
    cleaned_df = pakistan_df[['city', 'lat', 'lng']].copy()
    cleaned_df.columns = ['City', 'Latitude', 'Longitude']
    
    # Step 4: Remove any duplicates and reset index
    cleaned_df = cleaned_df.drop_duplicates(subset=['City']).reset_index(drop=True)
    
    print(f"Unique Pakistani cities after cleanup: {len(cleaned_df)}")
    
    # Step 5: Save to CSV
    cleaned_df.to_csv(output_file, index=False)
    print(f"Saved filtered data to: {output_file}")
    
    return cleaned_df


if __name__ == "__main__":
    # Input and output file paths
    input_path = "simplemaps_worldcities_basicv1.901/worldcities.csv"
    output_path = "pak_cities.csv"
    
    # Run the filtering
    pak_cities = filter_pakistani_cities(input_path, output_path)
    
    # Display sample of the data
    print("\n--- Sample Pakistani Cities ---")
    print(pak_cities.head(20))
    
    # Display some statistics
    print(f"\nLatitude range: {pak_cities['Latitude'].min():.4f} to {pak_cities['Latitude'].max():.4f}")
    print(f"Longitude range: {pak_cities['Longitude'].min():.4f} to {pak_cities['Longitude'].max():.4f}")

