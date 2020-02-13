import requests
from bs4 import BeautifulSoup as bs
import re
from .constants import ParseError


def getTrending():
    # This website provides trending tweets for the last 24 hrs
    url = "https://trends24.in/india/"
    headers = {
        "User-Agent": """
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
        """
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": ParseError.bad_status}
    soup = bs(response.content, "lxml")
    firstcard = soup.find("div", class_=re.compile("trend-card"))
    all_hashtag = []
    hashtags = firstcard.find_all("a")
    for hashtag in hashtags:
        all_hashtag.append(hashtag)
    return {"hashtagArray": all_hashtag, "error": None}
