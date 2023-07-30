import glob
import locationtagger
import nltk
import random
import pandas as pd
import requests
import spacy
import urllib.parse

from collections import Counter
from datetime import datetime, date, timedelta
#from geopy.geocoders import Nominatim
from newsapi import NewsApiClient
from requests.structures import CaseInsensitiveDict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# essential entity models downloads; should only need once during first time use
#nltk.downloader.download('maxent_ne_chunker')
#nltk.downloader.download('words')
#nltk.downloader.download('treebank')
#nltk.downloader.download('maxent_treebank_pos_tagger')
#nltk.downloader.download('punkt')
#nltk.download('averaged_perceptron_tagger')

class ProcessingFrame():
    nlp = spacy.load("en_core_web_lg")
    nltk.downloader.download('maxent_ne_chunker')
    nltk.downloader.download('words')
    nltk.downloader.download('treebank')
    nltk.downloader.download('maxent_treebank_pos_tagger')
    nltk.downloader.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    frame = pd.DataFrame()

    def readingFrames(self):
        print("Reading all the frames.")
        file_list = glob.glob("temp/*.csv")

        files = []

        for filename in file_list:
            df = pd.read_csv(filename)
            files.append(df)

        self.frame = pd.concat(files, axis=0, ignore_index=True)
        return self.frame

    def getLocationNames(self, text):
        # extracting entities.
        place_entity = locationtagger.find_locations(text = text)
        locationNames = {"Countries": place_entity.countries, "States": place_entity.regions, 
                         "Cities": place_entity.cities}        
        return locationNames

    def getCoordinates(self, text):
        if len(text['Cities']) >= 1:
            place = text['Cities']
        elif len(text['States']) >= 1:
            place = text['States']
        elif len(text['Countries']) >= 1:
            place = text['Countries']
            
        try:
            #1loc = place[0]
            url = "https://api.geoapify.com/v1/geocode/search?text=" + place[0] + "&apiKey=43a11a6b22cd4143a539fea67a98e798"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            resp = requests.get(url, headers=headers)
            data = resp.json()
            coordinates = data['features'][0]['properties']['lat'], data['features'][0]['properties']['lon']
            return coordinates
        except:
            return "No Location found."

    def getLatitude(self, text):
        return text[0]

    def getLongitude(self, text):
        return text[1]

    def offSet(self, text):
        try:
            return text + random.uniform(-0.5, 0.5)
        except:
            pass

    def getFrequentWords(self, text):
        doc = self.nlp(text)
        # all tokens that arent stop words or punctuations
        words = [token.text
                for token in doc
                if not token.is_stop and not token.is_punct]

        # noun tokens that arent stop words or punctuations
        nouns = [token.text
                for token in doc
                if (not token.is_stop and
                    not token.is_punct and
                    token.pos_ == "NOUN")]

        # five most common tokens
        word_freq = Counter(words)
        common_words = word_freq.most_common(5)

        # five most common noun tokens
        noun_freq = Counter(nouns)
        common_nouns = noun_freq.most_common(5)
        
        return common_words
    
    def getColors(self, text):
        if (text >= -1.0) & (text < -0.8):
            return "#056607"
        elif (text >= -0.8) & (text < -0.6):
            return "#2d6900"
        elif (text >= -0.6) & (text < -0.4):
            return "#476a00"
        elif (text >= -0.4) & (text < 0.2):
            return "#606a00"
        elif (text >= 0.2) & (text < 0.0):
            return "#7a6800"
        elif (text >= 0.2) & (text < 0.4):
            return "#946400"
        elif (text >= 0.4) & (text < 0.6):
            return "#ae5c00"
        elif (text >= 0.6) & (text < 0.8):
            return "#c94f00"
        elif (text >= 0.6) & (text < 0.8):
            return "#e33b00"
        else:
            return "#fc0c0c"
    
    def applyToFrame(self):
        print("Creating popup column text.")
        self.frame["Popup"] = self.frame.title + "\n" + self.frame.url
        print("Assigning location names.")
        self.frame['LocationNames'] = self.frame.content.apply(self.getLocationNames)
        print("Assigning coordinates when possible.")
        self.frame['Coordinates'] = self.frame.LocationNames.apply(self.getCoordinates)
        self.frame['Latitude'] = self.frame.Coordinates.apply(self.getLatitude)
        self.frame.Latitude = pd.to_numeric(self.frame.Latitude, errors='coerce')
        self.frame.Latitude = self.frame.Latitude.apply(self.offSet)
        self.frame['Longitude'] = self.frame.Coordinates.apply(self.getLongitude)
        self.frame.Longitude = pd.to_numeric(self.frame.Longitude, errors='coerce')
        self.frame.Longitude = self.frame.Longitude.apply(self.offSet)
        print("Getting frequent word counts.")
        self.frame['FrequentWords'] = self.frame.content.apply(self.getFrequentWords)
        print("Assigning colors for markers.")
        self.frame['Compound'] = self.frame['Compound'].astype("Float64")
        self.frame['Colors'] = self.frame.Compound.apply(self.getColors)
        self.frame.to_csv("app/static/processed_frame.csv", index=False)
        print('Results were saved. Query processing is complete')