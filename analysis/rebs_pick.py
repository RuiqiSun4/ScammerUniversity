import os 
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

data = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
df = pd.read_csv(data)

pick = "Pk"
rebs = "Per Game_TRB"

x = df[pick]
y = df[rebs]

plt.figure()
plt.scatter(x, y)
plt.title("Draft Position vs Rebounds per Game")
plt.xlabel("Draft Position")
plt.ylabel("Rebounds per Game")
plt.grid(True)
plt.tight_layout()
plt.show()
