# Defining a function to extract the data based on labels
import urllib
from config import credentials
from getMoviesUrls import *


def getInfoBox(url: str):
    """Take the url address of a movie and returns the information box
    the movie as a BeautifulSoup object.

    Args:
        url (string): URL address of the movie.

    Returns:
        infobox[BeautifulSoup object]: Information box as the BeautifulSoup object
    """
    # Runing the get request
    r = requests.get(url=url)
    if r.ok:
        # If there exist an information box, extract and store it in infobox
        try:
            # converting the request content into a bs object
            soup = BeautifulSoup(r.content, "lxml")
            # Accessing the information box using the tag "table", and class of "infobox vevent".
            # These tag and class was found after inspecting the webpage.
            infobox = soup.find("table", class_="infobox vevent")
            # Removing the superscript and span tags (to clean up the texts).
            for tag in infobox.find_all(["sup", "span"]):
                tag.decompose()
        except Exception as e:
            infobox = None
        return infobox
    else:
        return r.status_code


def getTitle(infobox):
    """Takes the infobox object returned by the getInfoBox function, and returns the 
    title of the movie.

    Args:
        infobox (BeautifulSoup object): Movie information box as a BeautifulSoup object.

    Returns:
        str: Title of the movie.
    """

    title = infobox.find("th", class_="infobox-above summary").text

    return title


def getContents(infobox, label):
    """Takes infobox object and a label as input and returns string specifying the valuee(s) of the 
    label.

    Args:
        infobox (BeautifulSoup object): Movie information box as a BeautifulSoup object.
        label (str): Specifies a role in the movie, such as "Directed by", "Written by", etc.
                     Labels are fetched by getLabels function in the getMovieInfo(url) function.

    Returns:
        str: Values of the role specified by the label
    """

    # Iterates over all the elements included in infobox which are specified by the tag "tr".
    for element in infobox.find_all("tr"):
        # Accessing the epecific element specifying the label
        match = element.find("th", class_="infobox-label")
        if match is not None:
            # Check if the element label matches our input label
            if match.get_text(" ", strip=True).title() == label:
                # Extract the enclosed data.
                infobox_data = element.find(
                    "td", class_="infobox-data"
                )  # This tag contains the data
                # Store the data in a list and remove some nwanted characters ("\x0")
                role = [
                    text.replace("\xa0", " ") for text in infobox_data.stripped_strings
                ]
    return role[0] if len(role) == 1 else role


def getLabels(infobox) -> list:
    """
    Takes an infobox input and returns all the labels that exist in infobox of the movie.

    Args:
        infobox (BeautifulSoup object): Movie information box as a BeautifulSoup object.

    Returns:
        list: a list of all labels (different roles) that exist in the information box.
    """
    labels = []
    for element in infobox.find_all("tr"):  # Each role enclosed within a "tr" tag.
        match = element.find(
            "th", class_="infobox-label"
        )  # This tag contains the label of the role
        if match is not None:
            labels.append(match.get_text(" ", strip=True).title())

    return labels


def getOmdbInfo(title):
    """Takes a title an return a json file of information from OMDB API.
    IMDB and Meta scores are extracted from this information.

    Args:
        title (str): a movie title

    Returns:
        json: OMDB movie information
    """
    baseUrl = "http://www.omdbapi.com/?"
    # parsing the API credentials to the base url
    credentialsData = urllib.parse.urlencode(credentials)
    finalUrl = baseUrl + credentialsData
    parameters = {"t": title}  # Parameters to add a query to the url
    try:
        r = requests.get(url=finalUrl, params=parameters)
        return r.json()
    except Exception as e:
        return None


def getMovieInfo(url):
    """
    Take the url address of a Walt Disney Movie Wikipedia page and returns a dictionary of the movie information.

    Args:
        url (str): url address of a movie including in 
           "https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films"

    Returns:
        Dictionary: A dictionary of the movie information
    """
    infobox = getInfoBox(url)
    if infobox:
        infoDict = {}
        title = getTitle(infobox)
        infoDict["Title"] = title
        for label in getLabels(infobox):
            infoDict[label] = getContents(infobox, label=label)
        # Adding IMDB and Meta scores
        omdbObject = getOmdbInfo(title)
        if omdbObject:
            infoDict["ImdbScore"] = omdbObject.get("imdbRating", "N/A")
            infoDict["Metascore"] = omdbObject.get("Metascore", "N/A")
        else:
            infoDict["ImdbScore"] = None
            infoDict["Metascore"] = None

        return infoDict
    else:
        pass
