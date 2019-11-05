import time
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver

class SeleniumScraper():
    def __init__(self):
        self.driver = None
        self.page = ''
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
                      xpath):
        '''
            This function opens a page in a browser and scrolls n times to the
            bottom of the page. After that, it finds all the elements as
            specified by the xpath, then finds the href attribute.
            
            Parameters:
                page : string
                    This is the URL you want to collect links for.
                
                scroll_n_times : int
                    How many times you want to scroll to the bottom of page
                
                xpath_element : string
                    In the xpath style, you should define which element and
                    value you want the value of the href attribute from.
            
            Returns:
                links : array
                    An array of links to the URLs scraped.
        '''
        self.page = page
        self.driver.get(page)
        
        try:
            # When scroll_n_times = 0, loop stops
            while scroll_n_times:
                # Scrolls browser to the bottom of the page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
                scroll_n_times -= 1
            
            elements = self.driver.find_elements_by_xpath(xpath)
            
            # Get the link from the href attribute
            self.links = [tag.get_attribute('href') for tag in elements]
            
        finally:
            self.driver.quit()
        
        return self.links
    
    def soup_data_helper(self,
                         urls):
        '''
            Finds the script with id of data
        '''
        pure_script_data = []
        
        for url in urls:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            
            soup = BeautifulSoup(r.text, 'html.parser')
            
            pure_script_data.append(soup.find(id='data').text)
        
        return pure_script_data
    
    def reddit_data_to_dict(self,
                            script_data = [], 
                            subreddit_name = ''):
        '''
            Takes id='data' as input and outputs a dict with all ids from page input
        '''
        pure_dicts = []
        
        for data in script_data:
            first_index = data.index('{')
            last_index = data.rfind('}') + 1
            
            subreddit_name = subreddit_name.lower()
            
            json_str = data[first_index:last_index]
            
            pure_dicts.append(json.loads(json_str))
        
        return pure_dicts