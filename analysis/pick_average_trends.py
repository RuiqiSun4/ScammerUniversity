import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load data 
path = os.path.join("artifacts", "pick_group_averages.csv")
df = pd.read_csv(path)

# Ensure numeric types
cols = ['Pk', 'Totals_PTS', 'Per Game_PTS', 'Yrs', 'Totals_MP']
for c in cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

df = df.dropna(subset=['Pk'])

# Ensure output folder exists 
os.makedirs("analysis/results", exist_ok=True)

# Plot all four in one figure 
fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)
fig.suptitle("Draft Outcomes vs Overall Pick (Averages by Pick)", fontsize=16, y=0.98)

plots = [
    ('Totals_PTS',   'Total Points',         'steelblue',  axes[0, 0]),
    ('Per Game_PTS', 'Points per Game',      'darkorange', axes[0, 1]),
    ('Yrs',          'Total Years',          'seagreen',   axes[1, 0]),
    ('Totals_MP',    'Total Minutes Played', 'firebrick',  axes[1, 1]),
]

for ycol, ylabel, color, ax in plots:
    data = df[['Pk', ycol]].dropna().sort_values('Pk')
    if data.empty:
        ax.set_title(f"{ylabel} (no data)")
        ax.axis('off')
        continue

    # Fit line
    m, b = np.polyfit(data['Pk'], data[ycol], 1)

    # Scatter + fitted line
    ax.scatter(data['Pk'], data[ycol], alpha=0.7, label=ylabel, color=color)
    ax.plot(data['Pk'], m * data['Pk'] + b, color='black', linewidth=1.5, label='Fit')

    # Labels & grid
    ax.set_title(f"{ylabel} vs Draft Pick", fontsize=11)
    ax.set_xlabel("Overall Pick")
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle='--', alpha=0.4)

# Layout & save
plt.tight_layout(rect=[0, 0, 1, 0.96])
out_path = os.path.join("analysis/results", "draft_pick_trends.png")
fig.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close(fig)

print(f"Saved combined figure: {out_path}")
