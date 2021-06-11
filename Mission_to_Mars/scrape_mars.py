from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup as bs
import time
import requests
import pymongo
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}

    #News URL Scrape
    url = "https://redplanetscience.com"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    # Retrieve the latest news title
    news_title=soup.find_all('div', class_='content_title')[0].text
    # Retrieve the latest news paragraph
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text
    print(news_title)
    print(16*("-"))
    print(news_p)

    #JPL Image Scrape
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)
    #Find featured image
    featured_image_url = browser.find_by_tag('img[class="headerimage fade-in"]')[0]["src"]
    print(featured_image_url)

    #Mars Fact Scrape
    facts_url = "https://galaxyfacts-mars.com"
    browser.visit(facts_url)
    facts_table = pd.read_html(facts_url, header=0, index_col=0)
    trimmed_table = facts_table[0]
    trimmed_table

    #Mars Hemispheres Scrape
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hems = soup.find('div',class_='collapsible results')
    mars_item = mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]

    for i in mars_item:
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text

        #Image links from pages
        hemisphere_link = hemisphere.a["href"]
        browser.visit(hemi_url + hemisphere_link)
    
        html = browser.html
        soup = bs(html, "html.parser")
   

        image_link = soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
   
        #Dictionary
        image_dict={}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
    

        hemisphere_image_urls.append(image_dict)
    browser.quit()

    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(trimmed_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict