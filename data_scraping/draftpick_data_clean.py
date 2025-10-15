import pandas as pd
import re

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

    # 2. Create and populate the 'Round' column using column position.
    #    - We assume the player name is in the 4th column (index 3).
    try:
        df['Round'] = df.iloc[:, 3].str.extract(r'Round (\d+)').astype(float)
        df['Round'].fillna(method='ffill', inplace=True)
        df['Round'].fillna(1, inplace=True)
        df['Round'] = df['Round'].astype(int)
    except IndexError:
        print(f"Error: The CSV file does not have enough columns (expected at least 4).")
        return
    except Exception as e:
        print(f"An error occurred while creating the 'Round' column: {e}")
        return

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

    # 5. Reorder the columns to place 'Year' and 'Round' at the front.
    #    - The 'Year' column is typically the last one added by the scraper.
    try:
        year_col_name = df.columns[-1] # Find the name of the last column
        all_other_cols = [col for col in df.columns if col != year_col_name and col != 'Round']
        new_order = [year_col_name, 'Round'] + all_other_cols
        df = df[new_order]
        print("Reordered columns.")
    except Exception as e:
        print(f"Could not reorder columns. Error: {e}")
    
    #5. Fill blanks with 0
    df.fillna(0, inplace=True)
    
    # 5. Save the cleaned DataFrame to a new CSV file.
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nSuccessfully cleaned the data and saved it to '{output_path}'.")
    print("Sample of the cleaned data:")
    print(df.head())


if __name__ == '__main__':
    # Define the input file (from the scraper) and the output file (for the cleaned data)
    raw_data_path = 'nba_draft_1980_2010.csv'
    cleaned_data_path = 'nba_draft_1980_2010_cleaned.csv'
    
    # Run the cleaning process
    clean_nba_draft_data(raw_data_path, cleaned_data_path)