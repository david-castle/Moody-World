from datetime import datetime
from newsapi import NewsApiClient
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class NewsApi():
    df = pd.DataFrame(columns = ['source', 'author', 'title', 'description', 'url', 
                                 'url_to_image', 'published_on', 'content'])

    def __init__(self):
        print("NewsAPI constructor.")
    
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
        print("NewsAPI: Getting the base info...")  
        # Init
        newsapi = NewsApiClient(api_key='87edec59c3ba4e03939a5ad21f02c52a')
        all_articles = newsapi.get_everything(q='germany',
                                    from_param='2023-06-23',
                                    to='2023-07-20',
                                    language='en',
                                    sort_by='relevancy')
        print("Create the NewsAPI dataframe")
        articles = all_articles['articles']
        for i in range(len(articles)):
            source = articles[i]['source']['name']
            author = articles[i]['author']
            title = articles[i]['title']
            description = articles[i]['description'],
            url = articles[i]['url'],
            url_to_image = articles[i]['urlToImage'],
            published_on = articles[i]['publishedAt'],
            content = articles[i]['content']
            dftemp = pd.DataFrame({'source': source, 'author': author, 'title' : title, 'description': description,
                        'url': url, 'url_to_image': url_to_image, 'published_on': published_on, 'content': content })
            df = pd.concat([self.df, dftemp], ignore_index=True)
        print("Getting a sentiment score for the text.....")
        df['SentimentScore'] = df.content.apply(self.sentimentScores)
        df['Compound'] = df.SentimentScore.apply(lambda score_dict: score_dict['compound'])
        run = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')
        print("Saving the dataframe.....")
        df.to_csv(f'temp/news_NewsAPI_{run}.csv', index=False)
        print("NewsAPI: All done!")