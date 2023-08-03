import json
import pandas as pd
import requests
import urllib
from datetime import datetime, date, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class GNewsApi():
    def __init__(self):
        print("GNewsAPI constructor.")

    def getInfo(self, term):
        print("GNewsAPI: Getting the base info...")  
        # Init
        file1 = open("temp/searchterms.txt","r+")
        term = list[str(file1.read())]
        base_url = "https://gnews.io/api/v4/search?q="
        keywords = self.convertKeyWords(term)
        language = "&lang=en"
        max_return = "&max=10" #default for free plan is 10
        #from_date = "&from-date=" + str(default_date)
        apikey = "&apikey=09fc1663f2898e244bd33b4cc76c254c"
        url = base_url + keywords + language + max_return + apikey
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            all_articles = data["articles"]
        return all_articles

    def convertKeyWords(self, wordList):
        wordLower = [x.lower() for x in wordList]
        if len(wordLower) > 1:
            keywords = '%20AND%20'.join(wordLower)
            return keywords
        else:
            return str(wordLower[0])

    def sentimentScores(self, text):
        # Create sentiment intensity analyzer object
        sid_obj = SentimentIntensityAnalyzer()
        # Polarity
        sentiment_dict = sid_obj.polarity_scores(text)
        # Insert scores to dataframe
        return sentiment_dict
    
    def sentimentOfText(self, scores):
        if scores['compound'] >= 0.05:
            return 'Positive'
        elif scores['compound'] <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    def setID(self, text):
        counter = 100
        date_stamp = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')
        applied_ID = date_stamp + str(counter)
        counter += 1
        return applied_ID

    def createDataFrame(self, term):
        df = pd.DataFrame(columns = ['source', 'author', 'title', 'description', 'url', 
                                 'url_to_image', 'published_on', 'content'])
        dictionary = self.getInfo(term)
        articles = dictionary['articles']
        print("Create the NewsAPI dataframe")
        for i in range(len(articles)):
            source = articles[i]['source']['name']
            author = "Author not available"
            title = articles[i]['title']
            description = articles[i]['description']
            url = articles[i]['url']
            url_to_image = articles[i]['image']
            published_on = articles[i]['publishedAt']
            content = articles[i]['content']
            dftemp = pd.DataFrame({'source': source, 'author': author, 'title' : title, 'description': description,
                        'url': url, 'url_to_image': url_to_image, 'published_on': published_on, 'content': content }, index=[i])
            df = pd.concat([df, dftemp], ignore_index=True)
            df.drop(df[df['source']== 'Google News'].index, inplace = True)
        return df
    
    def ScoreAndSave(self, term):
        df_final = self.createDataFrame(term)
        print("Getting a sentiment score for the text.....")
        df_final['SentimentScore'] = df_final.content.apply(self.sentimentScores)
        df_final['Compound'] = df_final.SentimentScore.apply(lambda score_dict: score_dict['compound'])
        run = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')
        print("Saving the dataframe.....")
        df_final.to_csv(f'temp/news_NewsAPI_{run}.csv', index=False)
        print("NewsAPI: All done!")

