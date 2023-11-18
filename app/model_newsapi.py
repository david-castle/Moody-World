from datetime import datetime, date, timedelta
from newsapi import NewsApiClient
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class NewsApi():
    def __init__(self):
        print("NewsAPI instantiated.")
    
    def getInfo(self):
        print("NewsAPI: Gett the base info...")  
        # Init
        try:
            file1 = open("temp/Anysearchterms.txt","r+")
            term = "".join(file1.readline())
            if len(term) < 1:
                raise Exception("No words given.")
        except:
            file2 = open("temp/AllSearchterms.txt", "r+")
            term = "".join(file2.readline()).split(', ')
            print("all: ", term)
        print(term)
        #keywords = self.convertKeyWords(term)
        #print(keywords)
        newsapi = NewsApiClient(api_key='GET_AN_API_KEY')
        to_date = date.today()
        from_date = to_date - timedelta(days=28)
        all_articles = newsapi.get_everything(q=str(term),
                                            #sources='bbc-news,the-verge',
                                            #domains='bbc.co.uk,techcrunch.com',
                                            from_param=str(from_date),
                                            to=str(to_date),
                                            language='en',
                                            sort_by='relevancy')
                                            #page=2)
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
        dictionary = self.getInfo()
        articles = dictionary['articles']
        print("Create the NewsAPI dataframe")
        for i in range(len(articles)):
            source = articles[i]['source']['name']
            author = articles[i]['author']
            title = articles[i]['title']
            description = articles[i]['description']
            url = articles[i]['url']
            url_to_image = articles[i]['urlToImage']
            published_on = articles[i]['publishedAt']
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
        df_final.to_csv(f'temp/news_NewsAPI_{run}.csv', index=False)
        print("NewsAPI: All done!")
