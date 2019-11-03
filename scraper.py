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

class SeleniumScraper():
    def __init__(self):
        self.driver = None
        self.links = []
    
    def setup_chrome_browser(self,
                             path_chromedriver):
        '''
            This function allows for setting up a chrome driver for use with
            Selenium. It expects a path to a chromedriver, available for download
            on this link: https://chromedriver.chromium.org/home
        '''
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(executable_path = path_chromedriver,
                                       options=options)
        
    def collect_links(self,
                      page,
                      scroll_n_times,
                      xpath_element):
        self.driver.get(page)
        
        try:
            # When scroll_n_times = 0, loop stops
            while scroll_n_times:
                # Scrolls browser to the bottom of the page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
                scroll_n_times -= 1
            
            elements = self.driver.find_elements_by_xpath(xpath_element)
            
            # Get the link from the href attribute
            self.links = [tag.get_attribute('href') for tag in elements]
            
        finally:
            self.driver.quit()
        
        return self.links

SS = SeleniumScraper()
SS.setup_chrome_browser("/Users/casperbogeskovhansen/Downloads/chromedriver")

# Selects all the a elements that have a "data-click-id" attribute with a value of "body"
xpath_element = "//a[@data-click-id='body']"
scroll_n_times = 5

links = SS.collect_links(page = reddit_home + slash + subreddit,
                         scroll_n_times = scroll_n_times,
                         xpath_element = xpath_element)

print(len(links))