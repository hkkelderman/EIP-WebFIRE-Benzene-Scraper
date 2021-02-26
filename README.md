## WebFIRE Benzene Scraper

#### Introduction

This is a Python script written to scrape fenceline benzene data from [EPA's WebFIRE Report Search](https://cfpub.epa.gov/webfire/reports/esearch2.cfm) page. Though this is specific to downloading the results from this search, the code can certainly be modified to bulk download other reports from other subsections of this webpage. This script works only on those results that return fewer than 500 records, as the pagination associated with results that have over 500 records is a bit more complicated and not accounted for in this program.

#### In this repository
1. **01_Benzene_Scraper_Notebook** - This Jupyter Notebook includes all the functions and code for the scraper, and can also be used to run the scraper if you prefer operating within a notebook. There is one section of the code that is highlighted and needs to be changed: the location of the chromedriver.
2. **02_Benzene_Scraper** - This is a python file that can be used to run the scraper without having to open up a Juptyer Notebook. The location of the chromedriver will need to be changed here as well. This file can just be run from the command line.
3. **03_Parameters** - This is an Excel file that can be used to change the inputs for the scraper. There are five inputs that can be changed, though in the case of scraping benzene data, you would only change the first two. The format for these four inputs are all as text.
    1.start_date: the start date you want for your search
    2.end_date: the end date you want for your search
    3.pages: the number of pages returned in your search results (you will need to run an initial search before running this script)
    4.CFR_Part: The main CFR Part of interest, in the case of benzene scraping, this should stay as 'Part 63'
    5.CFR_Subpart: The CFR subpart of interest, in the case of benzene scraping, this should stay as 'Subpart CC'
4. **requirements.txt** - This is a text file of the package requirements in order to run the app. 


#### Steps to using this app
1. Create a folder on the hard drive where you want to store the application and accompanying files and move them there.
2. Make sure you make the necessary changes to the **03_Parameters** spreadsheet as well as change the location of the chromedriver within the **02_Benzene_Scraper** file.
3. Open up a Command Prompt Window and navigate to the file where the scripts is located. Basic commands for command prompt navigation can be found [here](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands/).
4. Once you've navigated to the correct folder, run the following command: **pip install -r requirements.txt**. This makes sure all the requirements for the application are met.
5. Finally, you should be able to run the script using the command **python 02_Benzene_Scraper.py**

Note: This assumes you already have Python and Selenium's chromedriver installed on your hard drive.