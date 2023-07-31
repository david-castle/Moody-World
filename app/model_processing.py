import geonamescache
import glob
import locationtagger
import nltk
import os
import random
import pandas as pd
import requests
import spacy

from collections import Counter
from requests.structures import CaseInsensitiveDict

# essential entity models downloads; should only need once during first time use
#nltk.downloader.download('maxent_ne_chunker')
#nltk.downloader.download('words')
#nltk.downloader.download('treebank')
#nltk.downloader.download('maxent_treebank_pos_tagger')
#nltk.downloader.download('punkt')
#nltk.download('averaged_perceptron_tagger')

class ProcessingFrame():
    gc = geonamescache.GeonamesCache()
    nlp = spacy.load("en_core_web_lg")
    nltk.downloader.download('maxent_ne_chunker')
    nltk.downloader.download('words')
    nltk.downloader.download('treebank')
    nltk.downloader.download('maxent_treebank_pos_tagger')
    nltk.downloader.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    frame = pd.DataFrame()

    countries_list = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 
                  'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 
                  'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 
                  'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 
                  'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 
                  'Bonaire, Saint Eustatius and Saba ', 'Bosnia and Herzegovina', 'Botswana', 
                  'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 
                  'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 
                  'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 
                  'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 
                  'Cocos Islands', 'Colombia', 'Comoros', 'Cook Islands', 'Costa Rica', 
                  'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czechia', 
                  'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 
                  'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 
                  'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland Islands', 
                  'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 
                  'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 
                  'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 
                  'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 
                  'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Honduras', 'Hong Kong', 
                  'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 
                  'Isle of Man', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jersey', 
                  'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 
                  'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 
                  'Lithuania', 'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 
                  'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 
                  'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 
                  'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 
                  'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 
                  'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea', 'North Macedonia', 
                  'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 
                  'Palestinian Territory', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 
                  'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 
                  'Republic of the Congo', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint Barthelemy', 
                  'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 
                  'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 
                  'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Serbia and Montenegro', 
                  'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 
                  'Solomon Islands', 'Somalia', 'South Africa', 
                  'South Georgia and the South Sandwich Islands', 'South Korea', 'South Sudan', 'Spain', 
                  'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen', 'Sweden', 'Switzerland', 
                  'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor Leste', 'Togo', 
                  'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 
                  'Turks and Caicos Islands', 'Tuvalu', 'U.S. Virgin Islands', 'Uganda', 'Ukraine', 
                  'United Arab Emirates', 'United Kingdom', 'United States', 
                  'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican', 
                  'Venezuela', 'Vietnam', 'Wallis and Futuna', 'Western Sahara', 'Yemen', 'Zambia', 
                  'Zimbabwe']

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
        locationNames = {'Countries': ['Peru']}
        place_entity = locationtagger.find_locations(text = text)
        for i in range(len(place_entity.cities)):
            if len(self.gc.get_cities_by_name(str(i))) >= 1:
                locationNames['Cities'] = place_entity.cities
            else:
                pass
        for i in range(len(place_entity.countries)):
            if len(place_entity.countries) > 0:
                for country in place_entity.countries:
                    if country in self.countries_list:
                        locationNames['Countries'] = place_entity.countries   
                    else:
                        pass
        print(locationNames)
        return locationNames

    def getCoordinates(self, text):
        if 'Cities' in text.keys():
            place = text['Cities']
        elif 'Countries' in text.keys():
            place = text['Countries']
        else:
            place = "London"

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
        self.frame['LocationNames'] = self.frame.description.apply(self.getLocationNames)
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
        print("Cleaning up.")
        for folder, subfolders, files in os.walk('temp/'):
            for file in files:
                if file.endswith('.csv') or file.endswith('.txt'):
                    path = os.path.join(folder, file)
                    print('deleted : ', path)
                    os.remove(path)