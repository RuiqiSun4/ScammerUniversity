import os
import pandas as pd
import statsmodels.api as sm

input_path = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
output_dir = "results"
os.makedirs( output_dir, exist_ok=True)

df = pd.read_csv(input_path)

# Defining x and y variables for easier addition/removal
y_vars = ["Pk"]

x_vars = ["Per Game_PTS",
          "Per Game_TRB",
          "Per Game_AST"
          ] 


# Assigning x and y variables for regression
x = df[x_vars]
y = df[y_vars]
x = sm.add_constant(x)

# Creation of the model

model = sm.OLS(y, x).fit()
print(model.summary().as_text())


output_path = os.path.join("analysis", "results", "general_regression_summary.txt")
with open(output_path, "w") as f:
    f.write(model.summary().as_text())

print("General regression summary saved at: {output_dir}/general_regression_summary.txt")
