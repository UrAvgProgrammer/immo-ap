import pandas as pd
import csv
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

# # create excel file for results
# workbook = xlsxwriter.Workbook('Result.xlsx')
# worksheet = workbook.add_worksheet()

# # set headers
# worksheet.write("A1", "company_name")
# worksheet.write("B1", "email")
# worksheet.write("C1", "city")
# worksheet.write("D1", "street")
# worksheet.write("E1", "contanct_number")
# worksheet.write("F1", "managing_director")

# open the file in the write mode
f = open('immoscout-de-cat-1.csv', 'w')
writer = csv.writer(f)
writer.writerow(['company_name', 'email', 'contanct_number', 'street', 'zip', 'city'])

def scroll_down():
	# scroll down to bottom page to load all data
	y = 1000
	for timer in range(0,50):
		driver.execute_script("window.scrollTo(0, "+str(y)+")")
		y += 1000
		time.sleep(1)

def clean_data(text):
	res = text.split(': ')
	return res[1]

def get_neubau_provider_data(urls):
	for url in urls:
		#go to posting
		driver.get(url)

		# get company name
		# company_name = driver.find_element(By.CSS_SELECTOR, 'div[id="detailsContactFooter"] a').text
		# provider_name = driver.find_element(By.CSS_SELECTOR, 'div[id="detailsContactFooter"] p').text

		# #click to show phone number
		# wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="phoneContactFooter"] span'))).click()
		# time.sleep(3)
		# provider_contact_number = driver.find_element(By.CSS_SELECTOR, 'div[id="phoneContactFooter"] p.phone-number').text
		#get mpressum link

		impressum_selector = 'div.grid-item.one-whole span div.margin-top-m.align-center.with-icon a'
		impressum_url = driver.find_elements(By.CSS_SELECTOR, impressum_selector)[-1].get_attribute('href')

		driver.get(impressum_url)

		company = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/h3').text
		raw_email = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/p[4]').text
		email = clean_data(raw_email)
		raw_contact = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/p[3]').text
		contact_number = clean_data(raw_contact)
		street = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/p[1]').text
		city_zip = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/p[2]').text
		city = city_zip.split()[1]
		zip = city_zip.split()[0]

		#insert to csv
		writer.writerow([company, email, contact_number, street, zip, city])

		

def neubau(cities):
	posting_url = []
	#answer captcha and accept cookies increase time if needed
	driver.get('https://www.immobilienscout24.de/neubauprojekte/#/')
	time.sleep(20)

	#find search bar
	search_field = driver.find_element(By.CSS_SELECTOR, 'input[id="gac-field"]')
	for city in cities:
		search_field.click()
		search_field.clear()
		search_field.send_keys(city)
		time.sleep(20)
		search_result = '//*[@id="form"]/fieldset/div/div[1]/div/div/ul/li[2]'
		wait.until(EC.element_to_be_clickable((By.XPATH, search_result))).click()
		submit_button = 'div.grid-item.grid-item-with-fixed-width.palm-order-one-down.palm-one-whole button.button-primary.one-whole'
		wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button))).click()

		#simulate scroll to load all search result
		scroll_down()

		#get results
		posts = driver.find_elements(By.CSS_SELECTOR, 'ul.grid.grid-flex.gutter.ng-binding li a')
		for post in posts:
			posting_url.append(post.get_attribute('href'))

	#get provider data
	get_neubau_provider_data(posting_url)


def bauen(cities):
	driver.get('https://www.immobilienscout24.de/bauen/')

def main():
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


if __name__ == '__main__':
	neubau(['hamburg'])
	f.close()
	driver.close()
	driver.quit()