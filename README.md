# Statistical Insights into Draft Efficiency in the NBA

## Data  
In this project, we used Basketball Reference website(`https://www.basketball-reference.com/draft/`). The NBA draft records spans from 1980 to 2010 and serves as the foundation for evaluating draft efficiency and player performance. Since only the top 60 draft picks per year are considered meaningful, our analysis focuses exclusively on the performance of players selected within ranks 1 to 60 for each draft year. Even players with performance metrics of zero were included to ensure a realistic and comprehensive evaluation.

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

### Win Shares and draft rank

### (Please add other topics)

## Instruction to Rerun

### Analysis code
Your code will be executed in a Python environment contatining the Standard Library and the packages specified in `requirements.txt`. Install them with `pip install -r requirements.txt`.

### Scrape code
Running the scrape code(`data_scraping/draftpick_scrape.py`) will take about 35 minutes. We have already uploaded the original data(`artifacts/nba_draft_1980_2010.csv`) to Github.  
After scraping, we cleaned the data (`data_scraping/draft_data_clean.py`) and grouped the data(`data_scraping/draft_data_clean_group.py`).

