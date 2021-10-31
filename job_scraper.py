# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 by chrislovejoy
Adapted by Regen Petu-Stiles
"""
'''
This code extracts all the desired characteristics of all new job postings
    of the title and location specified and returns them in single file.
I have focused on two websites
    The arguments it takes are:
        - Website: to specify which website to search (options: 'careersinafrica' or 'CWjobs')
        - Job_title
        - Location
        - Desired_characs: this is a list of the job characteristics of interest,
            from titles, companies, links and date_listed.
        - Filename: to specify the filename and format of the output.
            Default is .csv file called 'results.csv'
'''
"""
Example code
import job_scraper
from job_scraper import find_jobs_from
desired_characs = ['titles', 'companies', 'links', 'date_listed']
find_jobs_from('careersinafrica', 'data scientist', 'london', desired_characs) #Extracting jobs from careersinafrica.com
find_jobs_from('CWjobs', 'data scientist', 'london', desired_characs)#Extracting jobs from weworkremotely.com (using Selenium)
"""

import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os
import re

def find_jobs_from(website, job_title, location, desired_characs, filename="results.csv"):    
    """
    This function extracts all the desired characteristics of all new job postings
    of the title and location specified and returns them in single file.
    The arguments it takes are:
        - Website: to specify which website to search (options: 'careersinafrica' or 'weworkremotely.com')
        - Job_title
        - Location
        - Desired_characs: this is a list of the job characteristics of interest,
            from titles, companies, links and date_listed.
        - Filename: to specify the filename and format of the output.
            Default is .csv file called 'results.csv'
    """
    
    if website == 'careersinafrica':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information_indeed(job_soup, desired_characs)
    
    if website == 'weworkremotely':
        location_of_driver = os.getcwd()
        driver = initiate_driver(location_of_driver, browser='chrome')
        job_soup = make_job_search(job_title, location, driver)
        jobs_list, num_listings = extract_job_information_cwjobs(job_soup, desired_characs)
    
    save_jobs_to_excel(jobs_list, filename)
 
    print('{} new job postings retrieved from {}. Stored in {}.'.format(num_listings, 
                                                                          website, filename))
    

## ======================= GENERIC FUNCTIONS ======================= ##

def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)


## ================== FUNCTIONS FOR careersinafrica =================== ##

def load_indeed_jobs_div(job_title, location):

    getVars = {'q' : job_title, 'l' : location, 'fromage' : 'last', 'sort' : 'date'}
    url = ('https://www.careersinafrica.com/job-search/' + urllib.parse.urlencode(getVars))
    url.format(getVars)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html5lib")
    job_soup = soup.find(id="resultsCol")
    
    return job_soup

def extract_job_information_indeed(job_soup, desired_characs):

    job_soup = soup.find(id="resultsCol")
    job_elems = job_soup.find_all('div', class_='jobsearch-SerpJobCard')
     
    
    cols = []
    extracted_info = []
    
    
    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)                    
    
    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)
    
    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)
    
    if 'date_listed' in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_indeed(job_elem))
        extracted_info.append(dates)
    
    jobs_list = {}
    
    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]
    
    num_listings = len(extracted_info[0])
    
    return jobs_list, num_listings


def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_='title')
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='company')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'www.careersinafrica.com/' + link
    return link

def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date



## ================== FUNCTIONS FOR weworkremotely.com=================== ##
    

def initiate_driver(location_of_driver, browser):
    if browser == 'chrome':
        driver = webdriver.Chrome(executable_path=(location_of_driver + "/chromedriver"))
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=(location_of_driver + "/firefoxdriver"))
    elif browser == 'safari':
        driver = webdriver.Safari(executable_path=(location_of_driver + "/safaridriver"))
    elif browser == 'edge':
        driver = webdriver.Edge(executable_path=(location_of_driver + "/edgedriver"))
    return driver

def make_job_search(job_title, location, driver):
    driver.get('https://weworkremotely.com/remote-jobs')
    
    # Select the job box
    job_title_box = driver.find_element_by_name('Keywords')

    # Send job information
    job_title_box.send_keys(job_title)

    # Selection location box
    location_box = driver.find_element_by_id('location')
    
    # Send location information
    location_box.send_keys(location)
    
    # Find Search button
    search_button = driver.find_element_by_id('search-button')
    search_button.click()

    driver.implicitly_wait(5)

    page_source = driver.page_source
    
    job_soup = BeautifulSoup(page_source, "html.parser")
    
    return job_soup


def extract_job_information_cwjobs(job_soup, desired_characs):
    
    job_elems = job_soup.find_all('div', class_="job")
     
    cols = []
    extracted_info = []
    
    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_cwjobs(job_elem))
        extracted_info.append(titles) 
                           
    
    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_cwjobs(job_elem))
        extracted_info.append(companies)
    
    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_cwjobs(job_elem))
        extracted_info.append(links)
                
    if 'date_listed' in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_cwjobs(job_elem))
        extracted_info.append(dates)    
    
    jobs_list = {}
    
    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]
    
    num_listings = len(extracted_info[0])
    
    return jobs_list, num_listings


def extract_job_title_cwjobs(job_elem):
    title_elem = job_elem.find('h2')
    title = title_elem.text.strip()
    return title
 
def extract_company_cwjobs(job_elem):
    company_elem = job_elem.find('h3')
    company = company_elem.text.strip()
    return company

def extract_link_cwjobs(job_elem):
    link = job_elem.find('a')['href']
    return link

def extract_date_cwjobs(job_elem):
    link_elem = job_elem.find('li', class_='date-posted')
    link = link_elem.text.strip()
    return link


"""
Example code
import job_scraper
from job_scraper import find_jobs_from
desired_characs = ['titles', 'companies', 'links', 'date_listed']
find_jobs_from('careersinafrica', 'data scientist', 'london', desired_characs) #Extracting jobs from careersinafrica.com
find_jobs_from('weworkremotely', 'data scientist', 'london', desired_characs)#Extracting jobs from CWjobs.co.uk (using Selenium)
"""
#from job_scraper import find_jobs_from

desired_characs = ['titles', 'companies', 'links', 'date_listed']


find_jobs_from('careersinafrica', 'data scientist', 'london', desired_characs) #Extracting jobs from careersinafrica.com



find_jobs_from('weworkremotely', 'data scientist', 'london', desired_characs)#Extracting jobs from CWjobs.co.uk (using Selenium)
