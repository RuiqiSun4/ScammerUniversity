import requests
import json
import pandas as pd
import sys
import time

# --- 1. Global Constants ---
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
# Measure Code for Unemployment Rate (Rate) at the State Level in LAUS
MEASURE_CODE = "0000000003" 
START_YEAR = "2020"
END_YEAR = "2022"
MAX_SERIES_PER_REQUEST = 50 

# --- 2. State FIPS Codes (50 States + DC) ---
# FIPS codes used for BLS LAUS State IDs.
STATE_FIPS_CODES = [
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", 
    "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", 
    "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", 
    "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", 
    "54", "55", "56"
]

# --- 3. Series ID Generation Function ---
def generate_series_ids(fips_list, measure_code):
    """Generates BLS LAUS State Series IDs (Unemployment Rate) using state FIPS codes."""
    all_series_ids = []
    # State LAUS Series ID format: LAU + S (State) + T (Not Seasonally Adjusted) + 
    # State FIPS (2 digits) + 000 (Area Sub-code) + Measure Code (10 digits)
    for fips in fips_list:
        area_code = fips + "000"
        series_id = f'LAUST{area_code}{measure_code}'
        all_series_ids.append((series_id, fips)) # (Series ID, FIPS)
        
    return all_series_ids

# --- 4. Data Fetching and Processing ---
def fetch_bls_data(series_id_metadata):
    all_data_frames = []
    series_id_list = [sid for sid, fips in series_id_metadata]
    fips_map = {sid: fips for sid, fips in series_id_metadata} # ID -> FIPS mapping
    
    for i in range(0, len(series_id_list), MAX_SERIES_PER_REQUEST):
        chunk_ids = series_id_list[i:i + MAX_SERIES_PER_REQUEST]
        
        payload = {
            "seriesid": chunk_ids,
            "startyear": START_YEAR,
            "endyear": END_YEAR,
            "annualaverage": "false" 
        }
        
        try:
            response = requests.post(
                BLS_API_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            response.raise_for_status()
            data = response.json()
            
            # Check API response status
            if data.get("status") != "REQUEST_SUCCEEDED":
                print(f"Warning: BLS API request failed or no data (Chunk {i}).")
                if data.get("message"):
                     print("BLS detailed message:", data["message"])
                continue

            for series in data.get("Results", {}).get("series", []):
                sid = series["seriesID"]
                fips = fips_map.get(sid)
                
                if not series.get("data"):
                    print(f"Warning: No data found for series ID {sid} (State FIPS {fips}).")
                    continue
                
                records = []
                for item in series["data"]:
                    # Filter for monthly data (M01-M12)
                    if item.get("period", "").startswith("M") and item["period"] != "M13":
                        value = item.get("value")
                        if value is not None and value != '':
                            records.append({
                                "fips": fips,
                                "year": item["year"],
                                "period": item["period"],
                                "month_name": item["periodName"],
                                "unemployment_rate": float(value) 
                            })
                
                if records: 
                    all_data_frames.append(pd.DataFrame(records))

            print(f"API call progress: {i + len(chunk_ids)}/{len(series_id_list)} completed. Waiting for 3 seconds...")
            time.sleep(3) 
            
        except requests.exceptions.RequestException as e:
            print(f"API request error occurred (Chunk {i}): {e}")
            time.sleep(10)
            continue
            
    return all_data_frames

# --- 5. Main Execution Logic ---
if __name__ == "__main__":
    # 1. Generate Series IDs
    series_metadata = generate_series_ids(STATE_FIPS_CODES, MEASURE_CODE)
    
    # 2. Fetch data from BLS API
    dfs = fetch_bls_data(series_metadata)
    
    if not dfs:
        sys.exit(1)
        
    # 3. Concatenate DataFrames and Calculate Employment Rate
    final_df = pd.concat(dfs, ignore_index=True)
    
    if final_df.empty:
        sys.exit(1)

    # Calculate Employment Rate: 100 - Unemployment Rate
    final_df["employment_rate"] = 100.0 - final_df["unemployment_rate"]

    # Final cleanup and save
    final_df = final_df.sort_values(by=["fips", "year", "period"])
    final_df = final_df[["fips", "year", "month_name", "unemployment_rate", "employment_rate"]]
    
    output_filename = "us_state_employment_rate_2020_2022.csv"
    final_df.to_csv(output_filename, index=False)
    