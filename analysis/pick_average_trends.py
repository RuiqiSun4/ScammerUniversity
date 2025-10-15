import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

path = os.path.join("artifacts", "pick_group_averages.csv")
df = pd.read_csv(path)

cols = ['Pk', 'Totals_PTS', 'Per Game_PTS', 'Yrs', 'Totals_MP']
for c in cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# Plot and save each scatterplot with best-fit line 
for ycol, color, title, fname in [
    ('Totals_PTS', 'steelblue', 'Total Points vs Draft Pick', 'total_points.png'),
    ('Per Game_PTS', 'darkorange', 'Points per Game vs Draft Pick', 'points_per_game.png'),
    ('Yrs', 'seagreen', 'Total Years vs Draft Pick', 'total_years.png'),
    ('Totals_MP', 'firebrick', 'Total Minutes Played vs Draft Pick', 'total_minutes.png')
]:
    data = df[['Pk', ycol]].dropna()
    m, b = np.polyfit(data['Pk'], data[ycol], 1)
    
    # Create scatterplot
    ax = data.plot(
        kind='scatter',
        x='Pk',
        y=ycol,
        color=color,
        alpha=0.7,
        title=title
    )
    
    # Add best-fit line
    data.assign(fitted=m * data['Pk'] + b).plot(
        x='Pk',
        y='fitted',
        ax=ax,
        color='black',
        linewidth=1.5,
        legend=False
    )

    # Save to analysis folder
    output_path = os.path.join("analysis", fname)
    fig = ax.get_figure()
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig) 
    
    print(f"Saved plot: {output_path}")
