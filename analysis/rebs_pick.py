import os 
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

data = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
df = pd.read_csv(data)

pick = "Pk"
rebs = "Per Game_TRB"
x = pd.to_numeric(df[pick], errors = "coerce")
y = pd.to_numeric(df[rebs])
mask = np.isfinite(x) & np.isfinite(y)
x = x[mask].to_numpy()
y = y[mask].to_numpy()

m, b = np.polyfit(x, y, 1)

xs = np.linspace(x.min(), x.max(), 400)
ys = m * xs + b

plt.figure()
plt.scatter(x, y, s=10, alpha = 0.6)
plt.plot(xs, ys, color = "black", linewidth = 1.5, zorder = 2)
plt.title("Draft Position vs Rebounds per Game")
plt.xlabel("Draft Position")
plt.ylabel("Rebounds per Game")
plt.grid(True)
plt.tight_layout()
plt.show()
