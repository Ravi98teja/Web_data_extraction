from selenium import webdriver
import urllib.request
import time
from IPython import embed
import re
import os
import wget


driver = webdriver.Chrome("//home/dell/PycharmProjects/selenium/chromedriver")
links = {}
articles = []

# def download_file(download_url, filepath):
#     wget.download(download_url, filepath)


def download_file(link, file_path, connection_timeout=10):
    print("downloading file " + link + " to " +
                file_path)
    try:
        r = requests.get(link, timeout=(connection_timeout, 90), verify=False)
        with open(file_path, 'wb+') as destination:
            destination.write(r.content)
    except:
        try:
            r = requests.get(link, timeout=(
                connection_timeout, 90), verify=False)
            with open(file_path, 'wb+') as destination:
                destination.write(r.content)
        except:
            print("unable to download file")
            print(file_path)
            return False
    print("downloaded " + link + " to " +
                file_path)
    return True


current_working_directory = os.curdir
if not os.path.exists(current_working_directory):
    os.makedir(current_working_directory,'pdfs')
pdf_path = current_working_directory + '/pdfs'
url = 'https://www.piie.com/research/publications/working-papers '
driver.get(url)
l = len(driver.find_elements_by_xpath('//*[@id="content"]/div[2]/div[2]/div'))

for i in range(1,l+1):
    time.sleep(2)
    links['Title '+str(i)] = driver.find_element_by_xpath("//*[@id='content']/div[2]/div[2]/div["+str(i)+"]/div/div[2]/h3/a").text
    links['Published_date '+str(i)] = driver.find_element_by_xpath("//*[@id='content']/div[2]/div[2]/div["+str(i)+"]/div/div[4]/span").text
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div['+str(i)+']/div/div[2]/h3/a').click()
    file_name = links['Title '+str(i)] + '.pdf'
    refined_name = file_name.replace(" ","_")
    file_path = os.path.join(pdf_path, refined_name)
    embed()
    try:
        
        url = driver.find_element_by_xpath('//*[@id="content"]/div/div[9]/span/a').get_attribute('href')
        download_file(url,file_path)
        print("downloaded successfully")
        driver.back()
    except:
        pass
        print("download failed")
        driver.back()
articles.append(links)
print(articles)



    