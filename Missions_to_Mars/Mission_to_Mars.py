#!/usr/bin/env python
# coding: utf-8

#import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re
import pymongo
from splinter import Browser
from flask import Flask, render_template

def initial_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = initial_browswer()
    mars_collection = {}
    
    #NASA url
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    #retrieve page
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'lxml')

    print(soup.prettify())

    # Retrieve the parent divs for all articles
    titles = soup.find_all('div', class_="content_title")
    titles

    #retrieve the child divs
    body = soup.find_all('div', class_='rollover_description')
    body

    #print news titles and paragraph
    results = soup.find_all('div', class_='slide')

    for result in results:
        titles=soup.find('div', class_='content_title')
        mars_collection['title']=titles.a.text
        mars_collection['body']=soup.find('div', class_='rollover_description_inner').text
      
    #URL for the feature image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url2)

    # find the image
    image = browser.find_by_id('full_image')
    image.click()

    # Find the info button and click it 
    browser.is_element_present_by_text('more info', wait_time =2)
    information = browser.find_link_by_partial_text('more info')
    information.click()

    html = browser.html
    image_soup= bs(html,'html.parser')

    image_soup

    #find the image
    find_image = image_soup.select_one('figure.lede a img').get("src")
    find_image

    #Build the image url
    mars_collection['final_image_url'] = f'https://www.jpl.nasa.gov{find_image}'
  
    #URL for Twitter
    import time
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    #retrieve page
    #response = requests.get(url3)
    html_twitter = browser.html
    time.sleep(5)
    #parse the website
    soup = bs(html_twitter, 'html.parser')

    print(soup.prettify())

    #Pull the tweet for Mars weather
    articles = soup.find_all("div", class_ = "css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-1mi0q7o")
    texts = [x.get_text() for x in articles[0].find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")]
    mars_collection['mars_weather'] = [i for i in texts if len(i)>25][0]
  
    #URL for Mars facts
    url4 = 'https://space-facts.com/mars/'

    #create a dataframe of Mars facts
    table = pd.read_html(url4)
    table[0]

    #cleaning the data
    table_df = table[0]
    table_df.columns = ["Facts", "Data"]
    table_df.set_index(["Facts"])
    table_df

    #writing the dataframe to a html
    table_html = table_df.to_html()
    table_html = table_html.replace("\n","")
    mars_collection['table']=table_html

    #URL for Mars hemispheres
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html_hemis=browser.html
    soup_hemis=bs(html_hemis, "html.parser")
    print(soup_hemis)

    #Finding the links for the images of the hemispheres and returning a list of links
    hemisphere = soup_hemis.find_all("div", class_="item")

    hemi_url = []
    # Core url to starore data
    core_url = 'https://astrogeology.usgs.gov'
    for x in hemisphere:
        #Store title
        title = x.find('h3').text
    
    #Store link that lead to full image
        temp_img =x.find('a', class_="itemLink product-item")['href']
    
    #visit the link
        browser.visit(core_url + temp_img)
        html_image = browser.html
        soup_hemis = bs(html_image, "html.parser")
    
        full_image = core_url + soup_hemis.find("img", class_="thumb")['src']
        
        hemi_url.append({"title": title,
                    "image_url": full_image})
    
    mars_collection['hemisphere_images'] = hemi_url

    return mars_collection
    




