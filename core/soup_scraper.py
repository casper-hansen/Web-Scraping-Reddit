import requests
from bs4 import BeautifulSoup

class SoupScraper():
    
    def __init__(self,
                 reddit_home,
                 slash,
                 subreddit):
        self.reddit_home = reddit_home
        self.slash = slash
        self.subreddit = subreddit
        
        self.pure_script_data = []
        self.urls = []
        self.data = []
        self.url_ids = []
        self.url_titles = []
        self.titles = []
    
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
    
    def get_post_ids_and_url_titles(self):
        url_ids = []
        url_titles = []
        
        for link in self.urls:
            first_index = link.index('comments/') + 9
            last_index = first_index + 6
            url_ids.append(link[first_index:last_index])
            
            first_index = last_index + 1
            last_index = link.rfind('/')
            url_titles.append(link[first_index:last_index])
        
        self.url_ids = url_ids
        self.url_titles = url_titles
    
    def get_titles(self):
        titles = []
        
        for i, data in enumerate(self.data):
            place = self.slash + self.subreddit + '/comments/' + self.url_ids[i] + '/' + self.url_titles[i] + '/'
            titles.append(data['platform']['metas'][place]['title'])
        
        self.titles = titles
    
    def get_votes(self):
        return None
    
    def get_upvote_ratio(self):
        # Upvote ratio
        #json.loads(json_str)['posts']['models']['t3_dkox1s']['upvoteRatio']
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
    
    def get_comment_ids(self):
        # All comment ids
        # commentsPage -> keyToChatCommentLinks -> commentsPage--[post:'t3_dkox1s'] -> id
        return None