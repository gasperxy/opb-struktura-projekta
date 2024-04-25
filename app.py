from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.transakcije_service import TransakcijeService
import os
service = TransakcijeService()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')


@get('/')
def index():
    """
    Domača stran z transakcijami.
    """   
  
    transakcije = service.dobi_transakcije()  
        
    return template('transakcije.html', transakcije = transakcije)

@get('/transakcije_dto')
def transakcije_dto():
    """
    Stran z dto transakcijami.
    """   
  
    transakcije_dto = service.dobi_transakcije_dto()  
        
    return template('transakcije_dto.html', transakcije = transakcije_dto)

@get('/dodaj_transakcijo')
def dodaj_transakcijo():
    """
    Stran za dodajanje transakcije.  """   
    return template('dodaj_transakcijo.html')

@post('/dodaj_transakcijo')
def dodaj_transakcijo_post():
    # Preberemo podatke iz forme. Lahko bi uporabili kakšno dodatno metodo iz service objekta

    racun = int(request.forms.get('racun'))
    znesek = float(request.forms.get('znesek'))
    opis = request.forms.get('opis')   

    service.naredi_transakcijo(racun, znesek, opis)
    
    
    redirect(url('/'))

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)