import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_every_player(input_path):
    """
    Reads the final cleaned and grouped draft data, analyzes the relationship
    between players' key performance metrics with picks, and visualizes the results.
    """
    # 1. Read csv
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"error: '{input_path}' not found.")
        return

    # 2. Choose columns to analyze 
    stats_to_analyze = ['Per Game_PTS', 'Advanced_WS/48', 'Advanced_BPM', 'Advanced_VORP']
  
    # 3. Analyze in tables (setup)
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('Key Metrics by Draft Picks of NBA players', fontsize=20)

    sns.regplot(ax=axes[0, 0], x='Pk', y=stats_to_analyze[0], data=df,
                scatter_kws={'s': 10, 'color': 'red', 'alpha': 0.5},
                line_kws={'color': 'blue'})
    axes[0, 0].set_title('Per Game Points', fontsize=14)
    axes[0, 0].set_xlabel('Draft Pick', fontsize=12)
    #axes[0, 0].set_ylabel('Per Game Points', fontsize=12)
    
    sns.regplot(ax=axes[0, 1], x='Pk', y=stats_to_analyze[1], data=df,
                scatter_kws={'s': 10, 'color': 'red', 'alpha': 0.5},
                line_kws={'color': 'blue'})
    axes[0, 1].set_title('Win Shares per 48 minutes', fontsize=14)
    axes[0, 1].set_xlabel('Draft Pick', fontsize=12)
    #axes[0, 1].set_ylabel('Win Shares per 48 minutes', fontsize=12)

    sns.regplot(ax=axes[1, 0], x='Pk', y=stats_to_analyze[2], data=df,
                scatter_kws={'s': 10, 'color': 'red', 'alpha': 0.5},
                line_kws={'color': 'blue'})
    axes[1, 0].set_title('Box Plus/Minus', fontsize=14)
    axes[1, 0].set_xlabel('Draft Pick', fontsize=12)
    #axes[1, 0].set_ylabel('Box Plus/Minus', fontsize=12)

    sns.regplot(ax=axes[1, 1], x='Pk', y=stats_to_analyze[3], data=df,
                scatter_kws={'s': 10, 'color': 'red', 'alpha': 0.5},
                line_kws={'color': 'blue'})
    axes[1, 1].set_title('Value over Replacement Player', fontsize=14)
    axes[1, 1].set_xlabel('Draft Pick', fontsize=12)
    #axes[1, 1].set_ylabel('Value over Replacement Player', fontsize=12)

    axes[0, 1].set_ylim(-0.5, 0.5)
    axes[1, 0].set_ylim(-20, 20)
    axes[0, 0].set_xlim(1, 60)
    axes[1, 0].set_xlim(1, 60)
    axes[0, 1].set_xlim(1, 60)
    axes[1, 1].set_xlim(1, 60)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

if __name__ == '__main__':
    input_file_path = '../artifacts/nba_draft_1980_2010_cleaned_grouped.csv'
    analyze_every_player(input_file_path)

