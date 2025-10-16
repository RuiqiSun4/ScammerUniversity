# Statistical Insights into Draft Efficiency in the NBA
### "Are top-paid NBA rookies performing well?"

## Data  
In this project, we used a basketball reference website(`https://www.basketball-reference.com/draft/`). The NBA draft records spans from 1980 to 2010 and serves as the foundation for evaluating draft efficiency and player performance.   
Since only the top 60 draft picks per year are considered meaningful, our analysis focuses exclusively on the performance of players selected within ranks 1 to 60 for each draft year. Even players with performance metrics of zero were included to ensure a realistic and comprehensive evaluation.

### Data Collection Method
 This dataset was compiled by scraping NBA draft records from 1980 to 2010, with each year's data extracted from a dedicated webpage. 

### Limitation of Data

### Extension of Data

### Glossary
The key metrics used to evaluate draft efficiency are as follows:  

Pk: Draft rank    
WS: Win Shares (An estimate of the number of wins contributed by a player)  
PTS: Points per game  
Years: Seasons the player has appeared in the NBA  
MP: Minutes played per game

For detailed explanations of the key terms used to assess draft efficiency, please refer to `reference/nba_stat_glossary.csv`.

### Descriptive Summary

## Draft Efficiency Analysis  

### Win shares and draft rank
If you make a scatter plot between win shares and draft ranks from 1980 to 2010 (number of observations: 1,802), there is a clear negative correlation (-0.4796). The results indicate that players selected at higher draft ranks (lower numerical values) tend to accumulate more career wins, suggesting a meaningful correlation between draft order and performance.
  
![](analysis/results/ws_pick.png) 
  
You can get these results (`analysis/results/ws_pick.png`, `analysis/results/ws_pick.txt`) by rerunning (`analysis/ws_pick.py`).

The negative correlation between draft rank and win share has fluctuated consistently from 1980 to 2010. While the year-by-year correlation graph does not reveal any notable long-term trends, this may suggest that the draft market has operated efficiently over time.  

![](analysis/results/ws_pick_corr_trend.png) 

The strongest negative correlation was observed in 1996, with a correlation coefficient of -0.619 and p-value of 0.000. This indicates that players with higher draft rankings (i.e., lower pick numbers) contributed significantly to team wins that year, and the result is statistically significant. The 1st pick in 1996 was Allen Iverson, followed by Kobe Bryant in 13th pick. Historically, the 1996 draft is considered as one of the successful drafts full of talents in NBA history. 

In contrast, the weakest negative correlation occured in 1986, with a coefficient of -0.265 and p-value of 0.040. This suggests that in 1986, the players that teams invested heavily in failed to deliver strong performances, and at the 1% significance level, there was no statistically meaningful evidence that higher draft picks performed better.

You can get these results (`analysis/results/ws_pick_corr_trend.png`, `ws_pick_corr_by_year.csv`, `ws_pick_regression_1986_1996.txt`, `ws_pick_1996_with_stats.png`, `ws_pick_1986_with_stats.png`) by rerunning (`analysis/ws_pick_yearly.py`, `anlysis/ws_pick_plot_1986_1996.py`).




### (Please add other topics)

## Instruction to Rerun

### Analysis code
Your code will be executed in a Python environment contatining the Standard Library and the packages specified in `requirements.txt`. Install them with `pip install -r requirements.txt`.

### Scrape code
Running the scrape code(`data_scraping/draftpick_scrape.py`) will take about 35 minutes. We have already uploaded the original data(`artifacts/nba_draft_1980_2010.csv`) to the repo.
After scraping, we cleaned the data through `data_scraping/draft_data_clean.py`, which gave 'artifacts/nba_draft_1980_2010_cleaned.csv'.



and grouped the data by draft rank(`data_scraping/draft_data_clean_group.py`).

