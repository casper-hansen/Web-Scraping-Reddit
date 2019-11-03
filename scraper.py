import urllib3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

base_url = 'https://www.reddit.com/r/'
subreddit = 'MachineLearning'

# Headers to mimic a browser visit
headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object
page = requests.get(base_url + subreddit, headers=headers)

def reddit_data_to_dict(data = '', subreddit_name = ''):
    '''
        Takes id='data' as input and outputs a dict with all ids from page input
    '''
    first_index = data.index('{')
    last_index = data.rfind('}') + 1
    
    subreddit_name = subreddit_name.lower()
    
    json_str = data[first_index:last_index]
    
    dict_from_json_str = json.loads(json_str) \     # Load json string
                                   ['listings'] \   # Find listings key
                                   ['postOrder'] \  # Find postOrder key
                                   ['ids'] \        # Find ids key
                                   [subreddit_name] # Find subreddit name key
    
    return dict_from_json_str

soup = BeautifulSoup(page.text, features='html.parser')
data_str = soup.find(id='data').text

data = reddit_data_to_dict(data_str, subreddit)