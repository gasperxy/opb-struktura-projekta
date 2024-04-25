from Data.repository import Repo
from Data.models import *
from typing import List


# V tej datoteki bomo definirali razred za obdelavo in delo s transakcijami

class TransakcijeService:
    def __init__(self) -> None:
        # Potrebovali bomo instanco repozitorija. Po drugi strani bi tako instanco 
        # lahko dobili tudi kot input v konstrukturju.
        self.repo = Repo()

    def dobi_osebe(self) -> List[oseba]:
        return self.repo.dobi_osebe()
    
    def dobi_transakcije(self) -> List[transakcija]:
        return self.repo.dobi_transakcije()
    
    def dobi_transakcije_dto(self) -> List[transakcijaDto]:
        return self.repo.dobi_transakcije_dto()
    

    def naredi_transakcijo_oseba(self, o : oseba, znesek: float, opis: str) -> None:
       
        # Naredimo objekt za transakcijo.
        # Za to potrebujemo številko računa.

        r = self.repo.dobi_racun(o.emso)

        # Naredimo objekt za transakcijo
        t = transakcija(
            racun=r.stevilka,
            znesek=znesek,
            cas=datetime.now(),
            opis=opis
            )        
        # uporabimo repozitorij za zapis v bazo
        self.repo.dodaj_transakcijo(t)

    def naredi_transakcijo(self, racun: int, znesek: float, opis: str) -> None:
       
        # Naredimo objekt za transakcijo.
        # Za to potrebujemo številko računa.
        

        # Naredimo objekt za transakcijo
        t = transakcija(
            racun=racun,
            znesek=znesek,
            cas=datetime.now(),
            opis=opis
            )        
        # uporabimo repozitorij za zapis v bazo
        self.repo.dodaj_transakcijo(t)

    def izplacaj_nagrado(self, znesek: float, opis: str) -> None:

        # Vsek osebam bi radi izplačali nagrado.
        osebe = self.repo.dobi_osebe()
        for o in osebe:
            self.naredi_transakcijo_oseba(o, znesek, opis)
