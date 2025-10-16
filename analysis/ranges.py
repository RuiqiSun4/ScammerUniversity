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
        Avg_Win_Shares = (win_shares, "mean"),
        Median_Win_Shares = (win_shares, "median"),
        std_Win_Shares = (win_shares, "std"),    
    )
        .reset_index()
        )

print(tbl.to_string(index=False))