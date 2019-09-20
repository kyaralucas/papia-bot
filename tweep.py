from bs4 import BeautifulSoup
import requests
import tweepy
from time import sleep
import json

with open('config.json') as json_file:
    config = json.load(json_file)


def scrape_article(url="https://pap.wikipedia.org/wiki/special:random") -> str:
    """
    Scrapes random article from Papiamentu wikipedia.
    :return: str: First sentence of scraped article
    """
    response = requests.get(url)
    page_content = BeautifulSoup(response.content, "html.parser")
    all_text = page_content.find("p").text
    try:
        sentence = str(all_text.split(".")[0])
    except IndexError:
        sentence = str(all_text)
    return sentence


def check_length(text) -> bool:
    """
    Checks if text length meets Twitter requirements.
    :param text:
    :return: bool:
    """
    if len(text < 150):
        return True
    else:
        return False


print('Starting...')
while True:
    sentence = scrape_article()

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
    auth.set_access_token(config['ACCESS_TOKEN'], config['ACCESS_TOKEN_SECRET'])

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    if check_length(sentence):
        api.update_status(sentence)
        print("[TWEETED] - " + sentence)
        sleep(1800)
    else:
        continue

