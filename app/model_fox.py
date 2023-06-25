import re
import requests 
import pandas as pd
import spacy
from bs4 import BeautifulSoup
from cleantext import clean
from datetime import datetime
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class newsSoupFox():
    
    all_tags_h2 = []
    all_tags_h4 = []
    parsed_h2 = []
    parsed_h4 = []
    
    def __init__(self):
        print("FOX NewsSoup constructor.")
        
    
    def getInfoh2(self):
        print("FOX: Getting the h2 info...")
        root = "https://www.foxnews.com"
        exts = ["/us", "/opinion", "/world", "/politics", "/media", "/entertainment", "/category/us/terror", 
               "/category/world/united-nations", "/category/world/conflicts", "/category/world/terrorism", 
               "/category/world/disasters", ]
        
        for ext in exts:
            website = f'{root}' + ext
            res = requests.get(website)
            soup = BeautifulSoup(res.text, 'lxml')
            headlines = soup.find_all('h2',{'class':'title'})
            self.all_tags_h2.append(headlines)
        return self.all_tags_h2
    
    def getInfoh4(self):
        print("FOX: Getting the h4 info...")
        root = "https://www.foxnews.com"
        exts = ["/us", "/opinion", "/world", "/politics", "/media", "/entertainment", "/category/us/terror", 
               "/category/world/united-nations", "/category/world/conflicts", "/category/world/terrorism", 
               "/category/world/disasters", ]
        for ext in exts:
            website = f'{root}' + ext
            res = requests.get(website)
            soup = BeautifulSoup(res.text, 'lxml')
            headlines = soup.find_all('h4',{'class':'title'})
            self.all_tags_h4.append(str(headlines))            
        return self.all_tags_h4
    
    def cleanAll_Tags_h2(self):
        print("FOX: Parsing for h2 links and headlines..")
        step1 = []
        for allts in self.all_tags_h2:
            for alls in allts:
                step1.append(alls)
        step2 = str(step1)
        step3 = step2.split("<h2 ")
        step4 = step3[1:]
        step5 = []
        for i in step4:
            step5.append(re.sub('class="title"><a href="', 'https://www.foxnews.com', i))

        step6 = []
        for j in step5:
            step6.append(re.sub('</a></h2>, ', '', j))

        for k in step6:
            self.parsed_h2.append(k.split('">'))
            
        return self.parsed_h2
    
    def cleanAll_Tags_h4(self):
        print("FOX: Parsing for h4 links and headlines..")
        step1 = []
        for allts in self.all_tags_h4:
            step1.append(allts)
        step2 = str(step1)
        step3 = step2.split("<h4 ")

        step4 = step3[1:]

        step5 = []
        for i in step4:
            step5.append(re.sub('class="title"><a href="', 'https://www.foxnews.com', i))

        step6 = []
        for j in step5:
            step6.append(re.sub('</a></h4>, ', '', j))

        for k in step6:
            self.parsed_h4.append(k.split('">'))

        return self.parsed_h4
    
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
    
    Token.set_extension("ignore", default=False, force=True)

    #load a model and create nlp object
    nlp = spacy.blank("en")
    matcher = PhraseMatcher(nlp.vocab)

    def set_ignore(self, matcher, doc, id, matches):
        for _, start, end in matches:
            for tok in doc[start:end]:
                tok._.ignore = True

    def cleanFullText(self, text):
        terms = ["Fox News",
        "MediaFox BusinessFox ",
        "NationFox News AudioFox WeatherOutkickBooks ",
        "Around the WorldAdvertise With UsMedia RelationsCorporate InformationCompliance",
        "U.S.PoliticsWorldOpinionMediaEntertainmentSportsLifestyleVideo More Expand",
         "Collapse search Login Watch TV Menu",
         "U.S. CrimeMilitaryEducationTerrorImmigrationEconomyPersonal",
         "FreedomsFox News InvestigatesWorld U.N.ConflictsTerrorismDisastersGlobal",
         "EconomyEnvironmentReligionScandalsOpinion",
         "Politics ExecutiveSenateHouseJudiciaryForeign PolicyPollsElectionsEntertainment",
         "Celebrity NewsMoviesTV NewsMusic NewsStyle NewsEntertainment VideoBusiness Personal",
         "FinanceEconomyMarketsWatchlistLifestyleReal EstateTechLifestyle",
         "Food + DrinkCars + TrucksTravel + OutdoorsHouse + HomeFitness + Well-beingStyle + BeautyFamilyFaithScience",
         "ArchaeologyAir & SpacePlanet EarthWild NatureNatural ScienceDinosaursTech",
         "SecurityInnovationDronesComputersVideo GamesMilitary TechHealth",
         "CoronavirusHealthy LivingMedical ResearchMental HealthCancerHeart HealthChildren's HealthTV",
         "ShowsPersonalitiesWatch LiveFull EpisodesShow ClipsNews ClipsAbout Contact UsCareersFox",
         "Fox BusinessFox WeatherFox NationFox News ShopFox News GoFox News RadioOutkickNewslettersPodcastsApps",
         "Products New Terms of Use New Privacy Policy Your Privacy Choices",
         "Closed Captioning Policy Help Contact Us",
         "This material may not be published, broadcast, rewritten,",
         "or redistributed. ©2023 FOX News Network, LLC. All rights reserved.",
         "Quotes displayed in real-time or delayed by at least 15 minutes.",
         "Market data provided by Factset. Powered and implemented by FactSet Digital Solutions.",
         "Legal Statement. Mutual Fund and ETF data provided by Refinitiv Lipper.",
         "Facebook Twitter Instagram RSS Email",
        "(Zach Wilkinson/Moscow-Pullman Daily News via Pool)", 
         "(Derek Shook for Digital)",
         "(Instagram @xanakernodle / @maddiemogen / @kayleegoncalves)", 
         "CLICK HERE TO GET THE FOX NEWS APP",
         "Story tips can be sent to michael.ruiz@fox.com and on Twitter: @mikerreports",
         "Facebook Twitter Flipboard Comments Print Email  close",
         "Get all the stories you need-to-know from the most powerful name in news delivered first thing every morning to your inbox Arrives Weekdays  Subscribe  Subscribed       Subscribe  You've successfully subscribed to this newsletter!",
        ]
        # create patterns variable
        patterns = [self.nlp.make_doc(text) for text in terms]
        self.matcher.add("TerminologyList", patterns, on_match=self.set_ignore)
        
        doc = self.nlp(text)
        # this will run the callback
        self.matcher(doc)

        toks = [tok.text + tok.whitespace_ for tok in doc if not tok._.ignore]
        text_n = "".join(toks)
        text_f = text_n.replace('\n', ' ').replace('\r', '') 
        return text_f
    
    def sentimentScores(self, text):
        # Create sentiment intensity analyzer object
        sid_obj = SentimentIntensityAnalyzer()
        # Polarity
        sentiment_dict = sid_obj.polarity_scores(text)
        # Insert scores to dataframe
        return sentiment_dict
    
    def setID(self, text):
        counter = 100
        date_stamp = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')
        applied_ID = date_stamp + str(counter)
        counter += 1
        return applied_ID
    
    def createDataFrame(self):
        print("FOX: Creating the dataframe...")
        self.parsed_h2.extend(self.parsed_h4)
        links = []
        headlines = []
        
        for i in self.parsed_h2:
            links.append(i[0])
            headlines.append(i[1])

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
        df.to_csv(f'temp/news_FOX_{run}.csv', index=False)
        print("FOX: All done!")