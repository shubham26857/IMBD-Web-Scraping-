import pandas as pd
import io,sys
import requests,urllib3

from s3data import s3_resource,bucket_name
from moviesdata import logger


def read_s3data(file_name ='movies_data.csv'):
    """
    Reading data from S3 bucket
    """
    logger.info(s3_resource)
    my_bucket=s3_resource.Bucket(bucket_name)
    try:
        for file in my_bucket.objects.all():
            print(file.key)
            if file.key==file_name:
                logger.info("reading File from s3")
                obj = s3_resource.Object(bucket_name,file_name)
                data=obj.get()['Body'].read()
                dataframe =pd.read_csv(io.BytesIO(data))
                data = dataframe.values.tolist()
                for i in range(len(data)):
                    for j in range(len(data[0])):
                        if j>=2:
                            data[i][j] =data[i][j].split(',')
                            data[i][j]= [k.strip(' [] ') for k in data[i][j]]
                return data
        return []
    except :
        logger.error("Exception occurred", exc_info=True)
        sys.exit("unable to connet to s3")



def movies_id_s3():

    """
    Returns all the movies_id present in s3
    """
    ids =[]
    data = read_s3data()
    rows = len(data)
    for i in range(rows):
        ids.append(data[i][0])
    return ids
    
    
        

