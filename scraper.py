from core.selenium_scraper import SeleniumScraper
from core.soup_scraper import SoupScraper

reddit_home = 'https://www.reddit.com'
slash = '/r/'
subreddit = 'MachineLearning'
sort_by = '/hot/'

SelScraper = SeleniumScraper()
BSoupScraper = SoupScraper(reddit_home,
                           slash,
                           subreddit)

SelScraper.setup_chrome_browser()

# Selects all the a elements that have a "data-click-id" attribute with a value of "body"
# https://stackoverflow.com/questions/36019544/if-double-slash-is-used-2-times-in-xpath-what-does-it-mean
xpath = "//a[@data-click-id='body']"
scroll_n_times = 5

# Collect links from subreddit
links = SelScraper.collect_links(page = reddit_home + slash + subreddit + sort_by,
                                 scroll_n_times = scroll_n_times,
                                 xpath = xpath)

print(('Caught {0} links').format(len(links)))

# Find the <script> with id='data' for each link
script_data = BSoupScraper.get_scripts(urls = links)

# Transforms each script with data into a Python dict, returned as [{}, {}...]
BSoupScraper.data = SelScraper.reddit_data_to_dict(script_data = script_data)

for i, current_data in enumerate(BSoupScraper.data):
    BSoupScraper.get_post_id_and_url_title(BSoupScraper.urls[i])
    BSoupScraper.get_title(current_data, i)
    BSoupScraper.get_upvote_ratio(current_data, i)
    BSoupScraper.get_score(current_data, i)
    BSoupScraper.get_posted_time(current_data, i)
    BSoupScraper.get_author(current_data, i)