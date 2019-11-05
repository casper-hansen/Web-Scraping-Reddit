from selenium_scraper import SeleniumScraper

reddit_home = 'https://www.reddit.com'
slash = '/r/'
subreddit = 'MachineLearning'

SS = SeleniumScraper()
SS.setup_chrome_browser("/Users/casperbogeskovhansen/Downloads/chromedriver")

# Selects all the a elements that have a "data-click-id" attribute with a value of "body"
xpath = "//a[@data-click-id='body']"
scroll_n_times = 5

links = SS.collect_links(page = reddit_home + slash + subreddit,
                         scroll_n_times = scroll_n_times,
                         xpath = xpath)

script_data = SS.soup_data_helper(links)

data = SS.reddit_data_to_dict(script_data, subreddit)

# Upvote ratio
#json.loads(json_str)['posts']['models']['t3_dkox1s']['upvoteRatio']

# All comment ids
# commentsPage -> keyToChatCommentLinks -> commentsPage--[post:'t3_dkox1s'] -> id