import pandas as pd
import re
import os

def clean_nba_draft_data(input_path, output_path):
    """
    Reads the raw NBA draft CSV, cleans it, and saves a new CSV file.
    Relies on column positions instead of names to handle corrupted headers.
    """
    # 1. Load the CSV file, ignoring potential errors.
    print(f"Loading data from '{input_path}'...")
    try:
        df = pd.read_csv(
            input_path, 
            encoding='latin-1', 
            engine='python', 
            on_bad_lines='skip',
            header=0  # Treat the first row as the header, even if it's corrupted.
        )
    except Exception as e:
        print(f"Failed to load CSV file. Error: {e}")
        return

    # 2. Delete rows with Rounds
    df.dropna(subset=['Unnamed: 2_level_0_Tm'])

    # 3. Remove intermediate header rows using column position.
    #    - We assume the pick number is in the 1st column (index 0).

    df = df[pd.to_numeric(df.iloc[:, 0], errors='coerce').notna()]
    print("Removed intermediate header rows.")

    try:
        df.drop(df.columns[[0, 2]], axis=1, inplace=True)
    except IndexError:
        print("error. no columns to delete")
        return
    
    # 4. Clean column names 
    def clean_col_name(col_name):
        name = re.sub(r'^(Unnamed: \d+_level_\d+_)', '', col_name)
        name = re.sub(r'^(Round \d+_)', '', name)
        return name
    
    df.rename(columns=clean_col_name, inplace=True)

    # 5. Fill blanks with 0
    df.fillna(0, inplace=True)

    # 6. Keep only picks 1–60
    df['Pk'] = pd.to_numeric(df['Pk'], errors='coerce')  
    df = df[df['Pk'] <= 60].copy()                       
    print(f"Remaining rows after filtering top 60 picks: {len(df)}")
    
    # 7. Save the cleaned DataFrame to a new CSV file.
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nSuccessfully cleaned the data and saved it to '{output_path}'.")
    print("Sample of the cleaned data:")
    print(df.head())


if __name__ == '__main__':
    # Define the input file (from the scraper) and the output file (for the cleaned data)
    raw_data_path = os.path.join("../artifacts", "nba_draft_1980_2010.csv")
    cleaned_data_path = os.path.join("../artifacts", "nba_draft_1980_2010_cleaned.csv")

    # Run the cleaning process
    clean_nba_draft_data(raw_data_path, cleaned_data_path)
