# scrape_visualize
A project to scrape data of interest from openly available sites for analysis anc visualization. 

Sequence of process:
  1. v1_1_twitterscrape.py runs the Twitter query with given parameters and saves the results in a jsonl file. 
  2. 1_spacy_testing.py reads the jsonl file into a datrframe, then parses through the content column of the dataframe using spacy to identify entitiies. The detected entities are being matched with city coordinates provided by values storess in a dictionary in cities_coords.py. The results are added to the existing dataframe as new columns and then saved in a new json file. 
