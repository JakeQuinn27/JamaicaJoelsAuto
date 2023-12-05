from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv


import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

import json

import requests

from email.message import EmailMessage
import ssl
import smtplib
from smtplib import SMTP_SSL
import os

'''
headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Authorization': 'Basic c29yZW46MVJ1bnRoaXN0b3du',
    'Accept-Language': 'en-US,en;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'api.greenbits.com',
    'Origin': 'https://secure.greenbits.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Referer': 'https://secure.greenbits.com/',
    'Connection': 'keep-alive',
    'X-GB-Web-Path': '/sessions/new',
    'X-Requested-With': 'XMLHttpRequest',
    'X-GB-CompanyId': 'null',
    'X-GB-Client': 'herer-web 2e1e8f1fa1',
}

response = requests.get('https://api.greenbits.com/api/v2/me', headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

array = json.loads(response.content)

userId = array['user']['id']
data = {
    'username': 'soren',
    'password': '1Runthistown',
    'id': userId
}

with requests.session() as s:
    session = HTMLSession()
    s.post('https://api.greenbits.com/api/v2/me', data=data)
    #r = requests.get('https://secure.greenbits.com/reports/sales-by?column=account&groupBy=employee&interval=week&report=discount_plan')
    test = session.get('https://secure.greenbits.com/reports/sales-by?column=account&groupBy=employee&interval=week&report=discount_plan')
    test.html.render()

    print(test.html.html)

session = HTMLSession()
session.post('https://secure.greenbits.com/sessions/new', data=data)
test = session.get('https://secure.greenbits.com/reports/sales-by?column=account&groupBy=employee&interval=week&report=discount_plan')
test.html.render()

print(test.html.html)





# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '[{"startDate":1700072068891,"endDate":1700072068891,"features":{"ENG-45166-polling-tasks-interval":{"default":60,"counters":[{"value":60,"count":1,"variation":1,"version":3}]}},"kind":"summary"}]'
#response = requests.post('https://events.launchdarkly.com/events/bulk/598352885d265b0cdab84a56', headers=headers, data=data)



# br.select_form(ls_form='fb-init')



# with requests.session() as s: # Use a Session object.
#     login = requests.post("https://secure.greenbits.com/sessions/new", data=data)
#
#     print(login.text)
'''








#Selenium webdriver Backup Script


USERNAME = 'soren'
PASSWORD = '1Runthistown'
loginURL = 'https://secure.greenbits.com/sessions/new'
secureURL = 'https://secure.greenbits.com/reports/sales-by?column=account&interval=week&report=discount_plan&sortBy=Sales&sortDirection=desc'


chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('prefs',{"download.default_directory": "/Users/jakequinn/Desktop/GitHub/Jamaica Joels Auto/Drops Auto Email"})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chromeOptions)

driver.get(loginURL)


u_name = driver.find_element(By.NAME, "username")
u_name.click()
u_name.send_keys(USERNAME)

p_word = driver.find_element(By.NAME, "password")
p_word.click()
p_word.send_keys(PASSWORD)

driver.find_element(By.CLASS_NAME, "btn-text").click()

#driver.find_element(By.CLASS_NAME, "sr-only").click()

time.sleep(4)

driver.find_element(By.LINK_TEXT, "Insights").click()

time.sleep(4)


driver.find_element(By.XPATH, '//*[@data-test-link="reorder_report_export"]').click()

time.sleep(4)


driver.find_element(By.LINK_TEXT, "Best Performing Discounts").click()

time.sleep(4)

driver.find_element(By.CLASS_NAME, "col-md-3").click()

time.sleep(4)

driver.find_element(By.XPATH, '//*[@value="yesterday"]').click()

time.sleep(4)

driver.find_element(By.XPATH, '//*[@title="Update Report"]').click()

time.sleep(4)

driver.find_element(By.XPATH, '//*[@data-test-action="download_csv"]').click()

time.sleep(10)

emailpass = 'ovdj qzne lkdy phxo'
email_sender = 'JamaicaJake27@gmail.com'

email_receiver = 'jakeq12345@icloud.com'


subject = "Testing email Automation"

voucher = 0

with open('best_performing_discounts.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for i in reader:
        if i[0] == '15% Student' and i[1] == 'Discounts':
            voucher = float(i[2])

body = f"""
JamaicaJake Auto Email test take 1
Yesterday, the 15% Student discount gave out {voucher} $$$
"""

emailpass = 'ovdj qzne lkdy phxo'
email_sender = 'JamaicaJake27@gmail.com'

email_receiver = 'dashboard@jamaicajoels.com'


subject = "Testing email Automation"

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['subject'] = subject
em.set_content(body)

context = ssl.create_default_context()




#em.add_attachment(csv_reader, maintype='image', subtype=file_type, filename=file_name)



with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, emailpass)
    smtp.sendmail(email_sender, email_receiver, em.as_string())








