import pandas as pd
import requests
from datetime import date, datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class GuardianAPI():
    df = pd.DataFrame(columns = ['source', 'author', 'title', 'description', 'url', 'url_to_image', 'published_on', 
                             'content'])
    
    def __init__(self):
        print("Guardian constructor.")

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
        print("GuardianAPI: Getting the base info...")  
        # Set the default date to return items for
        default_date = date.today() - timedelta(days=7)
        from_date = "&from-date=" + str(default_date)
        # Keywords to search for
        keyword_input = ['Poland', 'Biden']
        # Convert keyword list items to lower case
        keyword_lower = [x.lower() for x in keyword_input]
        # Join keyword list items for api call
        keywords = '%20AND%20'.join(keyword_lower)
        # Set max number of results to be returned   
        number_results = 10 #default is 10

        base_url = "https://content.guardianapis.com/search?q="
        api_key = '&api-key=399bc171-6978-4e1a-8551-c38c0026369c'

        # Set API call url
        guardian_search = base_url + keywords + from_date + api_key

        # Make the API call 
        x = requests.get(guardian_search)
        responses = x.json()
        print("Create the GuardianAPI dataframe")
        articles = responses['response']['results']
        for i in range(len(articles)):
            source = "The Guardian"
            author = "The Guardian editors"
            title = articles[i]['webTitle']
            description = articles[i]['sectionName'],
            url = articles[i]['webUrl'],
            url_to_image = 'None',
            published_on = articles[i]['webPublicationDate'],
            content = 'Follow link - undetermined sentiment'
            dftemp = pd.DataFrame({'source': source, 'author': author, 'title' : title, 'description': description,
                        'url': url, 'url_to_image': url_to_image, 'published_on': published_on, 'content': content })
            df = pd.concat([df, dftemp], ignore_index=True)
        df = df.drop_duplicates(inplace=True)
        print("Getting a sentiment score for the text.....")
        df['SentimentScore'] = df.content.apply(self.sentimentScores)
        df['Compound'] = df.SentimentScore.apply(lambda score_dict: score_dict['compound'])
        run = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')
        print("Saving the dataframe.....")
        df.to_csv(f'temp/news_GuardianAPI_{run}.csv', index=False)
        print("NewsAPI: All done!")
