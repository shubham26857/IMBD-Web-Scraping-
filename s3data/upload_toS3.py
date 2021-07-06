import boto3
from botocore.exceptions import NoCredentialsError

from s3data import s3_client,bucket_name
from moviesdata import logger


def upload_to_aws(local_file, s3_file=None):
    """
    Upload local_file to s3 in bucket_name
    """

    logger.info(s3_client)
    if s3_file is None:
        s3_file=local_file
    try:
        s3_client.upload_file(local_file, bucket_name, s3_file)
        print("Upload Successful")
        logger.error("Exception occurred", exc_info=True)
        return True
    except FileNotFoundError:
        print("The file was not found")
        logger.error("Exception occurred", exc_info=True)
        return False
    except NoCredentialsError:
        print("Credentials not available")
        logger.error("Exception occurred", exc_info=True)
        return False
    


