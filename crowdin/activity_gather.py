#!/usr/bin/env python
# coding: utf-8

'''
TODO: replace sleeps with event handling
'''

import os
import yaml
import json

from time import sleep
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def wait_for_class(driver, item_class):
    delay = 5  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, item_class)))
    except TimeoutException:
        print('Reached timeout')


def wait_for_id(driver, item_id):
    delay = 5  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, item_id)))
    except TimeoutException:
        print('Reached timeout')


def prettify(html):
    print(BeautifulSoup(html, 'html.parser').prettify())


CROWDIN_PREFIX = 'https://crowdin.com'

driver = webdriver.Chrome()


# ----------- login ---------------
driver.get(CROWDIN_PREFIX + '/login')

env_path = os.path.join(os.environ['KA_HELPERS_REPO'], 'env.yaml')

with open(env_path, 'r') as fp:
    env = yaml.safe_load(fp)

driver.find_element_by_id('login_login').send_keys(env['crowdin']['user'])
driver.find_element_by_id('login_password').send_keys(env['crowdin']['pass'])
driver.find_element_by_id('login_password').send_keys(Keys.ENTER)
# --------------------------------

# ---------- Fist level activity gather -------------
url = 'https://crowdin.com/project/khanacademy/activity_stream'
driver.get(url)

wait_for_class(driver, 'list-activity')
elem = driver.find_element_by_id('result-languages-list')

elem.click()
sleep(1)
div_languages_filter = driver.find_element_by_id('languages-filter')

lang_input_field = div_languages_filter.find_element_by_tag_name('input')

lang_input_field.clear()
lang_input_field.send_keys("Ukra")
sleep(2)
lang_input_field.send_keys(Keys.RETURN)
sleep(3)

hats = driver.find_elements_by_class_name('static-icon-chevron-down')
for hat in hats:
    hat.click()
    sleep(0.2)

activity = driver.find_element_by_id('activity_stream')
activity = activity.find_element_by_tag_name('div')

activity_html = activity.get_attribute('innerHTML')

soup = BeautifulSoup(activity_html, 'html.parser')

user_activities = soup.contents[0]

summary = dict()

DATE_ITEM = 'line-activities-date'
PHRASE_SUGGESTED_ITEM = 'phrase_suggested'

last_day = ''
for i, item in enumerate(user_activities.contents):
    if DATE_ITEM in item['class']:
        current_date = item.string
        last_day = current_date

        if current_date not in summary.keys():
            summary[current_date] = dict()

    if PHRASE_SUGGESTED_ITEM in item['class']:
        entry = item.contents[1].contents[0].contents[2]
        if 'You suggested' in entry.get_text():
            title = 'Bohdan'
        else:
            title = entry.contents[0].contents[0].get_text()

        summary[current_date][title] = dict()
        summary[current_date][title]['hrefs'] = list()

        if len(item.contents) < 3:
            # this special case
            row_item = item.contents[1].contents[0].contents[2].contents[0].contents[2]
            href = row_item['href']
            summary[current_date][title]['hrefs'].append(href)
            continue

        translates = item.contents[2]
        translations_table = translates.contents[0].contents[1]

        for table_row in translations_table.contents:
            row_item = table_row.contents[0].contents[0]
            href = row_item['href']
            summary[current_date][title]['hrefs'].append(href)

# ---------------------------------

print('{} hats to click encountered.'.format(len(hats)))

# ------------ Second level of activity gather -----------------
i = 0
for day, activity in summary.items():
    i += 1
    print(day)
    for person, person_results in activity.items():
        print(person)
        
        if 'translaitons' not in person_results.keys():
            person_results['translations'] = list()
            
        print('Hrefs to work on: {}'.format(len(person_results['hrefs'])))
        for href in person_results['hrefs']:
            href = CROWDIN_PREFIX + href
            
            translation = {
                'source': None,
                'suggestions': list()
            }

            driver.get(href)
            driver.refresh()

            wait_for_id(driver, 'source_phrase_container')
            sleep(1)
            source_elem = driver.find_element_by_id('source_phrase_container')
            translation['source'] = source_elem.text

            suggestions = driver.find_elements_by_class_name('suggestion')

            for sug in suggestions:
                text = sug.find_elements_by_class_name('suggestion-text')[0].text
                author = 'Machine Translation'
                
                matches = sug.find_elements_by_class_name('author-name')
                if len(matches) > 0:
                    author = sug.find_elements_by_class_name('author-name')[0].text
                
                translation_suggestion = {
                    'author': author,
                    'text': text
                }
                
                translation['suggestions'].append(translation_suggestion)
            
            person_results['translations'].append(translation)

    print('-'*30)
# -----------------------------------------------------

with open('summary.json', 'w') as fp:
    json.dump(summary, fp)

print('Results are stored in summary.json')

driver.close()
