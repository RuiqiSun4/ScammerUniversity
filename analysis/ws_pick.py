# ws_pick_analysis.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 1. Folder setup 
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "artifacts", "nba_draft_1980_2010_cleaned.csv")
output_dir = os.path.join(base_dir, "results")
os.makedirs(output_dir, exist_ok=True)

# 2. load data
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
with open(os.path.join(output_dir, "regression_summary.txt"), "w", encoding="utf-8") as f:
    f.write(model.summary().as_text())

# 7. Scatter plot + regression line
plt.figure(figsize=(8,6))
sns.scatterplot(data=df_clean, x=pick_col, y=ws_col, alpha=0.6, edgecolor=None)
sns.regplot(data=df_clean, x=pick_col, y=ws_col, scatter=False, color="red", line_kws={'linewidth': 2})
plt.title("Win Shares vs Draft Pick (1980–2010)", fontsize=14)
plt.xlabel("Draft Pick Number")
plt.ylabel("Win Shares")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# 8. Save plot
plt.savefig(os.path.join(output_dir, "ws_pick.png"), dpi=300)
plt.close()

print("Analysis complete! Results saved in the 'analysis/' folder.")