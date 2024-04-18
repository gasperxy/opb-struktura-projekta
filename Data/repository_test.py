from repository import Repo
from models import *


repo = Repo()

# Dobimo vse osebe

osebe = repo.dobi_osebe()


# Jih izpišemo
for o in osebe:
    print(o)

# Izberemo si recimo neko osebo
o = osebe[0]

# Za to osebo želimo pridobiti vse transakcije

transakcije = repo.dobi_transakcije_oseba(o.emso)

for t in transakcije:
    print(t)


