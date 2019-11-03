import urllib3
import requests
import time
import json

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

reddit_home = 'https://www.reddit.com'
slash = '/r/'
subreddit = 'MachineLearning'

def setup_chrome_browser(path_chromedriver):
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(executable_path = path_chromedriver,
                              options=options)
    
    return driver

browser = setup_chrome_browser("/Users/casperbogeskovhansen/Downloads/chromedriver")
browser.get(reddit_home + slash + subreddit)

scroll_n_times = 60

try:
    while scroll_n_times:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        scroll_n_times -= 1
        
    elements = browser.find_elements_by_xpath("//*[@data-click-id='body']")
    links = [tag.get_attribute('href') for tag in elements]
    
    print(len(links))
    
finally:
    browser.quit()
