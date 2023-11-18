# MoodyWorld
A project to ingest data of interest from news APIs for analysis anc visualization. 

The code in the files creates a website interface to initiate API calls from various news outets. Once the information requested is returned into a dataframe, it is scrubbed to remove redunadant spacing, lettering and other noise. Additionally, a sentiment score is assigned to the full text using Vader Sentiment Analyser. 
The text is then further processed using the spaCy library to tokenize the text, find the most frquent words in the text, as well as find location entities. This is to provide a location for the marker to be placed on the results map. Location coordinates are provided through a maps API. 
Based on the sentiment score, the markers appear in a 10 step gradient of colors ranging from red to green. 

## Requirements
Get started by cloning the project repository from GitHub.

Once the project is cloned, you also need to install the dependencies. Use the command "pip install -r requirements.txt" from the root folder of the project.


Additionally, spacy will need the en-core-web-lg language model to do its job, which can be found [here](https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.5.0/en_core_web_lg-3.5.0-py3-none-any.whl).
