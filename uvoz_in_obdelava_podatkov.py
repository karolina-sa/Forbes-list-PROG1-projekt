#
# OBRAZLOŽITEV: v datoteki funkcija main() naredi dve .csv datoteki in sicer:
#                   - uvozi podatke s strani worldpopulation o državah ter njihovih gdp in številu prebivalcev, 
#                           jih prečisti in vrne .csv
#                   - že uvožene podatke o Forbes prečisti in vrne .csv. Uvoz podatkov Fobesove lestvice je v ločeni datoteki, 
#                           saj je za pravilno delovanje potrebno naložiti nekaj razširitev. 
#
# =================================================================================================================================================

import re
import os
import csv
import requests

# =================================================================================================================================================

# za Forbes:
directory = "Obdelani-podatki"
frontpage_filename = "output.html"
csv_filename = "forbes.csv"

# za worldpopulation:
url_wp = "https://worldpopulationreview.com/country-rankings/gdp-per-capita-by-country"
frontpage_filename_wp = 'worldpopulation.html'
csv_filename_wp = 'worldpopulation.csv'

# =================================================================================================================================================
# funckije za pridobivanje podatakov s spleta (za worldpopulation)
# =================================================================================================================================================

def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Napaka pri povezovanju do:", url)
        return None
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        print("Napaka pri prenosu strani:", url)
        return None

def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(directory, filename, url):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    text = download_url_to_string(url)
    save_string_to_file(text, directory, filename)
    return None

# =================================================================================================================================================
# sestavim vzorce za lažje iskanje želenih podatkov:
# =================================================================================================================================================

# za Forbes:

block_pattern = re.compile(                         # blok v katerem so podatki ene osebe
    r'<div class="personName" role="cell"'          # začetek vsakega bloka
    r'(.*?)</svg></span></div>\s*</div>\s*</div>',  # konec vsakega bloka
    flags=re.DOTALL
)

info_pattern = re.compile(
    r'style=".*?">\s*<div>(?P<name>.+?)\s</div>\s*</div>.*?'
    r'<div class="netWorth".*?"\s*style=".*?">\s*<div>(?P<networth>.+?)<div.*?'
    r'<div class="age".*?\s*style=".*?">\s*<div>(?P<age>.+?)</div>\s*.*?'
    r'<div class="countryOfCitizenship".*?"\s*style=".*?">\s*(?P<country>.+?)</div>.*?'
    r'<div class="source-column">\s*<div .*?><span\s*class="source-text">(?P<source>.+?)</span>.*?'
    r'<div class="category" .*?\s*style=".*?">\s*<div>(?P<industry>.+?)\s*<span\s*',
    flags=re.DOTALL
)

# za worldpopulation:

block_pattern_wp = re.compile(r'{"place"'
                    r'(.*?)"rank":\d*}',
                    re.DOTALL)

info_pattern_wp = re.compile(r'"pop2022":(?P<population>.+?),"growthRate".*?'
                    r'"country":"(?P<country>.+?)","cca3".*?'
                    r'"gdppc":(?P<gdp_pc>.+?),',
                    re.DOTALL)

# =================================================================================================================================================
# funkcije za pretvorbo niza v slovar:
# =================================================================================================================================================

# rabim za worldpopulation:

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()

f = read_file_to_string(directory, frontpage_filename)

# naslednje rabim za oboje:

def page_to_blocks(str, block_pattern):
    """Funkcija poišče posamezne bloke oseb oz. držav, ki se nahajajo v nizu ter vrne njihov seznam"""
    rx = block_pattern
    list = re.findall(rx, str)
    return list

def get_info_from_block(block, pattern):
    """Funkcija iz niza za posamezen blok osebe v primeru Forbes izlušči podatke o imenu,
    vrednosti (net worth), starosti, nacionalnosti, viru prihodka ter industriji kateri oseba priprada.
    V primeru worldpopulation pa izlušči podatke o imenu države,
    številu njenih prebivalcev in njenem GDP per capita.
    Vrne slovar, ki vsebuje želene podatke"""
    rx = pattern
    data = re.search(rx, block)
    dict = data.groupdict()
    return dict

def all_blocks(filename, block_pattern, info_pattern, directory):
    """Funkcija prebere podatke iz niza  in jih pretvori seznam slovarjev za vsako državo posebej."""
    page = read_file_to_string(directory, filename)
    blocks = page_to_blocks(page, block_pattern)
    countries = [get_info_from_block(block, info_pattern) for block in blocks]
    return countries

# za Forbes:

def list_of_dict():
    return all_blocks(frontpage_filename, block_pattern, info_pattern, directory)

# za worldpopulation:

def list_of_dict_wp():
    return all_blocks(frontpage_filename_wp, block_pattern_wp, info_pattern_wp, directory)

# =================================================================================================================================================
# funkcije za shranjevanje podatkov v .csv
# =================================================================================================================================================

def write_csv(fieldnames, rows, directory, filename):
    """ Funkcija ustvari .csv datoteko oblike:
    - prva vrstica so ključi slovarja (vsi slovarji imajo enake ključe)
    - vse ostale vrstice pa so podatki posameznih seznamov"""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

def write_info_to_csv(list_of_dict, directory, filename):
    """Funkcija podatke iz parametra "list_of_dict" - torej seznam slovarjev - zapiše 
    v .csv datoteko. Funkcija predpostavi, da so ključi vseh
    slovarjev parametra blocks enaki in je seznam blocks neprazen."""
    # Stavek assert preveri da zahteva velja. Če drži se program normalno izvaja, drugače pa sproži napako
    assert list_of_dict and (all(j.keys() == list_of_dict[0].keys() for j in list_of_dict))
    write_csv(list_of_dict[0].keys(), list_of_dict, directory, filename)

# =================================================================================================================================================
# 'zaključna' funkcija:
# =================================================================================================================================================

def main():
    """Funkcija naredi sledeče:
    - prebere podatke s spleta za worldpopulation,
    - .html datoteko pretvori v lepšo obliko (kot seznam slovarjev blokov) in
    - podatke shrani v .csv datoteko"""
    # Iz .html datoteke preberemo podatke in jih pretvorimo v seznam slovarjav
    #               list_of_dict() oz. list_of_dict_wp()
    # in podatke shranimo v .csv datoteko
    save_frontpage(directory, frontpage_filename_wp, url_wp) # preberemo s spleta podatke za worldpopulation
    write_info_to_csv(list_of_dict(), directory, csv_filename)
    write_info_to_csv(list_of_dict_wp(), directory, csv_filename_wp)

main()
