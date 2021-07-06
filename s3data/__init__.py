import boto3
import sys

from moviesdata import logger
from config import aws_access_key,aws_secret_key


ACCESS_KEY = aws_access_key
SECRET_KEY = aws_secret_key

bucket_name = 'shubhamsharma88-datascrape'
#get the s3 object to use in others modules 
try: 
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    s3_resource =boto3.resource('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
except Exception as e:
    logger.error("Exception occurred", exc_info=True)
    sys.exit("unable to connet to s3")

# Creating the high level object oriented interface


