import requests
import json
import re


from config import api_key
from requests.models import Response
from moviesdata import logger



def check_splcharacter(test):
    """
    it checks the special characters in tittle
    """

    string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
 
    if(string_check.search(test) == None):
        return False
    else: 
        return True


def validate_id(id):
    """
    it validates the ID
    """

    try:
        if len(id)<9 or len(id)>9:
            raise Exception("Enter id should consist of 9 character")
        if id[:2]!='tt':
            raise ValueError("movie id should start with 'tt' only ")
        if check_splcharacter(id):
            raise ValueError("moive id should not contain special character")
    except ValueError as error:
        logger.error("Exception occurred", exc_info=True)
        return False
    except Exception as e:
        logger.error("Exception occurred", exc_info=True)
        return False

    return True

def apiresponse(id):

    """
    Return data from omdb api
    """
    error =None
    url  = "http://www.omdbapi.com/"
    #enter your api key
    query = {'apikey':api_key}
    query['i']=id
    logger.info("fetching data from API")
    response ={}
    try:
        response = requests.get(url =url,params=query)
    except:
        logger.error("Exception occurred", exc_info=True)
        error ='Unable to fetch data'
    if error is None:
        if response.json().get('Response')=='False':
            error = response.json().get('Error')
    return error,response

def movie_details(id):
    """
    Return details of movie like genre and actors
    """

    error =False
    if not validate_id(id):
        error=  True
    else:
        error,response = apiresponse(id)
        if error == None and response.status_code ==200 :
            data =response.json()
            #print(data['Actors'].split(','),type(data['Actors']))
            return data['Actors'].split(','),data['Genre'].split(','),False
        else:
            if response:
                logger.error(response.json())
            error =True
    return [],[],error

def update_movies_dict(data):
    """
    Update the movies dictionary add actors and genres as keys
    """
    out =[]
    for cur_data in data:
        temp ={}
        Actors,Genre,error = movie_details(cur_data)
        print(Actors)
        if error :
            continue
        temp['id'] =cur_data
        temp['word_vector'] = data[cur_data]
        temp["Actor"] = Actors
        temp["Genre"] =Genre
        out.append(temp)
    return out
