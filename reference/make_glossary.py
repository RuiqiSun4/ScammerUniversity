import pandas as pd
import os

# Get the directory where this script is located
current_dir = os.path.dirname(__file__)

# Define the output path for the CSV file
output_path = os.path.join(current_dir, "nba_stat_glossary.csv")

# Define NBA stat abbreviation glossary data
data = [
    {"Abbreviation": "G", "Full Name": "Games Played", "Description": "Total number of games played by the player"},
    {"Abbreviation": "MP", "Full Name": "Minutes Played", "Description": "Total minutes played"},
    {"Abbreviation": "PTS", "Full Name": "Points", "Description": "Total points scored"},
    {"Abbreviation": "TRB", "Full Name": "Total Rebounds", "Description": "Total number of rebounds"},
    {"Abbreviation": "AST", "Full Name": "Assists", "Description": "Total number of assists"},
    {"Abbreviation": "FG%", "Full Name": "Field Goal Percentage", "Description": "Field goal success rate"},
    {"Abbreviation": "3P%", "Full Name": "Three-Point Percentage", "Description": "Three-point shot success rate"},
    {"Abbreviation": "FT%", "Full Name": "Free Throw Percentage", "Description": "Free throw success rate"},
    {"Abbreviation": "WS", "Full Name": "Win Shares", "Description": "Estimated contribution to team wins"},
    {"Abbreviation": "WS/48", "Full Name": "Win Shares per 48 Minutes", "Description": "Win contribution per 48 minutes"},
    {"Abbreviation": "BPM", "Full Name": "Box Plus/Minus", "Description": "Impact compared to an average player (± scale)"},
    {"Abbreviation": "VORP", "Full Name": "Value Over Replacement Player", "Description": "Value compared to a replacement-level player (higher is better)"},
    {"Abbreviation": "Reference", "Full Name": "For more information", "Description": "https://www.basketball-reference.com/draft/"}
]

# Create a DataFrame and save it as a CSV file
df = pd.DataFrame(data)
df.to_csv(output_path, index=False)

# This script generates a glossary of NBA stat abbreviations
# and saves the output file in the same folder as the script (reference/).