import json
import pandas as pd
import requests
import urllib
from datetime import datetime, date, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class GNewsApi():
    def __init__(self):
        print("NewsDataAPI instantiated.")

    def getInfo(self):
        print("NewsDataAPI: Get the base info...")  
        # Init
        file1 = open("temp/searchterms.txt","r+")
        term = "".join(file1.readline()).split(', ')
        base_url = "https://newsdata.io/api/1/news?"
        keywords = self.convertKeyWords(term)
        language = "&lang=en"
        max_return = "&max=10" #default for free plan is 10
        #from_date = "&from-date=" + str(default_date)
        apikey = "apikey=pub_27238b44ca178461c62ff294307456683f97f&q="
        url = base_url + apikey + keywords
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

    def createDataFrame(self):
        df = pd.DataFrame(columns = ['source', 'author', 'title', 'description', 'url', 
                                 'url_to_image', 'published_on', 'content'])
        articles = self.getInfo()
        print("Create the NewsDataAPI dataframe")
        for i in range(len(articles)):
            source = articles[i]['source_id']
            author = "Author not available"
            title = articles[i]['title']
            description = articles[i]['description']
            url = articles[i]['link']
            url_to_image = articles[i]['image_url']
            published_on = articles[i]['pubDate']
            content = articles[i]['content']
            dftemp = pd.DataFrame({'source': source, 'author': author, 'title' : title, 'description': description,
                        'url': url, 'url_to_image': url_to_image, 'published_on': published_on, 'content': content }, index=[i])
            df = pd.concat([df, dftemp], ignore_index=True)
            df.drop(df[df['source']== 'Google News'].index, inplace = True)
        return df
    
    def ScoreAndSave(self):
        df_final = self.createDataFrame()
        print("Get a sentiment score for the text.....")
        df_final['SentimentScore'] = df_final.content.apply(self.sentimentScores)
        df_final['Compound'] = df_final.SentimentScore.apply(lambda score_dict: score_dict['compound'])
        run = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')
        print("Save the dataframe.....")
        df_final.to_csv(f'temp/news_NewsDataAPI_{run}.csv', index=False)
        print("NewsDataAPI: All done!")

