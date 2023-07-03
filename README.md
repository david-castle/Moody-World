# MoodyWorld
A project to scrape data of interest from openly available sites for analysis anc visualization. 

The code in the files creates a website interface to initiate scraping news articles from NBC, Fox and The Guardian news outets. Since no APIs are being used, the code first selects all tagged headlines and links of interest on the main site, as well as select subsites of the different outlets. After taking the links and headlines and putting them into a pandas dataframe, the code then follows the links to get the article text. 
Once the text is returned into dataframe, it is scrubbed to remove redunadant spacing, lettering and other noise. Additionally, a sentiment score is assigned to the full text using Vader Sentiment Analyser. 
The text is then further processed using the spaCy library to tokenize the text, find the most frquent words in the text, as well as find location entities. This is to provide a location for the marker to be placed on the results map. Location coordinates are being pulled online. 
Based on the sentiment score, the markers appear in a 10 step gradient of colors ranging from red to green. 

## Requirements
While the requirements file shows all necessary packages for this project, most will be automatically installed when installing the following core packages using pip:
  pip install beautifulsoup4
  pip install Flask
  pip install Flask-WTF
  pip install glob2
  pip install pandas
  pip install requests
  pip install spacy
  pip install vader-sentiment


Additionally, spacy will need a language model to do its job, which can be found here:
  en-core-web-lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.5.0/en_core_web_lg-3.5.0-py3-none-any.whl
