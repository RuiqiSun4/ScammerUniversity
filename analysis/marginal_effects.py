import os
import pandas as pd
import statsmodels.api as sm

script_dir = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join("artifacts", "nba_draft_1980_2010_cleaned.csv")
output_dir = os.path.join(script_dir, "results", "marginal_effects")
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(input_path)

# Defining y and 3 categories of x variables for marginal effects analysis
y_vars = ["Pk"]
x_cols_totals = ["Yrs",
                 "Totals_G",
                 "Totals_MP",
                 "Totals_PTS",
                 "Totals_TRB",
                 "Totals_AST"]

x_cols_per = ["Shooting_FG%", 
              "Shooting_3P%", 
              "Shooting_FT%", 
              "Per Game_MP",
              "Per Game_PTS",
              "Per Game_TRB",
              "Per Game_AST"]

x_cols_adv = ["Advanced_WS", 
              "Advanced_BPM",
              "Advanced_VORP"]

# Assigning x and y variables for regressions
x_vars_totals = df[x_cols_totals]
x_vars_per = df[x_cols_per]
x_vars_adv = df[x_cols_adv]

x_vars_totals = sm.add_constant(x_vars_totals)
x_vars_per = sm.add_constant(x_vars_per)
x_vars_adv = sm.add_constant(x_vars_adv)

y = df[y_vars]


#Creation of the models
model_totals = sm.OLS(y, x_vars_totals).fit()
model_per = sm.OLS(y, x_vars_per).fit()
model_adv = sm.OLS(y, x_vars_adv).fit()

# Printing the summaries to individual text files
output_path_totals = os.path.join(output_dir, "marginal_effects_totals.txt")
with open(output_path_totals, "w") as f:
    f.write(model_totals.summary().as_text())

output_path_per = os.path.join(output_dir, "marginal_effects_percentages.txt")
with open(output_path_per, "w") as f:
    f.write(model_per.summary().as_text())

output_path_adv = os.path.join(output_dir, "marginal_effects_advanced.txt")
with open(output_path_adv, "w") as f:
    f.write(model_adv.summary().as_text())

print(f"Marginal effects summaries saved at: {output_dir}/marginal_effects_(totals/percentages/advanced).txt")
