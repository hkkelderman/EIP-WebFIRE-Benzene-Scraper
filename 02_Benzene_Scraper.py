#Libraries
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import zipfile
import time
import glob
import os
from datetime import date

#Fills out the search page
def search_page(start_date, end_date, CFR_Part, CFR_Subpart):
    """This function fills out the search page for EPA's Webfire Report Search.
    Parameters:
    start_date: the start date you want for your document search
    end_date: the end date you want for your document search
    CFR_Part: the regulatory part of interest
    CFR_Subpart: the regulatory subpart of interest"""

    date = driver.find_element_by_id('ui-id-3')
    date.click()
    time.sleep(2)
    
    search_start = driver.find_element_by_name("startdate")
    search_start.send_keys(start_date)
    search_end = driver.find_element_by_name("enddate")
    search_end.send_keys(end_date)
    
    reg = driver.find_element_by_id('ui-id-7')
    reg.click()
    time.sleep(2)
    
    part = Select(driver.find_element_by_id('CFRpart'))
    part.select_by_value(CFR_Part)
    time.sleep(5)
    
    subpart = Select(driver.find_element_by_id('CFRSubpart'))
    subpart.select_by_value(CFR_Subpart)

    submit = driver.find_element_by_id('Submit')
    submit.click()

#Pulls zip files from results page
def results_page():
    """This pulls the download links for each facility that appears on the results page as well as the document names."""
    page_links = []
    doc_names = []
    
    table = driver.find_element_by_id('myDocTable')
    docs = table.find_elements_by_tag_name('a')
    
    for doc in docs:
        page_links.append(doc.get_attribute('href'))
        doc_names.append(doc.get_attribute('title'))
    
    return page_links, doc_names

#Grabbing information from parameters spreadsheet
df = pd.read_excel('03_Parameters.xlsx')
start = df.start_date[0]
end = df.end_date[0]
part = df.CFR_Part[0]
subpart = df.CFR_Subpart[0]
page_count = df.pages[0]+1

#Scraping download links from Webfire Reports Page
driver_path = "C:/Users/kkelderman/Documents/Python Scripts/chromedriver.exe" #This should be changed to the location of your driver
driver = webdriver.Chrome(driver_path)
driver.get("https://cfpub.epa.gov/webfire/reports/esearch2.cfm")

search_page(start_date=start, end_date=end, CFR_Part=part, CFR_Subpart=subpart)
time.sleep(2)

link_list = []
name_list = []

for x in range(1,page_count):
    page_links, doc_names = results_page()
    link_list.append(page_links)
    name_list.append(doc_names)
    button = driver.find_element_by_id("myDocTable_next")
    button.click()
    time.sleep(2)

driver.quit()

all_links = [item for sublist in link_list for item in sublist]
all_names = [item for sublist in name_list for item in sublist]

new_names = []

for count, name in enumerate(all_names):
    new = '{}_{}'.format(count,name)
    new_names.append(new)

#Creating subfolder in directory for files to be downloaded
day = date.today().strftime("%b-%d-%Y")
dest = os.path.abspath(os.getcwd()) + '\\Downloads_{}'.format(day)
os.mkdir(dest)

#Downloading and unzipping the files from the scraped links
for i in range(0,len(all_links)):
    path = '{}\\{}'.format(dest,new_names[i]) 
    link = all_links[i]
    urllib.request.urlretrieve(link,path)

all_zips = glob.glob(dest + "\*.zip")

for zip_ in all_zips:
    prefix = zip_[71:74]
    zipdata = zipfile.ZipFile(zip_)
    zipinfos = zipdata.infolist()
    
    for zipinfo in zipinfos:
        zipinfo.filename = prefix + zipinfo.filename
        zipdata.extract(zipinfo, path='{}\\Unzipped_Files'.format(dest))
    
    zipdata.close()