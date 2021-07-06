from bs4 import BeautifulSoup
import requests
import sys

from moviesdata import logger
from s3data.read_froms3 import movies_id_s3


def response_handle(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as err:
        logger.error("Exception occurred", exc_info=True)
        sys.exit(" Request exception error during  request for scraping the data")
    except requests.exceptions.HTTPError as err:
        logger.error("Exception occurred", exc_info=True)
        sys.exit(" HTTP error during  request for scraping the data")
    except requests.exceptions.ConnectionError as err:
        logger.error("Exception occurred", exc_info=True)
        sys.exit(" Connection error during  request for scraping the data")
    except requests.exceptions.Timeout as err:
        logger.error("Exception occurred", exc_info=True)
        sys.exit(" Timeout error during  request for scraping the data")
    return response

def is_updated_top5(imdb_top5):
    """
    Return what are the changes in IMDBdata
    """
    s3_top5 = movies_id_s3()
    new_ids=[]
    if imdb_top5==s3_top5:
        return new_ids
    for i in imdb_top5:
        if i not in s3_top5:
            new_ids.append(i)
    return s3_top5+new_ids


def gettopmovies_title():

    """
    Return top5 movies titles 
    """
    url = 'http://www.imdb.com/chart/top'
    
    response = response_handle(url)
    
    #get the Html
    soup = BeautifulSoup(response.text, 'html.parser')
    # get all the movies column 
    movies = soup.select('td.titleColumn')
    links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]

    # make a dictionary with movie name as key and title as value
    topmovie_data ={}
    imdb_movies_id =[]
    for index in range(5):
        movie_id = movies[index].find('a')['href'].replace('title','').replace('/','').strip()
        topmovie_data[movie_id]= links[index]
        imdb_movies_id.append(movie_id)
    ids =is_updated_top5(imdb_movies_id)
    if ids:
        count =len(ids)
        index =0
        while(index<250 and count>0):
            movie_id = movies[index].find('a')['href'].replace('title','').replace('/','').strip()
            if movie_id in ids:
                topmovie_data[movie_id]= links[index]
                count-=1
            index+=1
    #ids =[1,2,3]
    return topmovie_data,ids


def gettopmovies_synposis():
    """
    Return movie synopsis as a dict with key as title and value as synopsis
    """

    topmovies_synopsis = {}
    movies_data,movies_id = gettopmovies_title()
    if movies_id==[]:
        return {}
    print(movies_data)
    for  data in movies_data:
        logger.info(f'scraping movie {data}')
        url ='https://www.imdb.com'+movies_data[data]+'plotsummary?ref_=tt_stry_pl#synopsis'
        response = response_handle(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # print(soup.prettify())
        soup =soup.find(id ='plot-synopsis-content')
        for data in soup(['style','script']):
            data.decompose()
        topmovies_synopsis[data] = ''.join(soup.stripped_strings)
            
    return topmovies_synopsis



