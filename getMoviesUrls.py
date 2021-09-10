"""
Extract the list of Walt Disney movies out from Wikipedia,
and stores the titles and the webpage links of them into a DataFrame.
"""


import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


def getAllUrls():
    URL = "https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films"
    baseLink = "https://en.wikipedia.org"
    df = pd.DataFrame(columns=["Title", "URL_Link"])
    r = requests.get(url=URL)
    soup = BeautifulSoup(r.content, "lxml")
    for item in soup.find_all("table", class_="wikitable sortable"):
        for i in item.find_all("i"):
            try:
                title = i.a["title"]
                link = i.a["href"]
                link = baseLink + link
                df_new_line = pd.DataFrame(
                    [[title, link]], columns=["Title", "URL_Link"]
                )
                df = pd.concat([df, df_new_line], ignore_index=True)
            except Exception as e:
                title = None
                link = None

    return df
