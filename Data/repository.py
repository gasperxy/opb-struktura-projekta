import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import datetime
import os

from Data.models import transakcija, oseba, osebaDto, racun, transakcijaDto, Uporabnik
from typing import List

# Preberemo port za bazo iz okoljskih spremenljivk
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

## V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dobi_transakcije(self) -> List[transakcija]:
        self.cur.execute("""
            SELECT id, racun, cas, znesek, opis
            FROM transakcija
            Order by cas desc
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        transakcije = [transakcija.from_dict(t) for t in self.cur.fetchall()]
        return transakcije
    
    def dobi_transakcijo(self, id) -> transakcija:
         self.cur.execute("""
            SELECT id, racun, cas, znesek, opis
            FROM transakcija
            Where id = %s
        """, (id,))
         
         t = transakcija.from_dict(self.cur.fetchone())
         return t

    
    def dobi_transakcije_dto(self) -> List[transakcijaDto]:
        self.cur.execute("""
            SELECT t.id, o.emso, o.ime || ' ' || o.priimek as oseba, t.racun, t.cas, t.znesek, t.opis
            FROM transakcija t 
            left join racun r on t.racun = r.stevilka
            left join oseba o on o.emso = r.lastnik
            Order by t.cas desc
        """)

        transakcije = [transakcijaDto.from_dict(t) for t in self.cur.fetchall()]
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

    def dobi_osebe_dto(self) -> List[osebaDto]:
        self.cur.execute("""
            SELECT emso, ime, priimek, rojstvo, ulica, posta, racun.stevilka as stevilka_racuna
            FROM oseba
            left join racun on racun.lastnik = oseba.emso 
                         
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
       # tt = [t for t in self.cur.fetchall()]
        osebe = [osebaDto.from_dict(t) for t in self.cur.fetchall()]
        return osebe
    
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

    def posodobi_transakcijo(self, t : transakcija):
        self.cur.execute("""
            Update transakcija set znesek = %s, racun = %s, cas=%s, opis = %s where id = %s
            """, (t.znesek, t.racun, t.cas, t.opis, t.id))
        self.conn.commit()

    def dodaj_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            INSERT into uporabniki(username, role, password_hash, last_login)
            VALUES (%s, %s, %s, %s)
            """, (uporabnik.username,uporabnik.role, uporabnik.password_hash, uporabnik.last_login))
        self.conn.commit()


    def dobi_uporabnika(self, username:str) -> Uporabnik:
        self.cur.execute("""
            SELECT username, role, password_hash, last_login
            FROM uporabniki
            WHERE username = %s
        """, (username,))
         
        u = Uporabnik.from_dict(self.cur.fetchone())
        return u
    
    def posodobi_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            Update uporabniki set last_login = %s where username = %s
            """, (uporabnik.last_login,uporabnik.username))
        self.conn.commit()



    


        


