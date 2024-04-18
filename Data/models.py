
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

# V tej datoteki definiramo vse podatkovne modele, ki jih bomo uporabljali v aplikaciji
# Pazi na vrstni red anotacij razredov!

@dataclass_json
@dataclass
class transakcija:
    id : int = field(default=0)  # Za vsako polje povemo tip in privzeto vrednost
    racun : int = field(default=0)
    cas: datetime=field(default=datetime.now()) 
    znesek: float=field(default=0)
    opis: str=field(default="")


@dataclass_json
@dataclass
class oseba:
    emso : str = field(default="")  # Za vsako polje povemo tip in privzeto vrednost
    ime : str = field(default="")
    priimek : str = field(default="")
    rojstvo: str = field(default="") 
    ulica : str = field(default="")
    posta : int = field(default=0)

@dataclass_json
@dataclass
class racun:    
    stevilka : int = field(default=0)
    lastnik : int = field(default=0)
    