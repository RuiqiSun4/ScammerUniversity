import pandas as pd
import os

# Load the cleaned data
cleaned_path = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
df = pd.read_csv(cleaned_path)


# Compute average total points and points per game for each group
group_avg_all = df.groupby('Pk').mean(numeric_only=True).reset_index()

# Print a preview
print("Average of all numeric columns by overall pick:")
print(group_avg_all.head(10))

# Save to a CSV file
output_path = os.path.join("artifacts", "pick_group_averages.csv")
group_avg_all.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\nSaved full averages table to: {output_path}")