import re
import requests 
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class newsSoupNBC():
    
    all_tags = []
    parsed = []
    
    def __init__(self):
        print("NBC NewsSoup constructor.")
    
    def getInfo(self):
        print("NBC: Getting the base info...")
        root = "https://www.nbcnews.com"
        exts = ["/news/china", "/news/africa", "/news/asia", "/news/europe", 
                "/world", "/nightly-news", "/politics"]

        for ext in exts:
            website = f'{root}' + ext
            res = requests.get(website)
            soup = BeautifulSoup(res.text, 'lxml')
            headlines_h2 = soup.find_all('h2',{'class':'tease-card__headline tease-card__title tease-card__title--news relative'})
            self.all_tags.append(headlines_h2)
        return self.all_tags
    
    def cleanAll_Tags(self):
        print("NBC: Parsing for links and headlines..")
        step1 = []
        for allts in self.all_tags:
            for alls in allts:
                step1.append(alls)
        step2 = str(step1)
        step3 = step2.split("<h2 ")
        step3[1][89:334]
        step4 = []
        for i in step3:
            try:
                step4.append(i[89:])
            except:
                pass
        
        for i in step4:
            try:
                self.parsed.append(i.split('tease-card__headline">'))
            except:
                pass
        
        del self.parsed[0]
        return self.parsed
    
    def strippedText(self, text):
        stripped = re.sub("[<@*&?].*[,@*&?]", "", text)
        return stripped
    
    def parseSiteForText(self, link):
        try:
            text = str(link)
            website = requests.get(text)
            soup = BeautifulSoup(website.content, 'html.parser')
            return soup.text
        except:
            return "No connection"
    
    def cleanFullText(self, text):
        text1 = re.sub(r"IE 11 is not supported. For an optimal experience visit our site on another browser.SKIP TO CONTENTNBC News LogoMeet the PressPoliticsU.S. NewsBusinessTechWorldHealthCulture & trendsNBC News TiplineShare & Save —SearchSearchProfile My NewsSign Out Sign InCreate your free profileSectionsCoronavirusU.S. NewsPoliticsWorldLocalBusinessHealthInvestigationsCulture & TrendsScienceSportsTech & MediaVideo FeaturesPhotosWeatherSelectAsian AmericaNBCBLKNBC LatinoNBC OUTtvTodayNightly NewsMSNBCMeet the PressDatelineFeaturedNBC News NowBetterNightly FilmsStay TunedSpecial FeaturesNewslettersPodcastsListen NowMore From NBCCNBCNBC.COMNBCU AcademyNBC LearnPeacockNEXT STEPS FOR VETSParent ToolkitNBC News Site MapHelpFollow NBC NewsSearchSearchFacebookTwitterEmailSMSPrintWhatsappRedditPocketFlipboardPinterestLinkedinMy NewsManage ProfileEmail PreferencesSign Out", " ", text)
        text2 = re.sub(r".AboutContactHelpCareersAd ChoicesPrivacy PolicyDo Not Sell My Personal InformationCA NoticeTerms of ServiceNBC News SitemapAdvertiseSelect ShoppingSelect Personal Finance© 2023 NBC UNIVERSALNBC News LogoMSNBC LogoToday Logo", " ", text1)
        return text2
    
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
        print("NBC: Creating the dataframe...")
        links = []
        headlines = []

        for i in self.parsed:
            links.append(i[0][:-15])
            try:
                headlines.append(i[1])
            except:
                headlines.append("Broken and unreadable")
        
        d = {'Links': links, 'Headlines': headlines}
        df = pd.DataFrame(d)
        print("Assigning Item ID numbers....")
        df['ItemID'] = df.Headlines.apply(self.setID)
        df.Headlines = df.Headlines.apply(self.strippedText)
        print("Following links for full text....")
        df['FullText'] = df.Links.apply(self.parseSiteForText)
        df['FullText'] = df.FullText.apply(self.cleanFullText)
        print("Getting a sentiment score for the text.....")
        df['SentimentScore'] = df.FullText.apply(self.sentimentScores)
        df['Compound'] = df.SentimentScore.apply(lambda score_dict: score_dict['compound'])
        run = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')
        print("Saving the dataframe.....")
        df.to_csv(f'temp/news_NBC_{run}.csv', index=False)
        print("NBC: All done!")




        
