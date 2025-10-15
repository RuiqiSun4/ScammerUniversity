import requests
import pandas as pd
import time
from io import StringIO
import os

def scrape_draft_year(year):
    """
    Scrapes NBA draft data for a given year and returns it as a pandas DataFrame.
    """
    # 1. Create the target URL
    url = f"https://www.basketball-reference.com/draft/NBA_{year}.html"
    print(f"Scraping draft data for {year}. URL: {url}")

    try:
        # 2. Get the HTML content of the web page
        # Add headers to prevent the site from blocking the request.
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception if the request fails.

        # 3. Read the HTML table into a pandas DataFrame
        # Wrap in StringIO to avoid warnings in recent pandas versions.
        tables = pd.read_html(StringIO(response.text))
        
        if not tables:
            print(f"Could not find a table for the year {year}.")
            return None
            
        df = tables[0]

        # 4. Data Cleaning (Rename Headers)
        # If the header is a MultiIndex (multiple rows), join with '_'.
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() for col in df.columns.values]

        # 5. Data Cleaning (Remove intermediate header rows)
        # Instead of relying on column names, remove rows where the first column's value is 'Rk'.
        # This approach works more reliably for tables with varying structures.
        if not df.empty:
            # .iloc[:, 0] refers to the first column of all rows.
            df = df[df.iloc[:, 0] != 'Rk'].copy()

        # 6. Add Year Column
        # Add a 'Year' column to identify the draft year for each player after merging.
        df['Year'] = year
        
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {year}: {e}")
        return None

def main():
    """
    Scrapes all draft data from 1980 to 2010 and saves it to a CSV file.
    """
    # Create an empty list to store the data.
    all_drafts = []
    
    # Loop from 1980 to 2010.
    for year in range(1980, 2011):
        draft_df = scrape_draft_year(year)
        
        if draft_df is not None:
            all_drafts.append(draft_df)
            
        # Pause for a short duration (60 second) between requests to prevent overwhelming the server.
        time.sleep(60)

    # Concatenate all the yearly DataFrames into a single one.
    if all_drafts:
        final_df = pd.concat(all_drafts, ignore_index=True)
        os.makedirs("artifacts", exist_ok=True)
        output_path = os.path.join("artifacts", "nba_draft_1980_2010.csv")
        final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"\nAll data has been scraped successfully! Saved to '{output_path}'.")
        print("Final data sample:")
        print(final_df.head())
    else:
        print("No data was scraped.")

if __name__ == "__main__":
    main()

