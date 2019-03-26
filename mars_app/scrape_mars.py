from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    try:
        latest_news = soup.find('div', class_="list_text")
        news_title = latest_news.find('a').text
        news_p = latest_news.find('div', class_="article_teaser_body").text
    except AttributeError:
        return None, None    
    return news_title, news_p

# # JPL Featured Image
def featured_img(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    featured_img_button = browser.find_by_id('full_image')
    featured_img_button.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_button = browser.find_link_by_partial_text('more info')
    more_info_button.click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.select_one('figure.lede a img')
    
    try:
        img_url = img.get('src')
    except AttributeError:
        return None

    img_url = f'https://www.jpl.nasa.gov{img_url}'
    return img_url


# # Mars Weather
def weather(browser):
#Visit browser to Mars Twitter account
    url ='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    weather_latest_tweet = soup.find('div', attrs={"class": "tweet","data-name": "Mars Weather"})
    mars_weather = weather_latest_tweet.find('p', 'tweet-text').text
    return mars_weather


# # Mars Hemisphere
def hemisphere(browser):
    url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_urls =[]

    links = browser.find_by_css('a.product-item h3')
    for link in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css('a.product-item h3')[link].click()
        # Find a tag and extract href
        img_link = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = img_link['href']
        #Retrieve hemisphere title
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_urls.append(hemisphere)
        browser.back()
    return hemisphere_urls
# # Set a helper function to scrape hemisphere data
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, 'html.parser')

    try: 
        title = hemisphere_soup.find('h2', class_="title").get_text()
        img_link = hemisphere_soup.find('a', text="Sample").get('href')
    except AttributeError:
        title = None
        img_link = None 
    hemisphere = {
        "title": title,
        "img_url": img_link
    }
    return hemisphere


    # # Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    return df.to_html(classes="table table-striped")



def scrape_all(): # main bot 
    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    news_title, news_p = news(browser)
    img_url = featured_img(browser)
    mars_weather = weather(browser)
    hemisphere_urls = hemisphere(browser)
    facts = mars_facts()
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": img_url,
        "hemispheres": hemisphere_urls,
        "weather": mars_weather,
        "facts": facts,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())







