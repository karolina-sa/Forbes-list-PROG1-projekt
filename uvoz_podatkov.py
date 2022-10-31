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
options.add_argument("--start-maximized") # ker mi sicer ni želelo klikati gumba za na naslednjo stran
# options.add_argument("--headless")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

driver.get(url) # gremo na spletno stran
time.sleep(5) # podaljšala, ker wifi ni delal OK

driver.find_element(by=By.ID, value="truste-consent-button").click() # potrdimo cookies
time.sleep(5)

# vseh strani (da gremo naprej) je 14
n = 13 # 13-krat pritisnemo gumb
html = '' # prazen niz v katerega bomo dodajali prebrane podatke
while n > 0: # prebrali bomo stran in nato bomo klikali na gumb (in brali stran) dokler ne gremo čez vseh 14 strani

    time.sleep(2) # počakamo da prebere
    html0 = driver.page_source # preberemo podatke iz trenutno odprte strani
    html += str(html0) # da dodajamo niz k nizu

    driver.find_element(By.XPATH, "//button[@class='pagination-btn pagination-btn--next ' and contains(., 'Next 200')]").click()

    n -= 1

# pridobljene podatke v .html obliki shranim v novo datoteko, da bom do njih lažje dostopala.
#          shranila sem kar v .html datoteko, da je datoteka po formatiranju bolj pregledna za 'luščenje' podatkov
with open("output.html", "w", encoding="utf-8") as file:
    file.write(str(html))