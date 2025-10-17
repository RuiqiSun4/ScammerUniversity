# ws_vorp.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, linregress

# 1. Set up folder paths
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "artifacts", "nba_draft_1980_2010_cleaned.csv")
output_dir = os.path.join(base_dir, "results", "ws_vorp")
os.makedirs(output_dir, exist_ok=True)

# 2. Load cleaned draft data
df = pd.read_csv(input_path)

# 3. Specify relevant column names
year_col = "Year"
ws_col = "Advanced_WS"
vorp_col = "Advanced_VORP"

# 4. Drop rows with missing values
df_clean = df[[year_col, ws_col, vorp_col]].dropna()

# 5. Compute Pearson correlation by year
corr_list = []
for year, group in df_clean.groupby(year_col):
    if len(group) < 5:
        continue
    r, pval = pearsonr(group[ws_col], group[vorp_col])
    corr_list.append({
        "Year": year,
        "Correlation_r": r,
        "p_value": pval,
        "N": len(group)
    })

corr_df = pd.DataFrame(corr_list)
corr_df.to_csv(os.path.join(output_dir, "ws_vorp_corr_by_year.csv"), index=False)

# 6. Perform linear regression on yearly correlation trend
slope, intercept, r_value, p_value, std_err = linregress(corr_df["Year"], corr_df["Correlation_r"])

# 7. Plot correlation trend with regression line and stats
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))

# 8. Plot yearly correlation points
sns.lineplot(data=corr_df, x="Year", y="Correlation_r", marker="o", label="Yearly Correlation")

# 9. Plot regression trendline
plt.plot(
    corr_df["Year"],
    intercept + slope * corr_df["Year"],
    color="red",
    linestyle="--",
    label="Trendline"
)

# 10. Set y-axis range 
plt.ylim(0.85, 1.0)

# 11. Add title and axis labels
plt.title("Yearly Correlation Trend between Win Shares and VORP (1980–2010)", fontsize=12)
plt.xlabel("NBA Draft Year")
plt.ylabel("Correlation (r)")
plt.axhline(0, color="gray", linestyle="--", linewidth=1)
plt.legend()

# 12. Display regression statistics on the plot 
stats_text = f"Slope: {slope:.3f}\nR²: {r_value**2:.3f}\np-value: {p_value:.4f}"
plt.text(
    0.05, 0.95, stats_text,
    transform=plt.gca().transAxes,  # use relative coordinates (0–1)
    fontsize=10,
    verticalalignment='top',
    horizontalalignment='left',
    bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5')
)

# 13. Final layout and save
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "ws_vorp_corr_trend.png"), dpi=300)
plt.close()

# 14. Completion message
print("Yearly correlation trend analysis between WS and VORP complete!")
print("Results saved in 'results/ws_vorp_corr_by_year.csv' and 'results/ws_vorp_corr_trend.png'")