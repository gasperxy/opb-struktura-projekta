from transakcije_service import TransakcijeService
from Data.models import *


# V tej datoteki lahko testiramo funkcionalnost servisov,
# brez da zaganjamo celoten projekt.

service = TransakcijeService()


service.izplacaj_nagrado(10, "Nagrada 1")

tr = service.dobi_transakcije()

for t in tr:
    print(t)


