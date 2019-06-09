import re,csv
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer, PorterStemmer
from string import punctuation

spell = SpellChecker()
wordnetLemm = WordNetLemmatizer()
ps = PorterStemmer()
from nltk.corpus import stopwords

def converter(word):
    word = word.split(" ")
    j = 0
    fileName = "../data/slang.txt"
    for _str in word:
        with open(fileName, "r") as file:      
            dataFromFile = csv.reader(file, delimiter="=")
            _str = re.sub('[^a-zA-Z0-9]+', '', _str)
            for row in dataFromFile:
                if _str.upper() == row[0]:
                    word[j] = row[1]
        j = j + 1
        file.close()    
    return ' '.join(word)

def check_html(tweet):
    fileName = "../data/htmlwords.txt"
    with open(fileName ,"r") as file:
        data = csv.reader(file)
        for row in data:
            if row[0] in tweet:
              tweet.replace(row[0],' ')
    return tweet    
def is_valid_word(word):  
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)

def handle_emojis(tweet):
    
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', 'laugh', tweet)
    tweet = re.sub(r'(<3|:\*)', 'love', tweet)
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', 'wink', tweet)
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', 'sad', tweet)
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', 'cry', tweet)   
    return tweet

def check_hashtag(tweet):
    new = []
    words = tweet.split()
    if len(words) <= 0:
        return tweet
    for word in words:
        if(len(word) <= 0):
            continue
        if(word[0] == '#'):
           if(len(word) == 1):
               continue
           if(word[1].isupper() == True):
               if(word[2].isupper() == True):
                   continue
               else:
                   word = re.findall('[A-Z][^A-Z]*', word)
                   new.append(' '.join(word))
        else:
            new.append(word)
    return ' '.join(new)
def clean_tweet(tweet):
    #print("Tweet : "  + tweet)
    table = str.maketrans(".,!/_-\'?", 8*" ")
    clean_tweet = []
    tweet = re.sub(r'(&lt;)', '<', tweet)  
    tweet = re.sub(r'(&quot;)', ' ', tweet)
    tweet = check_html(tweet)     
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' ', tweet)
    tweet = re.sub(r'((www\.[\S]+)|(http?://[\S]+))', ' ', tweet)
    #print("Link Temizleme Sonrası : " + tweet)
    tweet = re.sub(r'@[\S]+', ' _mention_ ', tweet)
    #print("Mention Temizleme : " + tweet)
    tweet = check_hashtag(tweet)
    tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
    #print("Hashtag Temizleme : " + tweet)
    tweet = re.sub(r'\brt\b', '', tweet)
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    tweet = handle_emojis(tweet)
    #print("Emoji Temizleme : " + tweet)
    tweet = re.sub(r'\s+', ' ', tweet)
    tweet = converter(tweet)
    #print("Kısaltma Temizleme : " + tweet)
    tweet = re.sub('\d+', '', tweet)
    tweet = re.sub('\'',' ', tweet)
    tweet = tweet.translate(table)
    tweet = ''.join(word for word in tweet if word not in punctuation)
    tweet = tweet.strip(' "\'')
    tweet = tweet.lower()
    #print("Noktalama Temizleme " + tweet)
    words = tweet.split()
    
    for word in words:
        word = spell.correction(word)
        if not word in set(stopwords.words('english')):
            word = re.sub(r'(.)\1+', r'\1\1', word)
            word = re.sub(r'(-|\')', ' ', word)
            if is_valid_word(word):
                word = str(wordnetLemm.lemmatize(word))
                #word = str(ps.stem(word))
                word = spell.correction(word)
                clean_tweet.append(word)
    return ' '.join(clean_tweet)