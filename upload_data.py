from moviesdata import logger
from s3data.upload_toS3 import upload_to_aws

def main():
    """
    Used to Upload data to S3 first Time
    """
    uploaded =False
    try:
        uploaded = upload_to_aws('movies_data.csv')
    except:
        uploaded =False
    
    if uploaded:
        logger.info("data Uploaded Succesfully")
    else:
        logger.info("data Upload Failed")



if __name__=='__main__':
    main()


