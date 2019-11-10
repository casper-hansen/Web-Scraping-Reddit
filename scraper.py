from core.selenium_scraper import SeleniumScraper
from core.soup_scraper import SoupScraper
from core.progress_bar import ProgressBar
import time

reddit_home = 'https://www.reddit.com'
slash = '/r/'
subreddit = 'MachineLearning'
sort_by = '/hot/'

start = time.time()

SelScraper = SeleniumScraper()
BSoupScraper = SoupScraper(reddit_home,
                           slash,
                           subreddit)

SelScraper.setup_chrome_browser()

# Selects all the a elements that have a "data-click-id" attribute with a value of "body"
# https://stackoverflow.com/questions/36019544/if-double-slash-is-used-2-times-in-xpath-what-does-it-mean
xpath = "//a[@data-click-id='body']"
scroll_n_times = 0

# Collect links from subreddit
links = SelScraper.collect_links(page = reddit_home + slash + subreddit + sort_by,
                                 scroll_n_times = scroll_n_times,
                                 xpath = xpath)

# Find the <script> with id='data' for each link
script_data = BSoupScraper.get_scripts(urls = links)

# Transforms each script with data into a Python dict, returned as [{}, {}...]
BSoupScraper.data = SelScraper.reddit_data_to_dict(script_data = script_data)

print('\nScraping data...')
progress = ProgressBar(len(links))
for i, current_data in enumerate(BSoupScraper.data):
    progress.update()
    
    BSoupScraper.get_url_id_and_url_title(BSoupScraper.urls[i],
                                          current_data, i)
    BSoupScraper.get_title()
    BSoupScraper.get_upvote_ratio()
    BSoupScraper.get_score()
    BSoupScraper.get_posted_time()
    BSoupScraper.get_author()
    BSoupScraper.get_flairs()
    BSoupScraper.get_num_gold()
    BSoupScraper.get_category()
    BSoupScraper.get_total_num_comments()
    BSoupScraper.get_comment_ids()
    BSoupScraper.get_links_from_post()
    BSoupScraper.get_main_link()

end = time.time()
print(('\nIt took {0} seconds to scrape {1} links').format(round(end - start, 1), len(links)))