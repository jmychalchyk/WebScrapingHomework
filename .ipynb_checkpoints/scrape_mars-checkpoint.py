
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

def scrape():

    url ='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    nt1 = soup.find_all('div', class_="content_title")
    news_title=nt1.a.text.replace("\n","")
    p1 = soup.find('div', class_="rollover_description_inner")
    news_p=p1.text.replace("\n","")



    url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response2 = requests.get(url2)
    soup2 = bs(response2.text, 'html.parser')
    pic1 = soup2.find('article', class_="carousel_item")    
    pic = pic1['style']
    featured_image_url = 'https://www.jpl.nasa.gov' + pic[23:-3]



    url3="https://twitter.com/marswxreport?lang=en"
    response3 = requests.get(url3)
    soup3 = bs(response3.text, 'html.parser')
    twt1 = soup3.find('div', class_='js-tweet-text-container')     
    mars_weather = twt1.p.text



    url4='https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Category','Value']
    html_table = df.to_html()
    html_table.replace('\n', '')



    url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response5 = requests.get(url5)
    soup5 = bs(response5.text, 'html.parser')

    titles = soup5.find_all('div', class_='description')  
    tlst=[]
    for title in titles:
        tlst.append(title.text)

    refs = soup5.find_all('a', class_='itemLink product-item') 
    urlroot = 'https://astrogeology.usgs.gov'
    rlst=[]
    for ref in refs:
        url6= urlroot + ref['href']
        response6 = requests.get(url6)
        soup6 = bs(response6.text, 'html.parser')
        imgbig = soup6.find('div', class_='downloads') 
        rlst.append(imgbig.li.a['href'])

    hemisphere_image_urls = []
    for i in range(0,4):
        hemisphere_image_urls.append ({'title': tlst[i],'imgurl': rlst[i]}) 


    bigscrape ={'news title': news_title,
                'news paragraph':news_p,
                'featured image url':featured_image_url,
                'html table':html_table,
                'hemisphere image urls':hemisphere_image_urls}
    return bigscrape