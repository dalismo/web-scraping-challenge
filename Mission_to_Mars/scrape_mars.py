from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd


def initiate_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
# NASA Mars News
    browser = initiate_browser()
    mars_dict={}

    url = "https://redplanetscience.com/"
    browser.visit(url)  

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()

# JPL Featured Image
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image_url = soup.find("img", class_="headerimage fade-in")["src"]

    image_url = image_url + featured_image_url 

# Mars Facts
    mars_facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(mars_facts_url)

    tables = pd.read_html(mars_facts_url)

    df = tables[1]

    df.columns = ['Description', 'Stats']

    html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)

# Mars Hemispheres
    hemis_url = "https://marshemispheres.com/"
    browser.visit(hemis_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    info = soup.find_all('div', class_='item')

    hemi_image_urls = []

    hemispheres_url = "https://marshemispheres.com/"

    for i in info: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_url + partial_img_url)
        partial_img_html = browser.html
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        img_url = hemispheres_url + soup.find('img', class_='wide-image')['src']
        hemi_image_urls.append({"title" : title, "img_url" : img_url})
        mars_dict ["hemispheres_info"] = hemi_image_urls
    
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":image_url,
        "fact_table":html_table,
        "hemisphere_images":hemi_image_urls
    }
    # Quit the browser
    browser.quit()

    return mars_dict
