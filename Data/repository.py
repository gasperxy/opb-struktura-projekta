import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import datetime

from Data.models import transakcija, oseba, racun
from typing import List

## V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=5432)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dobi_transakcije(self) -> List[transakcija]:
        self.cur.execute("""
            SELECT id, racun, cas, znesek, opis
            FROM transakcija
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        transakcije = [transakcija.from_dict(t) for t in self.cur.fetchall()]
        return transakcije
    
    def dobi_osebe(self) -> List[oseba]:
        self.cur.execute("""
            SELECT emso, ime, priimek, rojstvo, ulica, posta
            FROM oseba
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
       # tt = [t for t in self.cur.fetchall()]
        osebe = [oseba.from_dict(t) for t in self.cur.fetchall()]
        return osebe
    
    def dobi_osebo(self, emso: str) -> oseba:
        self.cur.execute("""
            SELECT emso, ime, priimek, rojstvo, ulica, posta
            FROM oseba
            WHERE emso = %s
        """, (emso,))
         
        o = oseba.from_dict(self.cur.fetchone())
        return oseba
    
    def dobi_racun(self, emso: str) -> racun:
        self.cur.execute("""
            SELECT stevilka, lastnik
            FROM racun
            WHERE lastnik = %s
        """, (emso,))
         
        r = racun.from_dict(self.cur.fetchone())
        return r
    
    def dobi_transakcije_oseba(self, emso : str) -> List[transakcija]:
        racun = self.dobi_racun(emso)
        self.cur.execute("""
            SELECT id, racun, cas, znesek, opis
            FROM transakcija
            WHERE racun = %s
        """, (racun.stevilka,))
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        transakcije = [transakcija.from_dict(t) for t in self.cur.fetchall()]
        return transakcije
    
    def dodaj_transakcijo(self, t : transakcija):
        self.cur.execute("""
            INSERT into transakcija(znesek, racun, cas, opis)
            VALUES (%s, %s, %s, %s)
            """, (t.znesek, t.racun, t.cas, t.opis))
        self.conn.commit()

    


        


