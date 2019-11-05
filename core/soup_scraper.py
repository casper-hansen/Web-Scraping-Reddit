import requests
from bs4 import BeautifulSoup

class SoupScraper():
    
    def __init__(self):
        self.pure_script_data = []
        self.urls = []
    
    def get_scripts(self,
                    urls = []):
        '''
            Finds the script with id of data
        '''
        self.urls = urls
        
        pure_script_data = []
        
        for url in urls:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            
            soup = BeautifulSoup(r.text, 'html.parser')
            
            pure_script_data.append(soup.find(id='data').text)
        
        self.pure_script_data = pure_script_data
        
        return pure_script_data
    
    def get_titles(self):
        return None
    
    def get_votes(self):
        return None
    
    def get_post_time(self):
        return None
    
    def get_flair(self):
        return None
    
    def get_user(self):
        return None
    
    def get_main_link(self):
        return None
    
    def get_all_links(self):
        return None