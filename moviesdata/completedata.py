from moviesdata.bagofwords import generate_bagofwords,get_dictionary
from moviesdata.ombddata import update_movies_dict
from moviesdata.savetocsv import save_tocsv
from moviesdata.imdbdata import gettopmovies_synposis
from moviesdata import logger
from s3data.upload_toS3 import upload_to_aws

def final_data():
    """
    Used to call other functions 
    """
    logger.info('calling the gettopmovies_synposis function')
    movies_synopsis =gettopmovies_synposis()
    if not movies_synopsis:
        logger.info("No changes in Data")
        return 
    bag_of_words= generate_bagofwords(movies_synopsis)
    data = get_dictionary(movies_synopsis,bag_of_words)
    data =update_movies_dict(data)
    save_tocsv(data,'movies_data.csv')
    uploaded = upload_to_aws('movies_data.csv')
    if uploaded:
        logger.info("data Uploaded Succesfully")
    else:
        logger.info("data Upload Failed")
    