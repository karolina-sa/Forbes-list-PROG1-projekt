from fileinput import filename
import re
import os
import sys
import csv

# =================================================================================================================================================

# output.html prenesem v string:
def file_to_string(filename):
    """Funkcija vrne celotno vsebino datoteke filename kot niz"""
    with open(os.path.join(sys.path[0], filename), 'r') as file: # ker je vse shranjeno v isti mapi
        return file.read()

# print(type(read_file_to_string("output.html"))) # vrne class 'str'
filename = "output.html"
str = file_to_string(filename)

# =================================================================================================================================================
# sestavim dva vzorca za lažje iskanje želenih podatkov:
# =================================================================================================================================================

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

# =================================================================================================================================================
# funkcije za pretvorbo niza v slovar:
# =================================================================================================================================================

def page_to_blocks(str):
    """Funkcija poišče posamezne bloke oseb, ki se nahajajo v nizu ter vrne njihov seznam"""
    rx = block_pattern
    list = re.findall(rx, str)
    return list

# print(len(page_to_blocks(str))) # res vrne 200 različnih blokov, torej ravno toliko kot jih mora
blocks = page_to_blocks(str)

def get_info_from_block(block):
    """Funkcija iz niza za posamezen blok osebe izlušči podatke o imenu,
    vrednosti (net worth), starosti, nacionalnosti, viru prihodka ter industriji kateri oseba priprada
    ter vrne slovar, ki vsebuje želene podatke"""
    rx = info_pattern
    data = re.search(rx, block)
    dict = data.groupdict()
    return dict

dict0 = get_info_from_block(blocks[124])
# print(dict0)

def all_blocks(filename):
    """Funkcija prebere podatke iz niza  in jih pretvori seznam slovarjev za vsako osebo posebej."""
    page = file_to_string(filename)
    blocks = page_to_blocks(page)
    people = [get_info_from_block(block) for block in blocks]
    return people

# print(all_blocks(filename))

def list_of_dict():
    return all_blocks(filename)

# =================================================================================================================================================
# funkcije za shranjevanje podatkov v .csv
# =================================================================================================================================================

directory_name = "Obdelani-podatki"
csv_filename = "forbes.csv"

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

def write_people_info_to_csv(list_of_dict, directory, filename):
    """Funkcija podatke iz parametra "list_of_dict" - torej seznam slovarjev - zapiše 
    v .csv datoteko. Funkcija predpostavi, da so ključi vseh
    slovarjev parametra blocks enaki in je seznam blocks neprazen."""
    # Stavek assert preveri da zahteva velja. Če drži se program normalno izvaja, drugače pa sproži napako
    assert list_of_dict and (all(j.keys() == list_of_dict[0].keys() for j in list_of_dict))
    write_csv(list_of_dict[0].keys(), list_of_dict, directory, filename)

# write_people_info_to_csv(list_of_dict(), directory_name, csv_filename)

# =================================================================================================================================================
# 'zaključna' funkcija:
# =================================================================================================================================================

def main():
    """Funkcija naredi sledeče:
    - že narejeno .html datoteko pretvori v lepšo obliko (kot seznam slovarjev blokov)
    - podatke shrani v .csv datoteko"""
    # Iz .html datoteke preberemo podatke in jih pretvorimo v seznam slovarjav
    #               list_of_dict()
    # in podatke shranimo v .csv datoteko
    write_people_info_to_csv(list_of_dict(), directory_name, csv_filename)

main()
