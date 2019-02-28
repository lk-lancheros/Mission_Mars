from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "chromedriver.exe"}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
 
    # A. MARS NEWS
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    html = browser.html
    # Create a Beautiful Soup object
    soup1 = BeautifulSoup(html, 'html.parser')
    # Identify and return title of latest news story and 'teaser' text
    news_title = soup1.find('div', class_="content_title").text      
    news_p = soup1.find('div', class_="rollover_description_inner").text
    
    # B. JPL MARS SPACE IMAGES
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    # Create a Beautiful Soup object
    soup2 = BeautifulSoup(html, 'html.parser')
    # Identify and return link to featured image
    temp = soup2.find('figure', class_='lede')
    img_partial = temp.find('a')['href']
    jpl_image_url = 'https://www.jpl.nasa.gov' + img_partial    
    
    # C. MARS WEATHER (TWITTER)
    # URL of page to be scraped
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup3 = BeautifulSoup(html, 'html.parser')
    temp = soup3.find('div', class_='js-tweet-text-container').find('p').text
    mars_weather=temp.split("pic")
    mars_weather= mars_weather[0]
    
    # D. MARS FACTS
    # URL of page to be scraped
    url4= 'http://space-facts.com/mars/'
    # Use read_html function in Pandas to automatically scrape any tabular data from a page
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Labels','Values']
    facts=df.to_dict()
    
    # E.MARS HEMISPHERES (TITLE AND IMAGE LINK)
    #URL of page to be scraped
    url5 = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced',
            'https://astrogeology   .usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
            'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
            'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced']

    hemi_image_url=[]
    title=[]

    for u in url5:
        browser.visit(u)
        html = browser.html
        #Create a Beautiful Soup object
        soup5=BeautifulSoup(html, 'html.parser')
        #Find the link to enhanced image
        temp = soup5.find('div', class_='downloads')
        hemi_image_url.append(temp.find('a')['href'])
        temp = soup5.find('div', class_='content')
        title.append(temp.find('h2').text)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "jpl_image_url": jpl_image_url,
        "mars_facts": facts,
        "mars_weather": mars_weather,
        "title": title,
        "hemi_image_url": hemi_image_url
    }

    print(mars_data)  

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
