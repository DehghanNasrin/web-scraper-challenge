from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd

def init_browser():

    exec_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', headless=True, **exec_path)

mars_info = {}

def scrape_mars_news():
    try:
        browser = init_browser()

        url = 'https://mars.nasa.gov/news/'

        browser.visit(url)
        
        html = browser.html

        soup = BeautifulSoup(html, 'html.parser')

        news_title= soup.find("div", class_="content_title").text

        news_p=soup.find("div", class_="article_teaser_body").text
        
        mars_info['news_title'] = news_title

        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

def scrape_mars_image():
    try:
        browser = init_browser()

        url_img="https://spaceimages-mars.com/"

        browser.visit(url_img)
        
        html_img= browser.html

        soup= BeautifulSoup(html_img, "html.parser")

        featured_image= soup.find("img", class_="headerimage fade-in")

        featured_image_url=url_img + featured_image["src"]
        
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()        

def scrape_mars_facts():
    try:

        browser = init_browser()

        url_facts="https://galaxyfacts-mars.com/"

        tables = pd.read_html(url_facts)

        df= tables[0]

        renamed_df=df.rename(columns={0:"Description", 1:"Mars", 2: "Earth"})

        reset_df=renamed_df.set_index("Description")

        html_table= reset_df.to_html()

        cleaned_html_table= html_table.replace("\n", " ")

        mars_info['mars_facts'] = cleaned_html_table

        return mars_info

    finally:

        browser.quit()  

def scrape_mars_hemispheres():
    try: 

        browser = init_browser()
        
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        
        browser.visit(hemispheres_url)

        html_hemispheres = browser.html

        soup = BeautifulSoup(html_hemispheres, 'html.parser')
        
        items = soup.find_all('div', class_='item')
        
        hiu = []
        
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        for i in items:            
            title = i.find('h3').text
            
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            browser.visit(hemispheres_main_url + partial_img_url)
            
            partial_img_html = browser.html
            
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu        

        return mars_info
    finally:

        browser.quit()