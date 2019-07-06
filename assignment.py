#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 10:10:53 2019

@author: manzar
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
import time
import pandas

url = "http://www.thailandstationery.com/%E0%B8%AA%E0%B8%A1%E0%B8%B2%E0%B8%8A%E0%B8%B4%E0%B8%81%E0%B8%81%E0%B8%A5%E0%B8%B8%E0%B9%88%E0%B8%A1%E0%B8%AF"
req = requests.get(url)
soup = BeautifulSoup(req.text, "lxml")
links = soup.findAll('a')
urls = []
for link in links[22:89]:
    ur = link.attrs['href']
    #print(url)
    urls.append(urljoin(url, ur))
    #print(link)
    
prefs = {
  "translate_whitelists": {"fr":"en"},
  "translate":{"enabled":"true"}
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
driver_location = "/home/manzar/Documents/chromedriver"
wb = webdriver.Chrome(driver_location, chrome_options=options)

wb.get(urls[0])
header = "Company name, Owner name, phone, fax, telephone, email, website\n"
file = open('assignment.csv', 'w')
file.write(header)
for url in urls:
    wb.get(url)
    time.sleep(1)
    html = wb.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'lxml')
    name = soup.findAll('h1', {'class': 'uk-text-large uk-margin-top uk-text-center'})
    name = name[0].text.replace('\n', '').strip()
    print(name)
    table = soup.findAll('table', {'class': 'uk-table uk-table-divider uk-table-small'})
    x = table[0].findAll('td')
    x = x[1::2]
    ow_name = x[0].text
    phone = x[7].text.strip().replace(',', '').replace(' ', ' | ')
    fax = x[8].text
    tel = x[9].text
    try:
        email = x[10].a.attrs['href'].replace('mailto:', '')
    except:
        email = 'NaN'
    try:
        web = x[11].a.attrs['href']
    except:
        web = 'NaN'
    print(name, ow_name, phone, fax, tel, email, web)
    file.write(name.replace(',', '') + ', ' + ow_name.replace(',', '') + ', ' + phone + ', ' + fax + ', ' + tel + ', ' + email + ', ' + web + '\n')
file.close()
file = pandas.read_csv('assignment.csv')