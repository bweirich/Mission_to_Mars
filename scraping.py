
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import datetime as dt
import pandas as pd

def scrape_all():
    # initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # run mars_new function
    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store reuslts in dic
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }

    # stop webdriver and return data
    browser.quit()
    return data

# mars_news function to scrape mars news site
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert browser html to soup object the quite browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use parent element to find 1st tag and save it
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # use parent element to find paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# Featured Images function from image site
def featured_image(browser):
    # visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add try/except for error handling
    try:
        # find relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # use base url to create absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Mars facts function
def mars_facts():
    # add try/except for handling errors
    try:
        # scrape data table into dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # assign columns and set index 
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # convert dataframe into HTML format, add boostrap
    return df.to_html()

if __name__ == '__main__':
    # if running as script, print scraped data
    print(scrape_all())