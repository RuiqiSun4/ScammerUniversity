import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Load data ---
path = os.path.join("artifacts", "pick_group_averages.csv")
df = pd.read_csv(path)

# --- Picks and columns of interest ---
picks = [1, 2, 3, 10, 20, 30, 40, 50, 60]
cols = ['Pk', 'Totals_PTS', 'Per Game_PTS', 'Yrs', 'Totals_MP', 'Advanced_VORP']

# --- Filter, sort, and round ---
summary = (
    df[df['Pk'].isin(picks)][cols]
    .sort_values('Pk')
    .round(2)
)

# --- Ensure output folder exists ---
os.makedirs("analysis", exist_ok=True)

# --- Create a figure for the table ---
fig, ax = plt.subplots(figsize=(10, 3))
ax.axis('tight')
ax.axis('off')

# --- Create the table ---
tbl = ax.table(
    cellText=summary.values,
    colLabels=summary.columns,
    cellLoc='center',
    loc='center'
)

# --- Adjust layout for readability ---
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.2, 1.3)

# --- Add a title ---
plt.title("Draft Pick Summary (Selected Picks)", fontsize=14, pad=20, weight='bold')

# --- Save the table as PNG ---
out_path = os.path.join("analysis/results", "pick_summary_table.png")
plt.savefig(out_path, bbox_inches='tight', dpi=300)
plt.close(fig)

print(f"✅ Table image saved to: {out_path}")