#!/usr/bin/env python
# coding: utf-8

# In[31]:


import requests
import pandas as pd
from bs4 import BeautifulSoup


# In[32]:


main_url = "http://books.toscrape.com/index.html"
result = requests.get(main_url)

result.text[:1000]


# In[33]:


soup = BeautifulSoup(result.text, 'html.parser')

print(soup.prettify()[:1000])


# In[34]:


def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)


# In[35]:


# soup.find("article", class_ = "product_pod")

soup.find("article", class_= "product_pod").div.a

soup.find("article", class_= "product_pod").div.a.get('href')


# In[36]:


main_page_products_urls = [x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")]

print(str(len(main_page_products_urls)) + " fetched products URLs")
print("One Example:")
print(main_page_products_urls[:5])


# In[47]:


def getBooksURLs(url):
    soup = getAndParseURL(url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])


# In[39]:


import re
pages_urls = [main_url]

soup = getAndParseURL(pages_urls[0])
# print(soup.prettify()[:1000])



while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
    new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")
    
    pages_urls.append(new_url)
    
    soup = getAndParseURL(new_url)
    
    
print(str(len(pages_urls)) + " fetched URLs")
print("some examples:")
print(pages_urls[:5])


# In[40]:


result = requests.get("http://books.toscrape.com/catalogue/page-50.html")
print("status code for page 50: " + str(result.status_code))
# no erro page


result = requests.get("http://books.toscrape.com/catalogue/page-51.html")
print("status code for page 50: " + str(result.status_code))
# 404 error page


# In[41]:


pages_urls = []

new_page = "http://books.toscrape.com/catalogue/page-1.html"
while requests.get(new_page).status_code == 200:
    pages_urls.append(new_page)
    new_page = pages_urls[-1].split("-")[0] + "-" + str(int(pages_urls[-1].split("-")[1].split(".")[0]) + 1) + ".html"
    

print(str(len(pages_urls)) + " fetched URLs")
print("Some examples:")
pages_urls[:5]


# In[48]:


booksURLs = []

for page in pages_urls:
    booksURLs.extend(getBooksURLs(page))
    
print(str(len(booksURLs))+ " fetched URLs")
print("some examples:")
booksURLs[:5]
    
    


# In[49]:


names = []
prices = []
nb_in_stock = []
img_urls = []
categories = []
ratings = []

for url in booksURLs:
    soup = getAndParseURL(url)
    
    #product name
    names.append(soup.find("div", class_ = re.compile("product_main")).h1.text)
    
    #product price
    prices.append(soup.find("p", class_ = "price_color").text[2:])
    
    # number of available products
    nb_in_stock.append(re.sub("[^0-9]", "", soup.find("p", class_ = "instock availability").text)) # get rid of non numerical characters
 
    # image url
    img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))
    
    # product category
    categories.append(soup.find("a", href = re.compile("../category/books/")).get("href").split("/")[3])

    # ratings
    ratings.append(soup.find("p", class_ = re.compile("star-rating")).get("class")[1])

# add data into pandas df
import pandas as pd

scraped_data = pd.DataFrame({'name': names, 'price': prices, 'nb_in_stock': nb_in_stock, "url_img": img_urls, "product_category": categories, "rating": ratings})
scraped_data.head()    


# In[ ]:


# Reference Info

# regular expression substitution
# re.sub: https://www.pythonforbeginners.com/regex/regular-expressions-in-python

# string split function        
# split function: https://www.w3schools.com/python/ref_string_split.asp        

# string join function
# https://www.programiz.com/python-programming/methods/string/join

