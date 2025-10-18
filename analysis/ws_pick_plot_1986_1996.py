import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import statsmodels.api as sm

# 1. Folder setup
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "artifacts", "nba_draft_1980_2010_cleaned.csv")
output_dir = os.path.join(base_dir, "results", "ws_pick")
os.makedirs(output_dir, exist_ok=True)

# 2. Load data
df = pd.read_csv(input_path)

# 3. Specify column names
year_col = "Year"
pick_col = "Pk"
ws_col = "Advanced_WS"

# 4. Remove missing values
df_clean = df[[year_col, pick_col, ws_col]].dropna()

# 5. Define target years
target_years = [1986, 1996]

# 6. Prepare regression output file
regression_output_file = os.path.join(output_dir, "ws_pick_regression_1986_1996.txt")
with open(regression_output_file, "w", encoding="utf-8") as f_out:
    f_out.write("OLS Regression Results for Selected Years\n")
    f_out.write("="*50 + "\n\n")

# 7. Scatter plot + regression + save results
sns.set_style("whitegrid")

for year in target_years:
    subset = df_clean[df_clean[year_col] == year]
    if subset.empty:
        print(f"No data found for {year}")
        continue

    # Pearson correlation
    r, pval = pearsonr(subset[pick_col], subset[ws_col])

    # Linear regression
    X = sm.add_constant(subset[pick_col])
    y = subset[ws_col]
    model = sm.OLS(y, X).fit()

    # Append regression summary to txt file
    with open(regression_output_file, "a", encoding="utf-8") as f_out:
        f_out.write(f"Year: {year}\n")
        f_out.write(model.summary().as_text())
        f_out.write("\n" + "="*50 + "\n\n")

    # Scatter plot with regression
    plt.figure(figsize=(7,5))
    sns.scatterplot(data=subset, x=pick_col, y=ws_col, alpha=0.6, edgecolor=None)
    sns.regplot(data=subset, x=pick_col, y=ws_col, scatter=False, color="red", line_kws={'linewidth':2})

    plt.title(f"WS vs Draft Pick – {year}", fontsize=14)
    plt.xlabel("Draft Pick Number")
    plt.ylabel("Win Shares")

    # Add r and p-value in plot
    plt.text(
        0.95, 0.95,
        f"r = {r:.3f}\np = {pval:.3f}",
        horizontalalignment='right',
        verticalalignment='top',
        transform=plt.gca().transAxes,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5)
    )

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    # Save figure
    filename = f"ws_pick_{year}_with_stats.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=300)
    plt.close()

print(f"Scatter plots and regression results saved in '{output_dir}' folder!")
print(f"Regression summary file: {regression_output_file}")
