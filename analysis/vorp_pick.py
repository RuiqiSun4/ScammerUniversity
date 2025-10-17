import os 
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np

#load data
data = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
df = pd.read_csv(data)

# create paths
os.makedirs("analysis/results", exist_ok = True)
save_path = os.path.join("analysis/results", "Draft_Pick_vs_VORP")

#assign variables
pick = "Pk"
vorp = "Advanced_VORP"
x = pd.to_numeric(df[pick], errors = "coerce")
y = pd.to_numeric(df[vorp])
mask = np.isfinite(x) & np.isfinite(y)
x = x[mask].to_numpy()
y = y[mask].to_numpy()

#line of best fit
m, b = np.polyfit(x, y, 1)

xs = np.linspace(x.min(), x.max(), 400)
ys = m * xs + b 

#create figure
plt.figure()
plt.scatter(x, y, s=10, alpha = 0.6)
plt.plot(xs, ys, color = "black", linewidth = 1.5, zorder = 2)
plt.title("Draft Position vs VORP")
plt.xlabel("Draft Position")
plt.ylabel("VORP")
plt.grid(True)
plt.tight_layout()
plt.savefig(save_path)
plt.show()
plt.close()
