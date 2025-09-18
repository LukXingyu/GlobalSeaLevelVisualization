import requests
import json
import pandas as pd
from datetime import datetime

def crawl_hko_sea_level_data():
    """
    Crawl Hong Kong Observatory yearly sea level data for QUB station
    Saves data to CSV format
    """
    print("Hong Kong Observatory Sea Level Data Crawler")
    print("=" * 50)
    
    # The JSON endpoint that contains all the data
    xml_url = "https://www.hko.gov.hk/cis/aws/tide/yearly_TIDE.xml"
    
    try:
        # Set proper headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.hko.gov.hk/en/cis/yearlyTide.htm'
        }
        
        print(f"Fetching data from: {xml_url}")
        response = requests.get(xml_url, headers=headers)
        response.raise_for_status()
        
        # Parse JSON data
        data = response.json()
        print(f"✓ Successfully retrieved data (Status: {response.status_code})")
        
        # Extract station data
        stations = data['tide']['data']
        print(f"✓ Found {len(stations)} stations in total")
        
        # Find QUB station data
        qub_data = None
        for station in stations:
            if station.get('code') == 'QUB':
                qub_data = station
                break
        
        if not qub_data:
            print("✗ QUB station data not found!")
            return None
        
        print(f"✓ Found QUB station data with {len(qub_data['yearData'])} years")
        
        # Process the data
        processed_data = []
        
        for year_record in qub_data['yearData']:
            # year_record format: [year, mean_sea_level, mean_higher_high_water, 
            #                      mean_lower_high_water, mean_higher_low_water, mean_lower_low_water]
            year = year_record[0]
            mean_sea_level = year_record[1] if year_record[1] != '***' else None
            mean_higher_high_water = year_record[2] if year_record[2] != '***' else None
            mean_lower_high_water = year_record[3] if year_record[3] != '***' else None
            mean_higher_low_water = year_record[4] if year_record[4] != '***' else None
            mean_lower_low_water = year_record[5] if year_record[5] != '***' else None
            
            processed_data.append({
                'Year': int(year),
                'Mean_Sea_Level_m': float(mean_sea_level) if mean_sea_level else None,
                'Mean_Higher_High_Water_m': float(mean_higher_high_water) if mean_higher_high_water else None,
                'Mean_Lower_High_Water_m': float(mean_lower_high_water) if mean_lower_high_water else None,
                'Mean_Higher_Low_Water_m': float(mean_higher_low_water) if mean_higher_low_water else None,
                'Mean_Lower_Low_Water_m': float(mean_lower_low_water) if mean_lower_low_water else None,
            })
        
        # Create DataFrame
        df = pd.DataFrame(processed_data)
        
        # Sort by year
        df = df.sort_values('Year')
        
        print(f"✓ Processed {len(df)} records from {df['Year'].min()} to {df['Year'].max()}")
        
        # Display summary statistics
        print("\nData Summary:")
        print("-" * 30)
        print(f"Data range: {df['Year'].min()} - {df['Year'].max()}")
        print(f"Total records: {len(df)}")
        
        # Count non-null values for each column
        for col in df.columns:
            if col != 'Year':
                non_null_count = df[col].notna().sum()
                print(f"{col}: {non_null_count} valid measurements")
        
        # Show first and last few records
        print("\nFirst 5 records:")
        print(df.head().to_string(index=False))
        
        print("\nLast 5 records:")
        print(df.tail().to_string(index=False))
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"HKO_QUB_SeaLevel_Data_{timestamp}.csv"
        
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"\n✓ Data saved to: {csv_filename}")
        
        # Also save a simplified version with just the main sea level data
        simple_df = df[['Year', 'Mean_Sea_Level_m']].copy()
        simple_df = simple_df.dropna()  # Remove years with missing data
        
        simple_csv_filename = f"HKO_QUB_MeanSeaLevel_Simple_{timestamp}.csv"
        simple_df.to_csv(simple_csv_filename, index=False, encoding='utf-8')
        print(f"✓ Simplified data (mean sea level only) saved to: {simple_csv_filename}")
        
        # Add metadata
        metadata = {
            'data_source': 'Hong Kong Observatory (HKO)',
            'station_code': 'QUB',
            'station_name': 'Quarry Bay',
            'data_url': 'https://www.hko.gov.hk/en/cis/yearlyTide.htm?stn=QUB',
            'api_endpoint': xml_url,
            'download_date': datetime.now().isoformat(),
            'units': 'meters above Chart Datum',
            'note': 'Tidal information from 1954 to 1985 are based on North Point tide gauge data. Mean Sea Levels are computed directly from on-site measurement data without any post data corrections including land settlement.',
            'total_records': len(df),
            'year_range': f"{df['Year'].min()}-{df['Year'].max()}"
        }
        
        metadata_filename = f"HKO_QUB_SeaLevel_Metadata_{timestamp}.json"
        with open(metadata_filename, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"✓ Metadata saved to: {metadata_filename}")
        
        return df
        
    except requests.RequestException as e:
        print(f"✗ Network error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"✗ JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return None

if __name__ == "__main__":
    result = crawl_hko_sea_level_data()
    
    if result is not None:
        print("\n" + "="*50)
        print("✓ Data crawling completed successfully!")
        print("\nFiles created:")
        print("1. Full dataset CSV with all tide measurements")
        print("2. Simplified CSV with mean sea level only")
        print("3. Metadata JSON file with source information")
    else:
        print("\n" + "="*50)
        print("✗ Data crawling failed!")