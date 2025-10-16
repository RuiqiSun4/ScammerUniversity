# Statistical Insights into Draft Efficiency in the NBA

## Data  
In this project, we used Basketball Reference website(`https://www.basketball-reference.com/draft/`). 
The key metrics used to evaluate draft efficiency are as follows:  

- Pk: Draft rank  

- WS: Win Shares (An estimate of the number of wins contributed by a player)  


- PTS: Points per game  

- Years: Seasons the player has appeared in the NBA

- MP: Minutes played per game

For detailed explanations of the key terms used to assess draft efficiency, please refer to `reference/nba_stat_glossary.csv`.

### Data Collection Method
 This dataset was compiled by scraping NBA draft records from 1980 to 2010, with each year's data extracted from a dedicated webpage. The resulting dataset spans 31 years of draft history and serves as the foundation for evaluating draft efficiency and player performance.

### Limitation of Data

### Extension of Data

### Descriptive Summary

## Draft Efficiency Analysis  

## Instruction to Rerun

### Analysis code
Your code will be executed in a Python environment contatining the Standard Library and the packages specified in `requirements.txt`. Install them with `pip install -r requirements.txt`.

### Scrape code
Running the scrape code(`data_scraping/draftpick_scrape.py`) will take about 35 minutes. We have already uploaded the original data(`artifacts/nba_draft_1980_2010.csv`) to Github.


