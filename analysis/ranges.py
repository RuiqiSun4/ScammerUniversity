import os
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

data = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
df = pd.read_csv(data)

os.makedirs("analysis/results", exist_ok = True)
save_path = os.path.join("analysis/results", "draft_pick_ranges_vs_win_shares.png")

pick = "Pk"
win_shares = "Advanced_WS"

df["pick_num"] = pd.to_numeric(df[pick], errors = "coerce")
a = list(range(0, 70, 5))
b = [f"{int(a[i]+1)}" for i in range(len(a)-1)]
df["group5"] = pd.cut(df["pick_num"], bins = a, labels = b, right=True, include_lowest=True)

df[win_shares] = pd.to_numeric(df[win_shares], errors = "coerce")
tbl = (
    df.dropna(subset=["pick_num", win_shares, "group5"])
    .groupby("group5", observed=True)
    .agg(
        Player = ("pick_num", "count"),
        Avg = (win_shares, "mean"),
        Median = (win_shares, "median"),
        std = (win_shares, "std"),    
    )
        .reset_index()
        )

round_cols = ["Avg", "Median", "std"]
for c in round_cols:
    if c in tbl.columns:
        tbl[c] = tbl[c].round(4)


rows, cols = tbl.shape
fig_height = max(3, 0.5 * (rows + 1))
fig_width = max(6, 1 * cols)

fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.axis("off")
ax.axis("tight")

table = ax.table(cellText=tbl.values,
                 colLabels=tbl.columns.tolist(),
                 loc="center")

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.2)

fig.tight_layout()
fig.savefig(save_path, dpi = 400, bbox_inches="tight" )
plt.close(fig)

print(tbl.to_string(index=False))