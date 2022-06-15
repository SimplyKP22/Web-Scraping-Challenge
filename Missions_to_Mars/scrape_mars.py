# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # ## NASA Mars News

    # In[3]:


    # Mars News Site to scrape
    mars_url = 'https://redplanetscience.com/'

    # visit the website
    browser.visit(mars_url)


    # In[4]:


    # Creating the BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[5]:


    # Print the html to confirm connection and review characteristics
    print(soup.prettify())


    # In[6]:


    # locate the attribute that contains the information we are looking for. In this case, the 'list_text' class contains
    # the information for the news title and the paragraph we want
    # Use the '.find' to default the search to the first occurance of the 'list_text' class
    news = soup.find('div', class_='list_text')
    print(news)


    # In[7]:


    # print the news_title
    news_title = news.find('div', class_='content_title')
    print(news_title.text)


    # In[8]:


    # print the news paragraph
    news_p = news.find('div', class_='article_teaser_body')
    print(news_p.text)
        


    # In[9]:


    # Close the browser after scraping
    browser.quit()


    # ## JPL Mars Space Images—Featured Image

    # In[10]:


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[11]:


    # Featured Space Image site to scrape
    rover_url = 'https://spaceimages-mars.com/'

    # visit the website
    browser.visit(rover_url)


    # In[12]:


    # Creating the BeautifulSoup object; parse with 'html.parser'
    html2 = browser.html
    soup = BeautifulSoup(html2, 'html.parser')


    # In[13]:


    # Search for the section of the page that contains the information we are looking for. In this case, the featured image
    area = soup.find('div', class_='floating_text_area')
    print(area)


    # In[14]:


    featured_image_url = rover_url + area.find('a')['href']
    featured_image_url


    # In[15]:


    # Close the browser after scraping
    browser.quit()


    # ## Mars Facts

    # In[16]:


    # Create a variable for the webpage we want to scrape
    url = 'https://galaxyfacts-mars.com/'

    # use the pd.read_html() method to scrape any tabular data from the page
    table = pd.read_html(url)
    table


    # In[17]:


    # Place the data from the scrape into a dataframe and display results to make sure we have the data we need
    df = table[0]
    df


    # In[18]:


    # Use Pandas to convert the data to a HTML table string.
    mars_facts_table = df.to_html()
    mars_facts_table


    # In[19]:


    # Strip unnecessary new lines 
    mars_facts_table.replace('\n', '')


    # ## Mars Hemispheres

    # In[20]:


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[21]:


    # The website that will be used for scraping the mars images
    url = 'https://marshemispheres.com/'

    # visit the site
    browser.visit(url)


    # In[22]:


    html3 = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html3, 'html.parser')


    # In[23]:


    # # Create a list that will house the dictionaries for the links to the high-resolution images 
    # for each hemisphere of Mars
    links = []
    hemisphere_image_urls = []

    # Search for the section of the page that contains the information we are looking for. In this case, the featured image
    area = soup.find_all('a', class_='itemLink')
    area

    for each in area:
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
            if url + link + href not in hemisphere_image_urls:
                hemisphere_image_urls.append(url + link + href)
        
        except:
            pass


    # In[24]:


    # Close the browser after scraping
    browser.quit()

    mars_data = {'news_title': news_title , 'news_p': news_p, 'featured_image_url': featured_image_url, 
                'mars_facts_table':mars_facts_table, 'hemisphere_image_urls':hemisphere_image_urls }
    mars_data

    # Return our dictionary
    return mars_data




