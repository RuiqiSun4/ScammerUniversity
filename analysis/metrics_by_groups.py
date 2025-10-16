import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_draft_groups(input_path):
    """
    Reads the final cleaned and grouped draft data, analyzes the relationship
    between draft groups and key performance metrics, and visualizes the results.
    """
    # 1. Read csv
    df = pd.read_csv(input_path)

    # 2. Choose columns to analyze
    stats_to_analyze = ['Per Game_PTS', 'Advanced_WS/48', 'Advanced_BPM', 'Advanced_VORP']
  
    # 3. Analyze in tables
    group_analysis = df.groupby('Group')[stats_to_analyze].mean()
    try:
        fig_table, ax_table = plt.subplots(figsize=(10, 4))
        ax_table.set_title("Average Metrics by Groups of Draftees", fontsize=16, pad=20)
        ax_table.axis('tight')
        ax_table.axis('off')
        table_data = group_analysis.round(2)
        the_table = ax_table.table(cellText=table_data.values,
                                   colLabels=table_data.columns,
                                   rowLabels=table_data.index,
                                   loc='center',
                                   cellLoc='center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(12)
        the_table.scale(1.2, 1.4)
        plt.show()
    except Exception as e:
        print(f"Error in making tables: {e}")

    # 5. Bar plot the results
    try:
        sns.set_style("whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle("Average Metrics by Groups of Draftees", fontsize=18)
        
        sns.barplot(ax=axes[0, 0], x=group_analysis.index, y=group_analysis['Per Game_PTS'])
        axes[0, 0].set_title('Per Game_PTS', fontsize=14)
        axes[0, 0].set_xlabel('Groups')
        axes[0, 0].set_ylabel('Per Game_PTS')

        sns.barplot(ax=axes[0, 1], x=group_analysis.index, y=group_analysis['Advanced_WS/48'])
        axes[0, 1].set_title('Win Shares per 48 minutes', fontsize=14)
        axes[0, 1].set_xlabel('Groups')
        axes[0, 1].set_ylabel('Win Shares per 48 minutes')

        sns.barplot(ax=axes[1, 0], x=group_analysis.index, y=group_analysis['Advanced_BPM'])
        axes[1, 0].set_title('Box Plus/Minus', fontsize=14)
        axes[1, 0].set_xlabel('Groups')
        axes[1, 0].set_ylabel('Box Plus/Minus')
        
        sns.barplot(ax=axes[1, 1], x=group_analysis.index, y=group_analysis['Advanced_VORP'])
        axes[1, 1].set_title('Value over Replacement Player', fontsize=14)
        axes[1, 1].set_xlabel('Groups')
        axes[1, 1].set_ylabel('Value over Replacement Player')

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
    except Exception as e:
        print(f"Error when making plots: {e}")


if __name__ == '__main__':
    input_file_path = '../artifacts/nba_draft_1980_2010_cleaned_grouped.csv'
    analyze_draft_groups(input_file_path)