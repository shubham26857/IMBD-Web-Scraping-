from s3data.read_froms3 import read_s3data


def fetch_movies(name,types):
    """
    return movies id according to user prefernces accepts actor name or genre name and type 
    """
    output =[]
    data = list(read_s3data())
    rows = len(data)
    if types==2:
        for i in range(rows):
            for cur_actor in data[i][types]:
                cur_actor =cur_actor[1:-1].strip()
                if cur_actor.lower() in name:
                    output.append(data[i][0])
                    break
    else:
        for i in range(rows):
            for cur_genre in data[i][types]:  
                cur_genre =cur_genre[1:-1].strip()
                if cur_genre.lower() in name:
                    output.append(data[i][0])
                    break
    return output