import requests
import datetime
from bs4 import BeautifulSoup
from core.progress_bar import ProgressBar

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
        self.pure_html = []
        self.pure_script_data = []
        self.data = []
        
        self.urls = []
        self.url_ids = []
        self.url_titles = []
        self.titles = []
        self.authors = []
        self.upvote_ratios = []
        self.scores = []
        self.post_datetime = []
        self.gold_counts = []
        self.total_num_comments = []
        self.categories = []
        self.texts = []
        self.main_links = []
        self.flairs = []
        self.comment_ids = []
        self.post_links = []
        
        # One array per post
        # [ [post 1], [post 2],... ]
        self.final_data = []
        
        
    def get_scripts(self,
                    urls = []):
        '''
            Finds the script with id of data
        '''
        print('Finding <script id="data"> for each link')
        
        self.urls = urls
        
        pure_html_data = []
        pure_script_data = []
        
        progress = ProgressBar(len(urls))
        for url in urls:
            progress.update()
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            
            soup = BeautifulSoup(r.text, 'html.parser')
            
            pure_html_data.append(r.text)
            pure_script_data.append(soup.find(id='data').text)
            
        self.pure_html = pure_html_data
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
                                     ['t3_' + self.url_ids[self.index]]\
                                     ['title']
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
        '''
            Gets the posted time in milliseconds from unix time and converts
            to datetime
        '''
        time = self.single_post_data['posts']\
                                    ['models']\
                                    ['t3_' + self.url_ids[self.index]]\
                                    ['created']
        time = datetime.datetime.fromtimestamp(time//1000.0)
        self.post_datetime.append(time)
    
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
        '''
            If the post links to a third party URL, it will be in the post
            instead of text/discussion of some topic.
            
            Returns main link to other URL.
        '''
        main_link = self.single_post_data['posts']\
                                         ['models']\
                                         ['t3_' + self.url_ids[self.index]]\
                                         ['source']
        if main_link is not None:
            main_link = main_link['url']
            
        self.main_links.append(main_link)
        
    
    def get_links_from_post(self):
        '''
            Gets all links from a post
        '''
        
        all_links_from_post = []
        
        curr_html = self.pure_html[self.index]
        soup = BeautifulSoup(curr_html, 'html.parser')
        div = soup.find('div', attrs={'data-click-id' : 'text'})
        
        if(div is not None):
            for a in div.find_all('a'):
                all_links_from_post.append(a['href'])
        else:
             all_links_from_post.append('')
        
        self.post_links.append(all_links_from_post)
        
    def get_text(self):
        '''
            Posts have text in them, which this method scrapes
        '''
        
        curr_html = self.pure_html[self.index]
        soup = BeautifulSoup(curr_html, 'html.parser')
        div = soup.find('div', attrs={'data-click-id' : 'text'})
        
        if(div is not None):
            self.texts.append(div.getText())
        else:
            self.texts.append('')
        
        
    def get_comment_ids(self):
        '''
            Gets all comment ids for each post.
                                                                                                        /comment id
            https://www.reddit.com/r/MachineLearning/comments/dtfx9m/rtheoretical_research_paper_in_gans/f6wbrvh
        '''
        
        comment_ids = self.single_post_data['commentsPage']\
                                           ['keyToCommentThreadLinkSets']\
                                           ["commentsPage--[post:'t3_" + self.url_ids[self.index] + "']"]
        
        self.comment_ids.append(comment_ids)
        
    def prepare_data_for_sql(self):
        pass
            