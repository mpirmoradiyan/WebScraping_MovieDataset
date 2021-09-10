from getMoviesUrls import *
from getMoviesInfo import *
import json


def saveToJson(title, data):
    with open(title, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def getWaltDisneyMovies():
    """
    Iterates ovel all movies urls and creats list of dictionaries 
    each of which is information of a movie. Finally it saves a json file.
    
    """

    movies_info_list = []

    for url in tqdm(getAllUrls()["URL_Link"]):
        if url is not None:
            movies_info_list.append(getMovieInfo(url=url))

    saveToJson("WaltDisneyDataset.json", movies_info_list)


if __name__ == "__main__":
    getWaltDisneyMovies()
