from s3data.fetch_data_s3 import fetch_movies


def main():
    """
    Return list of all movies queried by user
    """

    print("Fetch information about top movies from theirs Genre and Actors")
    while True:
        print("enter 1 for Actors, 2 for Genre, 3 for exit")
        try:
            userinput = int(input("enter your choice  :  "))
        except ValueError as e:
            print("Invalid Value")
            continue
        if userinput not in [1,2,3]:
            print('Invalid input')
            continue
        else:
            if userinput==1:
                print("enter actors name ,if multiple actors enter , seprated ")
                actor_name =  [i.lower() for i in input().split(',')] 
                output  = fetch_movies(actor_name,2)
                print("your movies are:")
                print(*output)
            
            elif userinput==2:
                print("enter genre name ,if multiple genre enter , seprated ")
                genre_name =  [i.lower() for i in input().split(',')]
                output  = fetch_movies(genre_name,3)
                print("your movies are:")
                for i,e in enumerate(output):
                    print(f'{i}  {e}')
            else:
                break



if __name__ =='__main__':
    main()