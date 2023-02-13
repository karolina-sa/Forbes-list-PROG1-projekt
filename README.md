# PROG1-projekt
## Forbes: The Richest People In The World
Forbesova lestvica je mednarodno uveljavljena lestvica podjetij in posameznikov, ki se določi glede na njihovo finančno stanje in bogastvo. Je seznam najbogatejših ljudi (milijarderjev) na svetu, ki ga letno objavlja revija Forbes.  
### Kratka predstavitev dela:
V projektni nalogi sem analizirala Forbesovo lestvico, torej vse osebe katerih premožnje je 1 milijarda USD ali več. Podatke sem črpala s strani [Forbes](https://www.forbes.com/billionaires/), kjer lahko najdemo lestvico 2600 najbogatejših oseb. Za potrebe boljše analiza pa sem pridobila še podatke o številu prebivalcev in BDP per capita vseh držav sveta. Slednji so bili pridobljeni s strani [World Population Review](https://worldpopulationreview.com/country-rankings/gdp-per-capita-by-country). Vsi podatki so bili zbrani v drugi polovici oktobra 2022.

Za vsako osebo z lestvice sem pridobila podatke o imenu, premoženju, starosti, nacionalnosti, viru dohodka ter industiji vira dohodka. Relavantni so bili vsi podatki, razen imen oseb, saj jih v ananlizi nisem nikjer uporabila. Za vsako državo sveta pa sem zajela podatke o številu prebivalcev ter BDP per capita

Analizo Forbesove lestvice so motivirala naslednja vprašanja in povezave med njimi:
- Katere države iztopajo po številu milijarderjev?
- V kateri starostni skupini je največ milijarderjev?
- Kateri industriji pripada največ oseb z lestvice?
- Kateremu podjetju pripada največ oseb Forbesove lestvice?

V poročilu sem odgovorila na zgornja vprašanja in analizirala še marsikatero drugo povezano temo. 

### Sestava projektna naloge:
**1. Uvoz in obdelava podatkov:** <br/>

Uvoz in obdelava podatkov je napisana v programskem jeziku [Python](https://www.python.org/). Ključno vlogo pri uvozu podatkov je igrala knjižnica [Selenium](https://selenium-python.readthedocs.io/), ki mi je omogočila zajetje podatkov s strani [Forbes](https://www.forbes.com/billionaires/).
- uvoz podatkov Forbesove lestvice je v datoteki `uvoz_podatkov_Forbes.py` (podatki o tem kaj si je potrebno naložiti za pravilno delovanje so napisani tekom kode/postopka),
- uvoz podatkov o državah in obdelava vseh podatkov (pretvorba v `.csv`) je v datoteki `uvoz_in_obdelava_podatkov.py`,
- vsi uvoženi (v `.html` obliki) in obdelani (v `.csv` obliki) podatki so v mapi `Obdelani-podatki`. <br/>

**2. Vizualizacija in poročilo:** 
- poročilo je v datoteki `analiza_Forbes_list.ipynb`, kjer je tudi koda za vizualizacijo podatkov,
- poročilo se lahko v lepši obliki (brez Python kode) bere v datoteki `analiza_Forbes_list.html`.
