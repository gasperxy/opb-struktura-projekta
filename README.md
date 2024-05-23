
Zagon projekta v Binderju: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gasperxy/opb-struktura-projekta/main?urlpath=proxy%2F8080)

# opb-struktura-projekta
Pri načrtovanju aplikacije in strukturi programske kode se je dobro držati nekaterih osnovnih pravil. Obstaja veliko različnih pristopov, ki so odvisni od težavnosti ter potreb aplikacije. V tem repozitoriju je predstavljena glavna ideja tako imenovane **clean architecture** strukture aplikacije.
Glavne prednosti so:
* Lažji razvoj, če aplikacijo razvija več oseb hkrati
* Omogoča lažje (avtomatsko) testiranje aplikacije
* Namenjena je aplikacijam za katere se v prihodnosti pričakuje nadgradnje
* Novi razvijalci lažje najdejo pomembne in relevantne dele kode, ki ga potem lahko spreminjajo neodvisno od drugih delov aplikacije

  
## Osnovna ideja clean architecture strukture
  
Kodo aplikacije razdelimo na več nivojev, ki se ponavadi imenujejo:
  * **podatkovni nivo** ( data layer, entites,..) kjer so implementirane metode za povezavo do baze ter definicije posameznih podatkovnih modelov
  * **aplikacijski nivo** (service layer, business layer, use cases,...), kjer je implementirana aplikacijska logika. Na tem nivoju ni direktne povezave do baze, ampak se uporablja podatke in modele dobljene iz podatkovnega nivoja.
  *  **predstavitveni nivo** (presentation layer,...), kjer se funkcionalnost aplikacije predstavi uporabnikom oziroma napravam. To vključuje razne html strani, REST Api povezave in podobno. V tem nivoju se ponavadi uporablja le preproste klice iz aplikacijskega nivoja.

Vizualno lahko to predstavimo s spodnjo shemo
<p align="center">
      <img width="200" height="450" src="https://github.com/gasperxy/opb-struktura-projekta/assets/3481918/3a227b87-81b7-41a9-b81c-306a00ab5330">
    </p>

Več informacij lahko najdete recimo na https://www.freecodecamp.org/news/a-quick-introduction-to-clean-architecture-990c014448d2/

## Implementacija (V Python-u)
Odvisno od zahtevnosti aplikacije so lahko posamezni nivoji aplikacije bodisi v svoji mapi (torej vključuje več datotek) bodisi je celotna logika nivoj implementirana v eni datoteki.
V ta namen si lahko pripravite naslednje mape:
* Data (vključuje datoteke za podatkovni nivo)
* Services (vključuje datoteke za aplikacijski nivo)
* Presentation (vključuje datoteke za predstavitveni nivo)

Več podrobnosti in primere si lahko ogledate v repozitoriju.

## Podatkovni nivo

Za namen projekta pri predmetu OPB bomo za dostop do baze postgres uporabljali Python knjižnjico `psycopg2`. V večjih in bolj kompleksnih aplikacij se za podobne namene ponavadi uporablja bolj zmogljive knjižnjice, ki omogočajo uporabo ORM pristopa.
Kljub temu, predlagam, da si podatkovne modele definirate kot Pythonove razrede oziroma bolj natančno `datamodels`, ki so del standardne Python distribucije. Za pomoč pri delu z njmi vam je lahko tudi (dodatna) knjižnjica `dataclasses_json`, ki omogoča preprosto ustvarjanje dataclass razredov iz slovarja. To je zelo priročno, saj kot rezultat poizvedbe na postgres bazo ponavadi dobimo seznam slovarjev.

