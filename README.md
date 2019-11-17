# Web Scraping Reddit
Web scraping /r/MachineLearning with BeautifulSoup and Selenium, without using the Reddit API, since you mostly web scrape when an API is not available -- or just when it's easier.

If you found this repository useful, consider giving it a star, such that you easily can find it again.

## Install

To run this project, you need to have the following (besides [Python 3+](https://www.python.org/downloads/)):

1. [Chrome browser](https://www.google.com/chrome/) installed on your computer.
2. Paste this into your address bar in Chrome chrome://settings/help. Download the corresponding [chromedriver version here](https://chromedriver.chromium.org/downloads).
3. Place the chromerdriver in the *core* folder of this project.
3. Install the packages specified below with pip or conda.

### Install the needed packages with pip:

```
pip install beautifulsoup4 selenium
```

### Install the needed packages with conda:

```
conda install -c anaconda -y beautifulsoup4 selenium
```

**Note**: If your Chrome browser automatically updates to a new version, the chromedriver that you downloaded will almost surely not work, after an automatic update.