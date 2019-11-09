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
        self.flairs = []
        self.gold_counts = []
        self.categories = []
        self.total_num_comments = []
        self.post_links = []
    
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
        
    
    def get_url_id_and_url_title(self,
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
        
        title = self.single_post_data['posts']\
                                     ['models']\
                                     ['t3_' + self.url_ids[self.index]]['title']
        self.titles.append(title)
        
    def get_upvote_ratio(self):
        '''
            Gets the upvote ratio of the post
        '''
        
        ratio = self.single_post_data['posts']\
                                     ['models']\
                                     ['t3_' + self.url_ids[self.index]]\
                                     ['upvoteRatio']
        
        self.upvote_ratios.append(ratio)
    
    def get_score(self):
        '''
            Gets the score of the post
        '''
        
        score = self.single_post_data['posts']\
                                     ['models']\
                                     ['t3_' + self.url_ids[self.index]]\
                                     ['score']
        self.scores.append(score)
    
    def get_posted_time(self):
        time = self.single_post_data['posts']\
                                    ['models']\
                                    ['t3_' + self.url_ids[self.index]]\
                                    ['created']
        self.milli_seconds_time_of_post.append(time)
    
    def get_flairs(self):
        '''
            Get the flair of the post
        '''
        
        flairs = self.single_post_data['posts']\
                                      ['models']\
                                      ['t3_' + self.url_ids[self.index]]\
                                      ['flair']
        
        flair_arr = []
        
        for flair in flairs:
            flair_arr.append(flair['text'])
        
        self.flairs.append(flair_arr)
    
    def get_num_gold(self):
        '''
            Get the number of golds for post
        '''
        
        gold = self.single_post_data['posts']\
                                    ['models']\
                                    ['t3_' + self.url_ids[self.index]]\
                                    ['goldCount']
                                    
        self.gold_counts.append(gold)
    
    def get_author(self):
        '''
            Get the author of the post
        '''
        
        author = self.single_post_data['posts']\
                                      ['models']\
                                      ['t3_' + self.url_ids[self.index]]\
                                      ['author']
                                      
        self.authors.append(author)
    
    def get_category(self):
        '''
            Gets the category of the subreddit
        '''
        categories = self.single_post_data['posts']\
                                          ['models']\
                                          ['t3_' + self.url_ids[self.index]]\
                                          ['postCategories']
        
        cat_arr = []
        
        for cat in categories:
            cat_arr.append(cat['categoryName'])
        
        self.categories.append(cat_arr)
    
    def get_total_num_comments(self):
        '''
            Gets the total number of comments on a post
        '''
        total_num_comments = self.single_post_data['posts']\
                                                  ['models']\
                                                  ['t3_' + self.url_ids[self.index]]\
                                                  ['numComments']
                                                 
        self.total_num_comments.append(total_num_comments)
    
    def get_main_link(self):
        return None
    
    def get_links_from_post(self):
        '''
            Gets all links from a post
        '''
        
        all_links_from_post = []
        
        curr_url = self.urls[self.index]
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(curr_url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        div = soup.find('div', attrs={'data-click-id' : 'text'})
        
        if(div is not None):
            for a in div.find_all('a'):
                all_links_from_post.append(a['href'])
        
        self.post_links.append(all_links_from_post)
        
    def get_comment_ids(self):
        '''
            Gets all comment ids for each post.
                                                                                                        /comment id
            https://www.reddit.com/r/MachineLearning/comments/dtfx9m/rtheoretical_research_paper_in_gans/f6wbrvh
        '''
        
        return None
