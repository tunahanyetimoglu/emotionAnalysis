import numpy as np
import re
from collections import Counter
from nltk.stem.porter import PorterStemmer


ps = PorterStemmer()
from nltk.corpus import stopwords



def clean_tweet(string):

    string = re.sub('[^A-Za-z0-9(),!?\'\`]',' ',string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string) 
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = string.lower()
    string = string.split()
    string = [ps.stem(word) for word in string if not word in set(stopwords.words('english'))]
    string = ' '.join(string)
    return string

