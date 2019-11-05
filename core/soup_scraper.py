import requests
from bs4 import BeautifulSoup

class SoupScraper():
    
    def __init__(self):
        self.pure_script_data = []
    
    def get_scripts_from_urls(self,
                              urls = []):
        '''
            Finds the script with id of data
        '''
        pure_script_data = []
        
        for url in urls:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            
            soup = BeautifulSoup(r.text, 'html.parser')
            
            pure_script_data.append(soup.find(id='data').text)
        
        self.pure_script_data = pure_script_data
        
        return pure_script_data