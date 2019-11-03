import urllib3
import requests
import time
import json

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


base_url = 'https://www.reddit.com'
subreddit = 'MachineLearning'
n_posts = 60

def setup_chrome_browser(path):
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(executable_path = path,
                              options=options)
    
    return driver

browser = setup_chrome_browser("/Users/casperbogeskovhansen/Downloads/chromedriver")
browser.get(base_url + '/r/' + subreddit)

try:
    while n_posts:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        n_posts -= 1
    elements = browser.find_elements_by_xpath("//*[@data-click-id='body']")
    links = [tag.get_attribute('href') for tag in elements]
    print(len(links))
finally:
    print('done')
    #browser.quit()



#soup = BeautifulSoup(page.text, features='html.parser')
#data_str = soup.find(id='data').text

#data = reddit_data_to_dict(data_str, subreddit)