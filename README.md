
Zagon projekta v Binderju: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gasperxy/opb-struktura-projekta/main?urlpath=proxy%2F8080)

# OPB struktura projekta
Pri načrtovanju aplikacije in strukturi programske kode se je dobro držati nekaterih osnovnih pravil. Obstaja veliko različnih pristopov, ki so odvisni od težavnosti ter potreb aplikacije. V tem repozitoriju je predstavljena glavna ideja tako imenovane **clean architecture** strukture aplikacije.
Glavne prednosti so:
* Lažji razvoj, če aplikacijo razvija več oseb hkrati
* Omogoča lažje (avtomatsko) testiranje aplikacije
* Namenjena je aplikacijam za katere se v prihodnosti pričakuje nadgradnje
* Novi razvijalci lažje najdejo pomembne in relevantne dele kode, ki ga potem lahko spreminjajo neodvisno od drugih delov aplikacije

Med drugim obstaja več različnih vzorcev za strukturiranje kode v projektu. Vsak vzorec ima svoje prednosti in slabosti. Pomembno je, da se z člani ekipe dogovorite kako boste strukturirali projekt. V firmah vam strukturo ter vzorce razložijo vaši mentorji, katerih morate ponavadi upoštevat. Samo na tak način je mogoče vzdrževati in nadgrajevati obstoječo aplikacijo z več 10000 vrsticami kode.
  
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

## Implementacija (Python)
Odvisno od zahtevnosti aplikacije so lahko posamezni nivoji aplikacije bodisi v svoji mapi (torej vključuje več datotek) bodisi je celotna logika nivoja implementirana v eni datoteki.
V ta namen si lahko pripravite naslednje mape:
* **Data** (vključuje datoteke za podatkovni nivo)
* **Services** (vključuje datoteke za aplikacijski nivo)
* **Presentation** (vključuje datoteke za predstavitveni nivo)

Več podrobnosti in primere si lahko ogledate v samem repozitoriju.

## Podatkovni nivo

Za namen projekta pri predmetu OPB bomo za dostop do baze postgres uporabljali Python knjižnjico `psycopg2`. V večjih in bolj kompleksnih aplikacij se za podobne namene ponavadi uporablja bolj zmogljive knjižnjice, ki omogočajo uporabo ORM pristopa.
Kljub temu, predlagam, da si podatkovne modele definirate kot Pythonove razrede oziroma bolj natančno `dataclass`, ki so del standardne Python distribucije `dataclasses`. Za pomoč pri delu z njimi vam je lahko tudi (dodatna) knjižnjica `dataclasses_json`, ki omogoča preprosto ustvarjanje dataclass razredov iz slovarja. To je zelo priročno, saj kot rezultat poizvedbe na postgres bazo ponavadi dobimo seznam slovarjev.

Primer preprostega data modela, ki predstavlja uporabnika v bazi:

```python
@dataclass
class Uporabnik:
    username: str = field(default="")
    role: str = field(default="")
    password_hash: str = field(default="")
    last_login: str = field(default="")
```


Ponavadi je navada, da je vsaka tabela v bazi en dataclass v Pythonu. Poleg tega pa aplikacija namesto osnovnega modela uporablja nekaj kar je imenuje DTO (database transffer object). V primeru uporabnika, nas seveda ne zanima polje `password_hash`. Zato ustvarimo še pripadajoč DTO kot:
```python
@dataclass
class UporabnikDto:
    username: str = field(default="")
    role: str = field(default="")
```

Osnovna ideja podatkovnega nivoja je interakcija z bazo. To torej pomeni, da je zadolžen za pridobivanje, zapisovanje, posodabljanje ter brisanje podatkov iz baze. Velikokrat take metode združimo v en (ali več) razredov, ki jih imenujemo **repozitorij**. Repozitorij imamo lahko en, lahko pa jih razdelimo glede na konteks. Naprimer lahko bi imeli naslednje repozitorije:
*  `UserRepository` : Zadolžen za prodobivanje ter dodajanje uporabnikov.
*  `TransactionRepository` : Zadolžen za pridobivanje ter dodajanje transakcij (v našo bazo banka).
*  ...
  
**OPOMBA**: Za namen podatkovnega skladišča ter uporabe v Plotly Dash knjižnjici, predlagam, da se izogneme modeliranju s pomočjo dataclasses.
V tem primeru je bolj primerno uporabljat `DataFrame` iz `Pandas` knjižnjice, saj je to ponavadi najbolj eleganten način za dodatno obdelavo ter prikaz podatkov.


Ideja repozitorija je torej, da hrani nabor funkcij za delo z bazo, kjer kot vhodni argument načeloma dobi DTO objekt, ki ga nato bodisi shrani/posodobi ali izbriše, ali pa kot vhod dobi id nekega objekta ter vrne pripadajoč DTO za ta objekt oziroma entiteto. Seveda lahko metode vračajo tudi seznam DTO-jev.

## Aplikacijski nivo

Aplikacijski nivo poskrbi za poslovno logiko aplikacije. Namen je, da poskrbi za vse možne omejitve aplikacije, ki jih ne moremo opisati direktno s strukturo baze. V ta namen uporablja repozitorije iz podatkovnega nivoja za interakcijo z bazo. V aplikacijskem nivoju ne sme biti nobenega klica na bazo. Podobno kot pri podatkovnem nivoju, nabor funkcij v podobnem kontekstu združimo v en razred, ki ga lahko poimenujemo `Service`. Seveda je smiselno imeti več različnih servisov za različne namene. Recimo:
* `AuthService` : Skrbi za prijavo ter dodajanje novih uporabnikov.
* `TransactionService`: Skrbi za dodajanje novih transakcij.
* ...

Kot primer lahko pokažemo kako bi z AuthService dodali novega uporabnika:

```python
from Data.repository import Repo
from Data.models import *
import bcrypt
from datetime import date


class AuthService:
    repo : Repo
    def __init__(self):
         self.repo = Repo()

    def dodaj_uporabnika(self, uporabnik: str, rola: str, geslo: str) -> UporabnikDto:

        # zgradimo hash za geslo od uporabnika

        # Najprej geslo zakodiramo kot seznam bajtov
        bytes = geslo.encode('utf-8')
  
        # Nato ustvarimo salt
        salt = bcrypt.gensalt()
        
        # In na koncu ustvarimo hash gesla
        password_hash = bcrypt.hashpw(bytes, salt)

        # Sedaj ustvarimo objekt Uporabnik in ga zapišemo bazo

        u = Uporabnik(
            username=uporabnik,
            role=rola,
            password_hash=password_hash.decode(),
            last_login= date.today().isoformat()
        )

        self.repo.dodaj_uporabnika(u)

        return UporabnikDto(username=uporabnik, role=rola)
```

## Predstavitveni nivo

Predstavitveni nivo je namenjen sprejemanju zahtev ter vizualnemu prikazu aplikacije. Predstavitveni nivo bi moral uporabljati samo razrede in metode iz 
aplikacijskega nivoja.

V primeru `bottle` knjižnjice (in splošnih spletnih aplikacij) je predstavitveni nivo sestavljen iz:
* `app.py` datoteke, ki sprejema vse zahtevke aplikacije
* `views` : html datoteke, ki jih napolnimo in prikažemo s pomočjo bottle knjižnjice
* `static` : statične datoteke kot css, js, ikone, logoti, itd.

Naloga prestavitvenega nivoja je, da sprejme podatke iz zahtevka, ter jih pošlje aplikacijskemu nivoju, da z njimi nekaj naredi.

Datoteka `app.py` je vhodna točka aplikacije, poleg tega pa je to datoteko treba zagnati, če hočemo zagnati aplikacijo. Zato se ta datoteka 
načeloma nahaja v korenu repozitorija oziroma projekta. Ostali deli predstavitvenega nivoja so zaradi jasnosti prestavljeni v podmaco Presentation (ali kaj drugega).


##
