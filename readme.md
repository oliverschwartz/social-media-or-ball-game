# Ball Game or Social Media Game?
## A predictive engine for the NBA All-Star vote
### Model inputs & outputs: x -> [Network importance scores, Standard & Advanced statistics], y -> [All-Star fan vote]

### Directories: 
- allstar-votes:
	- contains a series of html files pulled programmatically from basketball-reference.com
	- parse.py, parse.sh, players-parse.py, usernames-and-handles.py: scripts to process all the html and associate entries for each player with a username
	- allstar-votes/votes: collection of player names and the number of fan votes receieved for a given season
- ig:
	- series of csvs pulled from Instagram containing information like who a user follows, who follows them etc.
	- ig/processed: the above, but processed (removed all redundant information)
	- ig/scripts: the core logic for this project, including PageRank.ipynb which processes all follower information and generates importance metrics
	- ig/scripts/count: logic for mimicking a browser and obtaining a follower count for each player (also an input to the model)
- kaggle:
	- logic for making and running the learning model
	- contains raw statistics (basic and advanced)
	- kaggle/gs: logic for scraping and obtaining the missing "GS" (games started) statistic from bbref.com
- env: virtual environment

