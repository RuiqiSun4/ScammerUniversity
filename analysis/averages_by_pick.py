import pandas as pd
import os

# Load the cleaned data
cleaned_path = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
df = pd.read_csv(cleaned_path)


# Compute averages, drop irrelevant columns, and round to 2 decimal places.
group_avg_all = df.groupby('Pk').mean(numeric_only=True).reset_index()
group_avg_all = group_avg_all.drop(columns=['Round', 'Round.1', 'Year'], errors='ignore')
group_avg_all = group_avg_all.round(2)

# Print a preview
print("Average of all numeric columns by overall pick:")
print(group_avg_all.head(10))

# Save to a CSV file
output_path = os.path.join("artifacts", "pick_group_averages.csv")
group_avg_all.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\nSaved full averages table to: {output_path}")