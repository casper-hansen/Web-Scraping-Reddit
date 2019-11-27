from core.selenium_scraper import SeleniumScraper
from core.soup_scraper import SoupScraper
from core.progress_bar import ProgressBar
from core.sql_access import SqlAccess
import time

reddit_home = 'https://www.reddit.com'
slash = '/r/'
subreddit = 'DataScience'
sort_by = '/hot/'
scroll_n_times = 1000
scrape_comments = True
erase_db_first = True

start = time.time()

SQL = SqlAccess()
SelScraper = SeleniumScraper()
BSS = SoupScraper(reddit_home,
                  slash,
                  subreddit)

SelScraper.setup_chrome_browser()

# Collect links from subreddit
links = SelScraper.collect_links(page = reddit_home + 
                                        slash + subreddit + sort_by,
                                 scroll_n_times = scroll_n_times)

# Find the <script> with id='data' for each link
script_data = BSS.get_scripts(urls = links)

# Transforms each script with data into a Python dict, returned as [{}, {}...]
BSS.data = SelScraper.reddit_data_to_dict(script_data = script_data)

print('Scraping data...')
progress = ProgressBar(len(links))
for i, current_data in enumerate(BSS.data):
    progress.update()
    
    BSS.get_url_id_and_url_title(BSS.urls[i],
                                 current_data, i)
    BSS.get_title()
    BSS.get_upvote_ratio()
    BSS.get_score()
    BSS.get_posted_time()
    BSS.get_author()
    BSS.get_flairs()
    BSS.get_num_gold()
    BSS.get_category()
    BSS.get_total_num_comments()
    BSS.get_links_from_post()
    BSS.get_main_link()
    BSS.get_text()
    BSS.get_comment_ids()

time.sleep(1)
BSS.prepare_data_for_sql(scrape_comments=scrape_comments)

try:
    SQL.create_or_connect_db(erase_first=erase_db_first)
    # [0] = post, [1] = comment, [2] = link
    for i in range(len(BSS.post_data)):
        SQL.insert('post', data = BSS.post_data[i])
        SQL.insert('link', data = BSS.link_data[i])
        
        if scrape_comments:
            SQL.insert('comment', data = BSS.comment_data[i])
except Exception as ex:
    print(ex)
finally:
    SQL.save_changes()

time.sleep(1)
end = time.time()

print(('\nIt took {0} seconds to scrape and store {1} links').format(round(end - start, 1),
                                                                     len(links)))