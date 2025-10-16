# ws_pick_corr_trend.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# 1. Folder setup
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "artifacts", "nba_draft_1980_2010_cleaned.csv")
output_dir = os.path.join(base_dir, "results")
os.makedirs(output_dir, exist_ok=True)

# 2. Load data
df = pd.read_csv(input_path)

# 3. Specify column names
year_col = "Year"         
pick_col = "Pk"
ws_col = "Advanced_WS"

# 4. Remove missing values
df_clean = df[[year_col, pick_col, ws_col]].dropna()

# 5. Compute correlation by year
corr_list = []
for year, group in df_clean.groupby(year_col):
    if len(group) < 5:
        continue
    r, pval = pearsonr(group[pick_col], group[ws_col])
    corr_list.append({"Year": year, "Correlation_r": r, "p_value": pval, "N": len(group)})

corr_df = pd.DataFrame(corr_list)
corr_df.to_csv(os.path.join(output_dir, "ws_pick_corr_by_year.csv"), index=False)

# 6. Plot correlation trend
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
sns.lineplot(data=corr_df, x="Year", y="Correlation_r", marker="o")
plt.title("Yearly Correlation between Draft Pick and Win Shares (1980–2010)", fontsize=14)
plt.xlabel("Draft Year")
plt.ylabel("Correlation (r)")
plt.axhline(0, color="gray", linestyle="--", linewidth=1)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "ws_pick_corr_trend.png"), dpi=300)
plt.close()

print("Yearly correlation trend analysis complete!")
print("Results saved in 'analysis/ws_pick_corr_by_year.csv' and 'analysis/ws_pick_corr_trend.png'")
