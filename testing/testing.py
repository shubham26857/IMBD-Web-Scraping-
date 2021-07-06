import unittest
import csv

#import 
from moviesdata.ombddata import check_splcharacter,validate_id,apiresponse,movie_details
from moviesdata.bagofwords import khighest,wordVector,clean_data,trans,get_dictionary
from moviesdata.imdbdata import gettopmovies_title
from moviesdata.savetocsv import save_tocsv
from s3data.fetch_data_s3 import fetch_movies
from s3data.read_froms3 import movies_id_s3
from s3data.upload_toS3 import upload_to_aws



class ApiTesting(unittest.TestCase):
    """
    testing  of working of API
    """

    def test_splchahracter(self):
        result =check_splcharacter('tt0011239')
        self.assertFalse(result)

        result  = check_splcharacter('tt!@11223')
        self.assertTrue(result)


    def test_validate_id(self):
        result =validate_id('tt0011239')
        self.assertTrue(result)
        
        result = validate_id('001122339')
        self.assertFalse(result)

        result  = validate_id('tt234')
        self.assertFalse(result)

        result =validate_id('tt00!1234')
        self.assertFalse(result)


    def test_api_response(self):
        error,response = apiresponse('tt0111161')
        statuscode = response.status_code
        self.assertEqual((None,200),(error,200))

        error,response = apiresponse('tt01161')
        self.assertEqual('Incorrect IMDb ID.',error)
    

    def test_movie_details(self):
        actor,genre,error = movie_details('tt01161')
        self.assertEqual(([],[],True),(actor,genre,True))
    
        actor,genre,error = movie_details('tt0111161')
        test_actor =['Tim Robbins', ' Morgan Freeman', ' Bob Gunton']
        test_genre =['Drama']
        test_error = False
        self.assertEqual((test_actor,test_genre,test_error),(actor,genre,error))


class TestBagOfWords(unittest.TestCase):
    """
    testing  of Bag  of Words
    """

    def test_khighest(self):
        words= {'jocker':3,'godfather':2,'loki':1,'aa':1,'bb':1}
        result = khighest(2,words)
        test_word =['jocker','godfather']
        self.assertEqual(test_word,result)


    def test_wordVector(self):
        words =['jocker','godfather','loki','aa','bb','jocker']
        bagofword = ['jocker','godfather']
        vector =wordVector(bagofword,words)
        test_vector =[2,1]
        self.assertEqual(test_vector,vector)


    def test_clean_data(self):
        sentence ="hi! jocker acted very well gave his 100% in the movies !!"
        result = clean_data(sentence)
        test_result =['hi', 'jocker', 'acted', 'well', 'gave', '100', 'movies']
        self.assertEqual(test_result,result)
    

    def test_trans(self):
        sentence = 'hi! @jocker acted very well gave his 100% in the movies !!'
        result =trans(sentence)
        test_result = 'hi jocker acted very well gave his 100 in the movies '
        self.assertEqual(test_result,result)


    def test_get_dictionary(self):
        words ={'a':'jocker godfather loki aa bb jocker'}
        bagofword = ['jocker','godfather']
        result =get_dictionary(words,bagofword)
        test_result= {'a':[2,1]}
        self.assertEqual(test_result,result)

        words = {'a':'jocker godfather loki aa bb'}
        bagofword = ['jocker','godfather']
        result =get_dictionary(words,bagofword)
        test_result= {'a':[2,1]}
        self.assertNotEqual(test_result,result)


class Test_Imdb_data(unittest.TestCase):
    """
    testing  of IMDB data
    """
    def  test_gettopmovies_title(self):
        test_result ={'tt0111161': '/title/tt0111161/',
         'tt0068646': '/title/tt0068646/', 
         'tt0071562': '/title/tt0071562/',
          'tt0468569': '/title/tt0468569/', 
          'tt0050083': '/title/tt0050083/'}

        result,ids = gettopmovies_title()
        self.assertEqual(test_result,result)

class Test_Saveto_CSV(unittest.TestCase):
    """
    testing  of saving data to CSV
    """

    def test_save_tocsv(self):
        data =[{'title':'tt1001161'},{'title':'tt1001162'},{'title':'tt1001163'}]
        save_tocsv(data,'test_data.csv')
        with open('test_data.csv',"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
        result =row_count
        test_result =4
        self.assertEqual(test_result,result)

class Test_Fetch_info(unittest.TestCase):

    """
    testing  of Fetch information
    """
    def test_fetch_movies(self):
        result = fetch_movies(['thriller'],3)
        test_result=['tt0468569']
        self.assertEqual(test_result,result)


        result = fetch_movies(['drama','action'],3)
        test_result=['tt0111161','tt0068646','tt0071562','tt0468569','tt0050083']
        self.assertEqual(test_result,result)


        result = fetch_movies(['christian bale'],2)
        test_result=['tt0468569']
        self.assertEqual(test_result,result)

class Test_upload_toS3(unittest.TestCase):

    """
    Testing of uploading data to s3
    """

    def test_upload_toaws(self):
        test_result =False
        result = upload_to_aws('file11.csv')
        self.assertEqual(test_result,result)

    
class Test_Readfrom_s3(unittest.TestCase):
    
    """
    testing  of Reading CSV file from s3
    """
    def test_movies_id_s3(self):
        result =movies_id_s3()
        test_result=['tt0111161','tt0068646','tt0071562','tt0468569','tt0050083']
        self.assertEqual(test_result,result)





