# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 16:45:19 2021

@author: Toshiba
"""


import job_scraper
from job_scraper import find_jobs_from

desired_characs = ['titles', 'companies', 'links', 'date_listed']


find_jobs_from('careersinafrica', 'data scientist', 'london', desired_characs) #Extracting jobs from careersinafrica.com



find_jobs_from('CWjobs', 'data scientist', 'london', desired_characs)#Extracting jobs from CWjobs.co.uk (using Selenium)