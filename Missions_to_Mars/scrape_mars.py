
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Define a scrape function that will review several websites regarding the planet Mars and gather data
def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # ## NASA Mars News

    # Mars News Site to scrape
    mars_url = 'https://redplanetscience.com/'

    # visit the website
    browser.visit(mars_url)

    # Creating the BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Print the html to confirm connection and review characteristics
    print(soup.prettify())

    # locate the attribute that contains the information we are looking for. In this case, the 'list_text' class contains
    # the information for the news title and the paragraph we want
    # Use the '.find' to default the search to the first occurance of the 'list_text' class
    news = soup.find('div', class_='list_text')
    

    # print the news_title
    news_title = news.find('div', class_='content_title').text
 

    # print the news paragraph
    news_p = news.find('div', class_='article_teaser_body').text
   

    # Close the browser after scraping
    browser.quit()


    # ## JPL Mars Space Images—Featured Image

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # Featured Space Image site to scrape
    rover_url = 'https://spaceimages-mars.com/'

    # visit the website
    browser.visit(rover_url)

    # Creating the BeautifulSoup object; parse with 'html.parser'
    html2 = browser.html
    soup = BeautifulSoup(html2, 'html.parser')

    # Search for the section of the page that contains the information we are looking for. In this case, the featured image
    area = soup.find('div', class_='floating_text_area')
   
    featured_image_url = rover_url + area.find('a')['href']
  

    # Close the browser after scraping
    browser.quit()

    # Create a variable for the webpage we want to scrape
    url = 'https://galaxyfacts-mars.com/'

    # use the pd.read_html() method to scrape any tabular data from the page
    table = pd.read_html(url)
    

    # Place the data from the scrape into a dataframe and display results to make sure we have the data we need
    df = table[0]

    # Use Pandas to convert the data to a HTML table string.
    mars_facts_table = df.to_html()

    # Strip unnecessary new lines 
    mars_facts_table.replace('\n', '')

    # Setup splinter to review a different website
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # The website that will be used for scraping the mars images
    url = 'https://marshemispheres.com/'

    # visit the site
    browser.visit(url)

    html3 = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html3, 'html.parser')

    # # Create a list that will house the dictionaries for the links to the high-resolution images 
    # for each hemisphere of Mars
    links = []
    titles = []
    hemisphere_image_urls = []

    # Search for the section of the page that contains the information we are looking for. In this case, the featured image
    area = soup.find_all('a', class_='itemLink')


    for each in area:
        # Using a sleep function to assit with monitoring the splinter steps
        time.sleep(1)
        # Create a Try and except statement that will allow the program to run fully, and capture all the desired information 
        # while also passing over issues that may arise from encountering code that would cause the program to fail. 
        try:
            # using an if statement to avoid duplicating the links. 
            # We want to make sure the href is not already in the list
            link = each.get('href')
            if link not in links:
                links.append(link)
            browser.visit(url + link)
            
            # New page being referenced
            html3 = browser.html
            
            # Parse HTML with Beautiful Soup
            soup = BeautifulSoup(html3, 'html.parser')
            downloads_div = soup.find('div', class_='downloads')
            anchor = downloads_div.a
            href = anchor.get('href')
            cover_div = soup.find('div', class_='cover')
            title = cover_div.h2.text
            img = url + link + href
            if {"title": title, "img_url": img} not in hemisphere_image_urls:
                hemisphere_image_urls.append({"title": title, "img_url": img})
        except:
            pass


    # Create a dictionary that contains the variables for the information we wanted to scrape
    mars_data = {'news_title': news_title , 
                'news_p': news_p, 
                'featured_image_url': featured_image_url, 
                'mars_facts_table':mars_facts_table, 
                'hemisphere_image_urls':hemisphere_image_urls }

    # Close the browser after scraping
    browser.quit()

    # Return the results from the scrape function
    
    return mars_data


