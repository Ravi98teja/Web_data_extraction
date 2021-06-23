__author__ = 'ravi98teja'

#python library files are used in code
import os
import json
import logging
import sys
import time
import requests,shutil
import re


from selenium import webdriver
from IPython import embed
from datetime import date, datetime, timedelta

# setting up the chrome driver options

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

driver = webdriver.Chrome(executable_path='/home/dell/PycharmProjects/selenium/chromedriver',chrome_options = chrome_options)
driver.set_window_size(1920, 1080)

# load website and wait for 10 sec
url = "https://www.csis.org/analysis?&type=publication "
driver.get(url)
driver.implicitly_wait(10)

# Selecting the year of publications on filter
l = len(driver.find_elements_by_xpath('//*[@id="facetapi-facet-search-apidefault-node-index-block-field-publication-date"]/li'))
year = input("Please enter the year:")
for i in range(1,6):
    date_selection = driver.find_element_by_xpath('//*[@id="facetapi-facet-search-apidefault-node-index-block-field-publication-date"]/li['+str(i)+']').text
    if year in date_selection:
        driver.find_element_by_xpath('//*[@id="facetapi-facet-search-apidefault-node-index-block-field-publication-date"]/li['+str(i)+']').click()
        break

# count number of results that have appeared.
rows = len(driver.find_elements_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div/div'))
print("Total number of rows present: ",rows)


def download_pdf(url,name):
    """
    This function downloads the research paper in given folder.
    Input args: pdf url that is available on website and name which we want to save it
    Output: pdf file stored in given path
    Author : Raviteja N
    """
    folder_path = '/home/dell/client/pdfs/' + name + '.pdf'
    r = requests.get(url,verify=False,stream=True)
    r.raw.decode_content = True
    f = open(folder_path,'w')
    with open(folder_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)  
    
    print("----------------------")
    print("PDF downloaded for "+page_name)
    print("----------------------")

# looping over the entites where we can get the pdf 

page_numbers = int(input("Enter the number of pages you want to download: "))
for page in range(0,page_numbers):
    driver.get('https://www.csis.org/analysis?type=publication&field_publication_date=2021&page='+str(page))
    for i in range(1,rows+1):
        paper_name = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div/div['+str(i)+']').text.split("\n")[1]
        paper_name = '\"'+paper_name+'\"'
        
        time.sleep(5)
        paper_name_sulgified = re.sub(" ","_",paper_name)
        
        # To do download pdf and store them in folder 
        driver.find_element_by_xpath("//a[contains(text(),"+str(paper_name)+")]").click()
        
        try:
            pdf_link = driver.find_element_by_xpath("//a[contains(text(),'Download')]").get_attribute('href')
            print(pdf_link)
            time.sleep(5)

            download_pdf(pdf_link,paper_name)
            
            time.sleep(10)
            driver.back()
        except:
            print("-------------------------")
            print("No pdf for the paper: "+paper_name)
            print("-------------------------")
            time.sleep(5)
            driver.back()
        
driver.close()
