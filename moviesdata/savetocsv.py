import csv
from moviesdata import logger

def save_tocsv(data,file_name):
    """
    it saves movies data to movies_data.csv accepts data as  dictionary
    """
    try:
        field_names = list(data[0].keys())
    except KeyError as e:
        field_names= {}
    except  IndexError as e:
        logger.info("empty data")
        field_names={}
    logger.info("writing data in csv")
    with open(file_name, 'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(data)
