
# TRENUTNO NAREJENO SAMO ZA PRVO STRAN (prvih 200 oseb) - UREDITI JE TREBA ŠE PREHOD S TIPKO 'NEXT'

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# med delom sem v cmd zaglana naslednje ukaze:
# pip install selenium
# pip install bs4
# pip install webdriver-manager
# pip3 install -U selenium
# pip install webdriver-manager

# naložila sem tudi Web drivers za Chrome (najnovejšo različico)

url = "https://www.forbes.com/billionaires/"

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

driver.get(url)
time.sleep(5) # podaljšala, ker wifi ni delal OK
driver.find_element(by=By.ID, value="truste-consent-button").click()
time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html, features="html.parser")

# print(soup)
# pridobljene podatke v .html obliki shranim v novo datoteko, da bom do njih lažje dostopala.
#          shranila sem kar v .html datoteko, da je datoteka po formatiranju bolj pregledna za 'luščenje' podatkov
with open("output.html", "w") as file:
    file.write(str(soup))

