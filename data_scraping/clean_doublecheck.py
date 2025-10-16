import os
import pandas as pd

"""The goal of this file is to double check the cleaning process in data_scraping/draftpick_data_clean, not necessarily to change anything
in nba_draft_1980_2010_cleaned.csv."""

input_path = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
output_dir = "data_scraping_check"

df = pd.read_csv(input_path)

def total_NA_values(df):
    """Counts total NA values in dataframe, and returns the names of columns with NA values along with NA values per column."""
    total_NA = df.isna().sum().sum()
 
    if total_NA > 0:
        cols_with_NA = df.columns[df.isna().any()].tolist()
        print(f"Total NA values in dataset: {total_NA}")
        print(f"NA value counts per column: {df[cols_with_NA].isna().sum().to_dict()}")
    else:
        print(f"Total NA values in dataset: {total_NA}. No NA values found in dataset.")
        return 0

    
def duplicate_entries(df):
    """Checks for duplicate entries in dataframe by checking select columns, and returns
    the rows with duplicate entries."""
    dup_entry = df.duplicated(subset=["Year", "Player", "College", "Totals_G"], keep=False)
    if dup_entry.any():
        dup_rows = df[dup_entry]
        print(f"Duplicate entries found:\n{dup_rows}")
    else:
        print("No duplicate entries found.")
        return 0

# Running checks

NA_count = total_NA_values(df)
dup_count = duplicate_entries(df)

if NA_count == 0 and dup_count == 0:
    print("Data cleaning process verified. No NA values or duplicate entries found.")
else:
    print("Data cleaning process not verified. Please check issues above.")
