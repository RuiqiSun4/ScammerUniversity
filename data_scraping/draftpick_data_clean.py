import pandas as pd
import re

def clean_nba_draft_data(input_path, output_path):
    """
    Reads the raw NBA draft CSV, cleans it, and saves a new CSV file.
    """
    # 1. Load the CSV file into a pandas DataFrame
    print(f"Loading data from '{input_path}'...")
    df = pd.read_csv(input_path)

    # Find the correct 'Player' and 'Pk' columns, as their names can vary
    try:
        player_col = next(col for col in df.columns if 'Player' in col)
        pk_col = next(col for col in df.columns if 'Pk' in col)
    except StopIteration:
        print("Error: Could not find 'Player' or 'Pk' columns in the CSV. Aborting.")
        return

    # 2. Create and populate the 'Round' column
    #    - Extracts the round number from rows that act as headers (e.g., 'Round 2').
    #    - Forward-fills the round number to apply it to all subsequent players.
    #    - Sets '1' for the first round.
    df['Round'] = df[player_col].str.extract(r'Round (\d+)').astype(float)
    df['Round'].fillna(method='ffill', inplace=True)
    df['Round'].fillna(1, inplace=True) # Assume the data starts with Round 1
    df['Round'] = df['Round'].astype(int) # Convert to integer (1, 2, 3...)
    print("Created and populated the 'Round' column.")

    # 3. Remove the intermediate header rows
    #    - These are the rows where we just extracted the round number from (e.g., 'Round 2').
    #    - Also removes any rows where the pick number is not a valid number.
    df = df[pd.to_numeric(df[pk_col], errors='coerce').notna()]
    print("Removed intermediate header rows.")
    
    # 4. Clean up the column names at the end of the process
    #    - This step is still needed to get the desired final column names like 'Player', 'College'.
    def clean_col_name(col_name):
        # Use regex to find and remove patterns like 'Round X_' or 'Category_'
        cleaned_name = re.sub(r'^(Round \d+_|Totals_|Shooting_|Per Game_|Advanced_|Unnamed: \d+_level_\d+_)', '', col_name)
        return cleaned_name
    
    df.columns = [clean_col_name(col) for col in df.columns]
    print("Cleaned up column names.")

    # 5. Reorder the columns
    #    - Moves the 'Year' and 'Round' columns to the beginning of the table.
    cols = df.columns.tolist()
    # Remove 'Year' and 'Round' from their current positions
    cols.remove('Year')
    cols.remove('Round')
    # Add them to the front
    new_order = ['Year', 'Round'] + cols
    df = df[new_order]

    # 6. Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nSuccessfully cleaned the data and saved it to '{output_path}'.")
    print(df.head())


if __name__ == '__main__':
    # Define the input file (from the scraper) and the output file (for the cleaned data)
    raw_data_path = 'nba_draft_1980_2010_original.csv'
    cleaned_data_path = 'nba_draft_1980_2010_cleaned.csv'
    
    # Run the cleaning process
    clean_nba_draft_data(raw_data_path, cleaned_data_path)