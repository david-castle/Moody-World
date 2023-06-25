import re
import requests 
import pandas as pd
import spacy
from bs4 import BeautifulSoup
from datetime import datetime
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class newsSoupGuardian():
    
    all_tags = []
    parsed = []
    
    def __init__(self):
        print("Guardian: The Guardian NewsSoup constructor.")
        
    
    def getInfo(self):
        print("Guardian: Getting the tags info...")
        root = "https://www.theguardian.com"
        exts = ["/international", "/opinion"]
        
        for ext in exts:
            website = f'{root}' + ext
            res = requests.get(website)
            soup = BeautifulSoup(res.text, 'lxml')
            headlines = soup.find_all('h3',{'class':'fc-item__title'})
            self.all_tags.append(headlines)
        return self.all_tags
    
    def cleanAll_Tags(self):
        print("Guardian: Parsing for links and headlines..")
        step1 = []
        for allts in self.all_tags:
            for alls in allts:
                step1.append(alls)
        step2 = str(step1)
        step3 = step2.split("<h3 ")
        step4 = step3[1:]
        
        #step5 = []
        for i in step4:
            self.parsed.append(i.split('<span class="js-headline-text">'))
        
        return self.parsed
    
    def strippedText(self, text):
        stripped = re.sub("[<@*&?].*[,@*&?]", "", text)
        return stripped
    
    def strippedLinks(self, text):
        s1 = text.split('href="', 1)[1]
        s2 = s1.split('">', 1)[0]
        stripped = s2.lstrip()
        return stripped
    
    def parseSiteForText(self, link):
        try: 
            text = str(link)
            website = requests.get(text)
            soup = BeautifulSoup(website.content, 'html.parser')
            return soup.text
        except:
            return "No connection"

    #load a model and create nlp object
    nlp = spacy.blank("en")
    matcher = PhraseMatcher(nlp.vocab)

    def set_ignore(self, matcher, doc, id, matches):
        for _, start, end in matches:
            for tok in doc[start:end]:
                tok._.ignore = True

    def cleanFullText(self, text):
        try:
            text1 = text.split('appGuardian', 1)[1]
            terms = ["LicensingThe Guardian", 
                     "appVideoPodcastsPicturesInside", 
                     "the GuardianGuardian", 
                     "WeeklyCrosswordsWordiplyCorrectionsFacebookTwitterSearch", 
                     "jobsDigital ArchiveGuardian Puzzles appGuardian",
                     "viewColumnistsLettersOpinion videosCartoons",
            ]
            # create patterns variable
            patterns = [self.nlp.make_doc(text) for text in terms]
            self.matcher.add("TerminologyList", patterns, on_match=self.set_ignore)
            
            doc = self.nlp(text1)
            # this will run the callback
            self.matcher(doc)

            toks = [tok.text + tok.whitespace_ for tok in doc if not tok._.ignore]
            text_n = "".join(toks)
            text_f = text_n.replace('\n', ' ').replace('\r', '') 
            return text_f
        except:
            return "No text available"
    
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
        print("Guardian: Creating the dataframe...")
        links = []
        headlines = []
        
        for i in self.parsed:
            links.append(i[0])
            headlines.append(i[1])

        d = {'Links': links, 'Headlines': headlines}
        
        df = pd.DataFrame(d)
        print("Assigning Item ID numbers....")
        df['ItemID'] = df.Headlines.apply(self.setID)
        df.Headlines = df.Headlines.apply(self.strippedText)
        df.Links = df.Links.apply(self.strippedLinks)
        print("Following links for full text....")
        df['FullText'] = df.Links.apply(self.parseSiteForText)
        df.FullText = df.FullText.apply(self.cleanFullText)
        print("Getting a sentiment score for the text.....")
        df['SentimentScore'] = df.FullText.apply(self.sentimentScores)
        df['Compound'] = df.SentimentScore.apply(lambda score_dict: score_dict['compound'])
        run = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')
        print("Saving the dataframe.....")
        df.to_csv(f'temp/news_Guardian_{run}.csv', index=False)
        print("Guardian: All done!")