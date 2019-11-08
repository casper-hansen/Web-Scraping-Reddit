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
        
        self.single_post_data = {}
        self.index = 0
        
        self.pure_script_data = []
        self.urls = []
        self.data = []
        self.url_ids = []
        self.url_titles = []
        self.titles = []
        self.upvote_ratios = []
        self.scores = []
        self.milli_seconds_time_of_post = []
        self.authors = []
    
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
        
    
    def get_post_id_and_url_title(self,
                                  single_link,
                                  current_data,
                                  index):
        '''
            Gets id and title from URL
            
                                       /--id--/--------------------URL title--------------------/
            /r/MachineLearning/comments/dkox1s/d_machine_learning_wayr_what_are_you_reading_week/
        '''
        
        self.single_post_data = current_data
        self.index = index
        
        first_index = single_link.index('comments/') + 9
        last_index = first_index + 6
        url_id = single_link[first_index:last_index]
        
        first_index = last_index + 1
        last_index = single_link.rfind('/')
        url_title = single_link[first_index:last_index]
        
        self.url_ids.append(url_id)
        self.url_titles.append(url_title)
    
    def get_title(self):
        '''
            Gets the title of the post
        '''
        
        title = self.single_post_data['posts']['models']['t3_' + self.url_ids[self.index]]['title']
        self.titles.append(title)
        
    def get_upvote_ratio(self):
        '''
            Gets the upvote ratio of the post
        '''
        
        ratio = self.single_post_data['posts']['models']['t3_' + self.url_ids[self.index]]['upvoteRatio']
        self.upvote_ratios.append(ratio)
    
    def get_score(self):
        '''
            Gets the score of the post
        '''
        
        score = self.single_post_data['posts']['models']['t3_' + self.url_ids[self.index]]['score']
        self.scores.append(score)
    
    def get_posted_time(self):
        time = self.single_post_data['posts']['models']['t3_' + self.url_ids[self.index]]['created']
        self.milli_seconds_time_of_post.append(time)
    
    def get_flairs(self):
        '''
            Get the flair of the post
        '''
         # ['posts']['models']['t3_id']['flair']['text']
        return None
    
    def get_num_gold(self):
        '''
            Get the number of golds for post
        '''
        # ['posts']['models']['t3_id']['goldCount']
        return None
    
    def get_author(self):
        '''
            Get the author of the post
        '''
        author = self.single_post_data['posts']['models']['t3_' + self.url_ids[self.index]]['author']
        self.authors.append(author)
    
    def get_main_link(self):
        return None
    
    def get_links_from_post(self):
        return None
    
    def get_total_num_comments(self):
        # ['posts']['models']['t3_id']['numComments']
        return None
    
    def get_comment_ids(self):
        # All comment ids
        # commentsPage -> keyToChatCommentLinks -> commentsPage--[post:'t3_dkox1s'] -> id
        return None
    
    def get_category(self):
        # ['posts']['models']['t3_id']['postCategories']['categoryName']
        return None