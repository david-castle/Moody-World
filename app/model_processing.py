import geonamescache
import glob
import locationtagger
import nltk
import os
import random
import re
import pandas as pd
import requests
import spacy

from app import model_call
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
    """if os.path.exists('/home/myname/nltk_data'):
        pass
    else:
        nltk.downloader.download('maxent_ne_chunker')
        nltk.downloader.download('words')
        nltk.downloader.download('treebank')
        nltk.downloader.download('maxent_treebank_pos_tagger')
        nltk.downloader.download('punkt')
        nltk.download('averaged_perceptron_tagger')"""
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
    
    country_adjectives = {'Afghan':'Afghanistan', 'Algerian':'Algeria', 'Angolan':'Angola', 'Argentine':'Argentina',
                            'Austrian':'Austria', 'Australian':'Australia', 'Bangladeshi':'Bangladesh',
                            'Belarusian':'Belarus', 'Belgian':'Belgium', 'Bolivian':'Bolivia', 'Bosnian':'Bosnia', 
                            'Herzegovinian': 'Herzegovina', 'Brazilian':'Brazil', 'British':'Britain', 'Bulgarian':'Bulgaria',
                            'Cambodian':'Cambodia', 'Cameroonian':'Cameroon', 'Canadian':'Canada', 
                            'Central African':'Central African Republic', 'Chadian':'Chad', 'Chinese':'China',
                            'Colombian':'Colombia', 'Costa Rican':'Costa Rica', 'Croatian':'Croatia', 'Czech':'the Czech Republic',
                            'Congolese':'Democratic Republic of the Congo', 'Danish':'Denmark', 'Ecuadorian':'Ecuador',
                            'Egyptian':'Egypt', 'Salvadoran':'El Salvador', 'English':'England', 'Estonian':'Estonia',
                            'Ethiopian':'Ethiopia', 'Finnish':'Finland', 'French':'France', 'German':'Germany',
                            'Ghanaian':'Ghana', 'Greek':'Greece', 'Guatemalan':'Guatemala', 'Dutch':'Holland',
                            'Honduran':'Honduras', 'Hungarian':'Hungary', 'Icelandic':'Iceland', 'Indian':'India',
                            'Indonesian':'Indonesia', 'Iranian':'Iran', 'Iraqi':'Iraq', 'Irish':'Ireland', 'Israeli':'Israel',
                            'Italian':'Italy', 'Ivorian':'Ivory Coast', 'Jamaican':'Jamaica', 'Japanese':'Japan',
                            'Jordanian':'Jordan', 'Kazakh':'Kazakhstan', 'Kenyan':'Kenya', 'Lao':'Laos', 'Latvian':'Latvia',
                            'Libyan':'Libya', 'Lithuanian':'Lithuania', 'Malagasy':'Madagascar', 'Malaysian':'Malaysia',
                            'Malian':'Mali', 'Mauritanian':'Mauritania', 'Mexican':'Mexico', 'Moroccan':'Morocco',
                            'Namibian':'Namibia', 'New Zealand':'New Zealand', 'Nicaraguan':'Nicaragua', 'Nigerien':'Niger',
                            'Nigerian':'Nigeria', 'Norwegian':'Norway', 'Omani':'Oman', 'Pakistani':'Pakistan',
                            'Panamanian':'Panama', 'Paraguayan':'Paraguay', 'Peruvian':'Peru', 'Philippine':'The Philippines',
                            'Polish':'Poland', 'Portuguese':'Portugal', 'Congolese':'Republic of the Congo',
                            'Romanian':'Romania', 'Russian':'Russia', 'Saudi':'Saudi Arabia', 'Scottish':'Scotland',
                            'Senegalese':'Senegal', 'Serbian':'Serbia', 'Singaporean':'Singapore', 'Slovak':'Slovakia',
                            'Somalian':'Somalia', 'South African':'South Africa', 'Spanish':'Spain', 'Sudanese':'Sudan',
                            'Swedish':'Sweden', 'Swiss':'Switzerland', 'Syrian':'Syria', 'Thai':'Thailand', 'Tunisian':'Tunisia',
                            'Turkish':'Turkey', 'Turkmen':'Turkmenistan', 'Ukranian':'Ukraine', 'Emirati':'United Arab Emirates',
                            'American':'United States', 'Uruguayan':'Uruguay', 'Vietnamese':'Vietnam', 'Welsh':'Wales',
                            'Zambian':'Zambia', 'Zimbabwean':'Zimbabwe',
                            'Afghans':'Afghanistan', 'Algerians':'Algeria', 'Angolans':'Angola', 'Argentines':'Argentina',
                            'Austrians':'Austria', 'Australians':'Australia', 'Bangladeshis':'Bangladesh',
                            'Belarusians':'Belarus', 'Belgians':'Belgium', 'Bolivians':'Bolivia', 'Bosnians':'Bosnia', 
                            'Herzegovinians': 'Herzegovina', 'Brazilians':'Brazil', 'Britishs':'Britain', 'Bulgarians':'Bulgaria',
                            'Cambodians':'Cambodia', 'Cameroonians':'Cameroon', 'Canadians':'Canada', 
                            'Central Africans':'Central African Republic', 'Chadians':'Chad', 'Chinese':'China',
                            'Colombians':'Colombia', 'Costa Ricans':'Costa Rica', 'Croatians':'Croatia', 'Czechs':'the Czech Republic',
                            'Congolese':'Democratic Republic of the Congo', 'Danish':'Denmark', 'Ecuadorians':'Ecuador',
                            'Egyptians':'Egypt', 'Salvadorans':'El Salvador', 'English':'England', 'Estonians':'Estonia',
                            'Ethiopians':'Ethiopia', 'Finnish':'Finland', 'French':'France', 'Germans':'Germany',
                            'Ghanaians':'Ghana', 'Greek':'Greece', 'Guatemalans':'Guatemala', 'Dutch':'Holland',
                            'Hondurans':'Honduras', 'Hungarians':'Hungary', 'Icelandic':'Iceland', 'Indians':'India',
                            'Indonesians':'Indonesia', 'Iranians':'Iran', 'Iraqis':'Iraq', 'Irish':'Ireland', 'Israelis':'Israel',
                            'Italians':'Italy', 'Ivorians':'Ivory Coast', 'Jamaicans':'Jamaica', 'Japanese':'Japan',
                            'Jordanians':'Jordan', 'Kazakhs':'Kazakhstan', 'Kenyans':'Kenya', 'Laos':'Laos', 'Latvians':'Latvia',
                            'Libyans':'Libya', 'Lithuanians':'Lithuania', 'Malagasys':'Madagascar', 'Malaysians':'Malaysia',
                            'Malians':'Mali', 'Mauritanians':'Mauritania', 'Mexicans':'Mexico', 'Moroccans':'Morocco',
                            'Namibians':'Namibia', 'New Zealanders':'New Zealand', 'Nicaraguans':'Nicaragua', 'Nigeriens':'Niger',
                            'Nigerians':'Nigeria', 'Norwegians':'Norway', 'Omanis':'Oman', 'Pakistanis':'Pakistan',
                            'Panamanians':'Panama', 'Paraguayans':'Paraguay', 'Peruvians':'Peru', 'Philippinos':'The Philippines',
                            'Polish':'Poland', 'Portuguese':'Portugal', 'Congolese':'Republic of the Congo',
                            'Romanians':'Romania', 'Russians':'Russia', 'Saudis':'Saudi Arabia', 'Scottish':'Scotland',
                            'Senegaleses':'Senegal', 'Serbiasn':'Serbia', 'Singaporeans':'Singapore', 'Slovaks':'Slovakia',
                            'Somalians':'Somalia', 'South Africans':'South Africa', 'Spanish':'Spain', 'Sudaneses':'Sudan',
                            'Swedish':'Sweden', 'Swiss':'Switzerland', 'Syrians':'Syria', 'Thais':'Thailand', 'Tunisians':'Tunisia',
                            'Turkish':'Turkey', 'Turkmens':'Turkmenistan', 'Ukranians':'Ukraine', 'Emiratis':'United Arab Emirates',
                            'Americans':'United States', 'Uruguayans':'Uruguay',
                            'Zambians':'Zambia', 'Zimbabweans':'Zimbabwe'}

    def readingFrames(self):
        print("Read all the frames.")
        file_list = glob.glob("temp/*.csv")

        files = []

        for filename in file_list:
            df = pd.read_csv(filename)
            files.append(df)

        self.frame = pd.concat(files, axis=0, ignore_index=True)
        self.frame.drop_duplicates(inplace=True)
        return self.frame

    def getLocationNames(self, text_in):
        # extracting entities.
        text = re.sub(r"[^a-zA-Z0-9 ]", " ", text_in)
        doc = self.nlp(text)
        # all tokens that arent stop words or punctuations
        words = [token.text
                for token in doc
                if not token.is_stop and not token.is_punct]
        for key, value in self.country_adjectives.items():
            for i in words:
                if i == key:
                    words.append(value)
        text = " ".join(words)
        locationNames = []
        for doc in self.nlp.pipe(words, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]):
            # Find GPE within text and append to list for gelocation
            place = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
            if len(place) > 0:
                locationNames.append([ent.text for ent in doc.ents if ent.label_ == "GPE"][0])    
            else:
                pass      
        return locationNames

    def getCoordinates(self, text):
        print(len(text))
        if len(text) < 1: 
            place = ["London"]
            #print(place)
        elif text[0] == "UK":
            place = ["England"]
        else:
            place = [text[0]]
            print(place)

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
            return text + random.uniform(-1.5, 1.5)
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
            return "#fa2525"
        elif (text >= -0.8) & (text < -0.6):
            return "#f95323"
        elif (text >= -0.6) & (text < -0.4):
            return "#f98121"
        elif (text >= -0.4) & (text < 0.2):
            return "#f8b01f"
        elif (text >= 0.2) & (text < 0.0):
            return "#f8e01d"
        elif (text >= 0.2) & (text < 0.4):
            return "#dff71b"
        elif (text >= 0.4) & (text < 0.6):
            return "#adf71a"
        elif (text >= 0.6) & (text < 0.8):
            return "#7bf618"
        elif (text >= 0.6) & (text < 0.8):
            return "#48f616"
        else:
            return "#14f514"

    def getColorsRanking(self, text):
        if text == "#fa2525":
            return 1
        elif text == "#f95323":
            return 2 
        elif text == "#f98121":
            return 3 
        elif text == "#f8b01f":
            return 4 
        elif text == "#f8e01d":
            return 5
        elif text == "#dff71b":
            return 6
        elif text == "#adf71a":
            return 7 
        elif text == "#7bf618":
            return 8 
        elif text == "#48f616":
            return 9 
        else:
            return 10 

    def applyToFrame(self):
        print("Create popup column text.")
        self.frame["Popup"] = self.frame.title + "\n" + self.frame.url
        print("Get location names.")
        self.frame['LocationNames'] = self.frame.title.apply(self.getLocationNames)
        print("Get coordinates.")
        self.frame['Coordinates'] = self.frame.LocationNames.apply(self.getCoordinates)
        self.frame['Latitude'] = self.frame.Coordinates.apply(self.getLatitude)
        self.frame.Latitude = pd.to_numeric(self.frame.Latitude, errors='coerce')
        self.frame.Latitude = self.frame.Latitude.apply(self.offSet)
        self.frame['Longitude'] = self.frame.Coordinates.apply(self.getLongitude)
        self.frame.Longitude = pd.to_numeric(self.frame.Longitude, errors='coerce')
        self.frame.Longitude = self.frame.Longitude.apply(self.offSet)
        print("Get frequent word counts.")
        self.frame['FrequentWords'] = self.frame.content.apply(self.getFrequentWords)
        print("Assign colors for markers.")
        self.frame['Compound'] = self.frame['Compound'].astype("Float64")
        self.frame['Colors'] = self.frame.Compound.apply(self.getColors)
        self.frame['Ranking'] = self.frame.Colors.apply(self.getColorsRanking)
        self.frame.sort_values(["Ranking", "published_on"], axis=0, inplace=True)
        self.frame.to_csv("app/static/processed_frame.csv", index=False)
        print('Results were saved. Query processing is complete')
        print("Cleaning up.")
        for folder, subfolders, files in os.walk('temp/'):
            for file in files:
                if file.endswith('.csv') or file.endswith('.txt'):
                    path = os.path.join(folder, file)
                    print('deleted : ', path)
                    os.remove(path)
