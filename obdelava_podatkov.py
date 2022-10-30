import re
import os
import sys

# =================================================================================================================================================
# output.html prenesem v string:
def file_to_string(filename):
    """Funkcija vrne celotno vsebino datoteke filename kot niz"""
    with open(os.path.join(sys.path[0], filename), 'r', encoding='utf-8') as file: # ker je vse shranjeno v isti mapi
        return file.read()

# print(type(read_file_to_string("output.html"))) # vrne class 'str'
str = file_to_string("output.html")

# =================================================================================================================================================

# sestavim dva vzorca za lažje iskanje želenih podatkov:

block_pattern = re.compile(                         # blok v katerem so podatki ene osebe
    r'<div class="personName" role="cell"'          # začetek vsakega bloka
    r'(.*?)</svg></span></div>\s*</div>\s*</div>',  # konec vsakega bloka
    flags=re.DOTALL
)

info_pattern = re.compile(
    r'style=".*?">\s*<div>(?P<name>.+?)\s</div>\s*</div>.*?' 
    r'<div class="netWorth" role="cell"\s*style=".*?">\s*<div>(?P<networth>.+?)<div class="status">.*?'
    r'<div class="age" role="cell"\s*style="box-sizing: border-box; flex: 150 0 auto; min-width: 0px; width: 150px;">\s*<div>(?P<age>.+?)</div>\s*.*?'
    r'<div class="countryOfCitizenship" role="cell"\s*style=".*?">\s*(?P<country>.+?)</div>.*?'
    r'<div class="source-column">\s*<div class="expand-row__icon-container"><span\s*class="source-text">(?P<source>.+?)</span><span.*?'
    r'<div class="category" role="cell"\s*style=".*?">\s*<div>(?P<industry>.+?)<span class="expand-row__icon">.*?',
    flags=re.DOTALL
)

# =================================================================================================================================================

# funkciji s katerima si pomagamo pri pretvorbi niza v slovar:

def page_to_block(str):
    """Funkcija poišče posamezne bloke oseb, ki se nahajajo v nizu ter vrne njihov seznam"""
    rx = block_pattern
    list = re.findall(rx, str)
    return list

# print(len(razdelitev_niza_na_bloke(niz))) # res vrne 200 različnih blokov, torej ravno toliko kot jih mora
block = page_to_block(str)

def get_info_from_block(block):
    """Funkcija iz niza za posamezen blok osebe izlušči podatke o imenu,
    vrednosti (net worth), starosti, nacionalnosti, viru prihodka ter industriji kateri oseba priprada
    ter vrne slovar, ki vsebuje želene podatke"""
    rx = info_pattern
    data = re.search(rx, block)
    dict = data.groupdict()
    return dict

dict0 = get_info_from_block(block[0])
print(dict0)

# =================================================================================================================================================
