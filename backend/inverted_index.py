import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
import string
import os
from os.path import join
import json
import math

ROOT = "./"
EXT = ".json"
BEG = "tweets_2018-"

nltk.download('stopwords')
nltk.download('punkt')
stoplist = stopwords.words("spanish")
stoplist += ['?','aqui','.',',','»','«','â','ã','>','<','(',')','º','u']
stemmer = SnowballStemmer('spanish')

class InvertedIndex:
  inverted_index = { }
  tweets_files = [ ]

  def read_files(self):
    for base, dirs, files in os.walk(ROOT):
      for file in files:
        file_path = join(base, file)
        if file_path.endswith(EXT) and BEG in file_path:
          self.tweets_files.append(file_path)
  
  def remove_punctuation(self, text):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

  def remove_emoji(self, text):
    emoji_pattern = re.compile("["
      u"\U0001F600-\U0001F64F"  # emoticons
      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
      u"\U0001F680-\U0001F6FF"  # transport & map symbols
      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
      u"\U00002500-\U00002BEF"  # chinese char
      u"\U00002702-\U000027B0"
      u"\U00002702-\U000027B0"
      u"\U000024C2-\U0001F251"
      u"\U0001f926-\U0001f937"
      u"\U00010000-\U0010ffff"
      u"\u2640-\u2642" 
      u"\u2600-\u2B55"
      u"\u200d"
      u"\u23cf"
      u"\u23e9"
      u"\u231a"
      u"\ufe0f"  # dingbats
      u"\u3030"
                    "]+", re.UNICODE)
    return re.sub(emoji_pattern, '', text)

  def remove_url(self, text):
    t = text.find('https://t.co/')
    if t != -1:
      text = re.sub('https://t.co/\w{10}', '', text)
    return text

  def remove_special_character(self, text):
    special_characters = ('\"','\'','º','&','¿','?','¡','!',' “','…','👏',
								'-','—','‘','•','›','‼','€','£','↑','→','↓','↔',
								'↘','↪','√','∧','⊃','⌒','⌛','⏬','⏯','⏰','⏹')
    for char in special_characters:
      text = text.replace(char, "")
    return text

  def clean_text(self, text):
    text = self.remove_special_character(text)
    text = self.remove_punctuation(text)
    text = self.remove_emoji(text)
    text = self.remove_url(text)
    text = nltk.word_tokenize(text)
    return text

  def create_inverted_index(self):
    count = 0
    for file_path in self.tweets_files:
      json_file = open(file_path, encoding='utf-8').read()
      text_list = [(e['text'], e['id']) for e in json.loads(json_file) if not e["retweeted"]]
      for text in text_list:
        tweet_text = text[0]
        tweet_text = self.clean_text(tweet_text.lower())
        for word in tweet_text:
          if word not in stoplist:
            token = stemmer.stem(word)
            if token not in self.inverted_index.keys():
              self.inverted_index[token] = {"df": 0}
            if file_path not in self.inverted_index[token].keys():
              self.inverted_index[token]["df"] += 1
              self.inverted_index[token][file_path] = {"tf": 0}
              self.inverted_index[token][file_path]["tweets"] = []
            found = False
            for x in self.inverted_index[token][file_path]["tweets"]:
              if x["tweet_id"] == text[1]:
                found = True
                x["freq"] += 1
                break
            if not found:
              self.inverted_index[token][file_path]["tweets"].append({"tweet_id": text[1], "freq": 1})
            self.inverted_index[token][file_path]["tf"] += 1
      count += 1
      print(count, file_path)
    for token in self.inverted_index.keys():
      self.inverted_index[token]["idf"] = math.log(len(self.tweets_files) / self.inverted_index[token]["df"], 10)
      self.inverted_index[token]["score"] = 0
      for doc in self.inverted_index[token].keys():
        if doc not in ["idf", "score", "df"]:
          tf = self.inverted_index[token][doc]["tf"]
          idf = self.inverted_index[token]["idf"]
          self.inverted_index[token][doc]["tf_idf"] = (1 + math.log(tf)) * idf
          tf_idf = self.inverted_index[token][doc]["tf_idf"]
          self.inverted_index[token]["score"] += tf_idf
    for doc in self.tweets_files:
      norma = 0
      for token in self.inverted_index.keys():
        if doc in self.inverted_index[token].keys():
          norma += self.inverted_index[token][doc]["tf_idf"] ** 2
      norma = math.sqrt(norma)
      for token in self.inverted_index.keys():
        if doc in self.inverted_index[token].keys():
          self.inverted_index[token][doc]["norma"] = self.inverted_index[token][doc]["tf_idf"] / norma

    # Memoria secundaria
    json_object = json.dumps(self.inverted_index, indent=4)
    with open("inverted_index_memsec.json", "w") as outfile:
        outfile.write(json_object)
        outfile.close()

  def initiate_inverted_index(self):
    self.read_files()
    try:
      inverted_index_memsec = open("inverted_index_memsec.json", "r")
      self.inverted_index = json.load(inverted_index_memsec)
    except IOError:
      self.create_inverted_index()
    
  def compare_query(self, query):
    query = self.clean_text(query)
    index_query = {}
    for word in query:
      word = stemmer.stem(word)
      if word not in index_query.keys():
        index_query[word] = {"tf": 0}
      index_query[word]["tf"] += 1
    norma = 0
    for word in index_query.keys():
      if word in self.inverted_index.keys():
        index_query[word]["tf_idf"] = (1 + math.log10(index_query[word]["tf"])) * self.inverted_index[word]["idf"]
        norma += index_query[word]["tf_idf"] ** 2
    norma = math.sqrt(norma)
    for word in index_query.keys():
      if "tf_idf" in index_query[word].keys():
        index_query[word]["norma"] = index_query[word]["tf_idf"] / norma if norma != 0 else 0
    cosenos = []
    for file in self.tweets_files:
      similarity = 0
      tweets = []
      for word in index_query.keys():
        if "norma" in index_query[word].keys() and file in self.inverted_index[word].keys():
          tweets_by_word = sorted(self.inverted_index[word][file]["tweets"], key=lambda v: v["freq"], reverse=True)
          tweets.append({"word": word, "tweets": tweets_by_word})
          similarity += index_query[word]["norma"] * self.inverted_index[word][file]["norma"]
      cosenos.append({"docId": file, "coseno": similarity, "results": tweets})
    cosenos = sorted(cosenos, key=lambda v: v["coseno"], reverse=True)
    return cosenos
