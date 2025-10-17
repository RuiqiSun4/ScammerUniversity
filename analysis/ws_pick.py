# ws_pick_analysis.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import pearsonr

# 1. Folder setup 
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "artifacts", "nba_draft_1980_2010_cleaned.csv")
output_dir = os.path.join(base_dir, "results")
os.makedirs(output_dir, exist_ok=True)

# 2. load cleaned NBA draft data
df = pd.read_csv(input_path)

# 3. Specify column names
pick_col = "Pk"
ws_col = "Advanced_WS"

# 4. Remove missing values
# Remove rows where either the pick_col or ws_col column contains a missing value (NaN).
df_clean = df[[pick_col, ws_col]].dropna()

# 5. OLS regression
X = sm.add_constant(df_clean[pick_col])
y = df_clean[ws_col]
model = sm.OLS(y, X).fit()

# 6. Save regression summary
with open(os.path.join(output_dir, "ws_pick.txt"), "w", encoding="utf-8") as f:
    f.write(model.summary().as_text())

# 7. Calculate Pearson correlation coefficient and p-value
r, pval = pearsonr(df_clean["Pk"], df_clean["Advanced_WS"])
n = len(df_clean)   # Number of observations

# 8. Set plot style and create scatterplot with regression line
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.scatterplot(x="Pk", y="Advanced_WS", data=df, alpha=0.6, label="Players")
sns.regplot(x="Pk", y="Advanced_WS", data=df, scatter=False, color="red", line_kws={"label": "Linear Fit"})

# 9. Annotate plot with correlation statistics
stats_text = f"r = {r:.3f}, p = {pval:.3g}, n = {n}"
plt.text(0.95, 0.95, stats_text, transform=plt.gca().transAxes,
         fontsize=12, verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))

# 10. Add title, axis labels, and legend
plt.title("Win Shares by Draft Pick (1980–2010)", fontsize=16)
plt.xlabel("NBA Draft Pick Ranks")
plt.ylabel("Win Shares")
plt.legend()
plt.tight_layout()

# 11. Save plot
plt.savefig(os.path.join(output_dir, "ws_pick.png"), dpi=300)
plt.close()

print("Analysis complete! Results saved in the 'analysis/' folder.")