import pandas as pd
import xlsxwriter
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
# chrome_options.add_argument('--headless')

chrome_path = r".\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 20)

provider_names = []
posting_url = []

def scroll_down(driver):
	# scroll down to bottom page to load all data
	y = 1000
	for timer in range(0,50):
		driver.execute_script("window.scrollTo(0, "+str(y)+")")
		y += 1000
		time.sleep(1)

def scroll_to_paginate(driver):
	driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2)+50);")

def get_provider(driver):
	scroll_down(driver)

	# get the posting
	providers = driver.find_elements(
		By.CSS_SELECTOR,
		'div[data-test~="searchlist"] div.ProjectItem-0a128 a.mainSection-27481'
	)

	for provider in providers:
		prov_name = provider.find_element(
			By.CSS_SELECTOR,
			'div.FactsSection-1460e div.BrokerSection-ae4d6 div.ProviderName-b71b2 span'
		).text
		post_url = provider.get_attribute('href')

		if prov_name not in provider_names:
			print('inserting provider name: {}'.format(prov_name))
			provider_names.append(prov_name)
			print('inserting posting url: {}'.format(post_url))
			posting_url.append(post_url)

def run(url):
	driver.get(url)

	#check if there is next page
	has_next = True

	while has_next:
		time.sleep(5)
		# scroll down to bottom page to load all data
		get_provider(driver)

		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.arrowButton-20ae5')))
		next_button = driver.find_element(By.CSS_SELECTOR, 'button.arrowButton-20ae5')
		last_page = driver.find_elements(By.CSS_SELECTOR, 'div.Pagination-190de button')[-1].get_attribute('class')
		if next_button and last_page == 'arrowButton-20ae5':
			scroll_to_paginate(driver)
			time.sleep(5)
			driver.find_elements(By.CSS_SELECTOR, 'div.Pagination-190de button')[-1].click()
			# wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.arrowButton-20ae5'))).click()
			print('clicked next')
		else:
			has_next = False
			print('last page')



def main():
	driver.get(url)
	time.sleep(10)

	cities = [
	    'berlin', 'hamburg', 'muenchen', 'koeln', 'frankfurt-am-main', 'duesseldorf', 'stuttgart', 'dortmund', 'essen',
	    'leipzig', 'bremen', 'dresden', 'hannover', 'nuernberg', 'duisburg', 'bochum', 'wuppertal', 'bielefeld', 'bonn',
	    'muenster', 'karlsruhe', 'mannheim', 'augsburg', 'wiesbaden', 'gelsenkirchen', 'moenchengladbach', 'braunschweig',
	    'chemnitz-sachs', 'kiel', 'aachen', 'halle-saale', 'magdeburg', 'freiburg-im-breisgau', 'krefeld', 'luebeck-hansestadt',
	    'oberhausen', 'erfurt', 'mainz', 'rostock', 'kassel', 'hagen', 'hamm', 'saarbruecken', 'muelheim-an-der-ruhr', 'potsdam',
	    'ludwigshafen-am-rhein', 'oldenburg-oldenburg', 'leverkusen', 'osnabrueck', 'solingen', 'heidelberg', 'herne', 'neuss',
	    'darmstadt', 'paderborn', 'regensburg', 'ingolstadt', 'wuerzburg', 'fuerth', 'wolfsburg', 'offenbach-am-main', 'ulm',
	    'heilbronn', 'pforzheim', 'goettingen-niedersachs', 'bottrop', 'trier', 'recklinghausen-westf', 'reutlingen', 'bremerhaven',
	    'koblenz', 'bergisch-gladbac', 'jena', 'remscheid', 'erlangen', 'moers', 'siegen', 'hildesheim', 'salzgitter', 'kaiserslautern'
	    'schwerin'
	]
	methods = [
		'kaufen', 'mieten'
	]
	for method in methods:
		for city in cities:
			url = 'https://www.immowelt.de/liste/{}/immobilien/{}?sort=relevanz'.format(city, method)
			run(url)

if __name__ == '__main__':
	# main()
	run('https://www.immowelt.de/liste/hamburg/immobilien/kaufen?sort=relevanz')
	# driver.close()
	# driver.quit()