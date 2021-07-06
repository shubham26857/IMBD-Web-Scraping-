from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import heapq
from moviesdata import logger


def trans(s):
	"""
	return string after removing punctuation
	"""
	return s.translate(str.maketrans('','',string.punctuation))

def clean_data(synopsis):
	"""
	return tokenize sentencce
	"""
	synopsis = trans(synopsis)
	stop_words = set(stopwords.words('english'))
	word_tokens = word_tokenize(synopsis)
	filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
	return filtered_sentence


def wordVector(bag_of_words,data):
	"""
	Return word vector for given data
	"""
	logger.info('generating word vector')
	vector=[]
	for w in bag_of_words:
		vector.append(data.count(w))
	return vector


def khighest(k,word2count):
	"""
    Return first k highest frequency words
    """
	return  heapq.nlargest(k, word2count, key=word2count.get)


def generate_bagofwords(data):
	"""
    Return bag of words of all the synopsis
    """

	logger.info("generating Bag of words")
	combined_text = ''
	for i in data:
		combined_text +=data[i]
	combined_text= clean_data(combined_text)
	word2count = {}
	for word in combined_text:
		if word not in word2count.keys():
			word2count[word] = 1
		else:
			word2count[word] += 1
	k = 300
	bag_of_words = khighest(k,word2count)
	return bag_of_words[10:]


	

def get_dictionary(data,bag_of_words):

	"""
    Return dictionary with key as movie id and word vector as value
    """

	for cur_data in data:
		cleaned_data = clean_data(data[cur_data])
		data[cur_data] = wordVector(bag_of_words,cleaned_data)
	return data