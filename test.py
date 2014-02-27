username = ''
password = ''
vat = '' #VAT company
in5 = '' # Franchise code
in7 = '' #Description ID Seur
ci = '' #Customer Code Seur
ccc = '' #Account Code Seur
debug = True

from seur.picking import *
from seur.utils import services
from base64 import decodestring

print "Seur services"
services = services()
print services

with API(username, password, vat, in5, in7, ci, ccc, debug) as seur_api:
    print "Test connection"
    print seur_api.test_connection()

with Picking(username, password, vat, in5, in7, ci, ccc, debug) as picking_api:
    print "Send a new shipment"
    data = {}

    data['servicio'] = '1'
    data['product'] = '2'
    data['total_bultos'] = '1'
    #~ data['total_kilos'] = 
    data['observaciones'] = 'Testing Seur API - Create shipments'
    data['referencia_expedicion'] = 'S/OUT/0001'
    data['ref_bulto'] = 'S/OUT/0001'
    #~ data['clave_portes'] = 
    #~ data['clave_reembolso'] = 
    #~ data['valor_reembolso'] = 
    data['cliente_nombre'] = 'Zikzakmedia SL'
    data['cliente_direccion'] = 'Docror Fleming, 28. Baixos'
    #~ data['cliente_tipovia'] = 'CL'
    #~ data['cliente_tnumvia'] = 'N'
    #~ data['cliente_numvia'] = '93'
    #~ data['cliente_escalera'] = 'A'
    #~ data['cliente_piso'] = '3'
    #~ data['cliente_puerta'] = '2'
    data['cliente_poblacion'] = 'Vilafranca del Penedes'
    data['cliente_cpostal'] = '08720'
    data['cliente_pais'] = 'ES'
    data['cliente_telefono'] = '938902108'
    data['cliente_atencion'] = 'Raimon Esteve'

    reference, label, error = picking_api.create(data)
    if error:
        print error

    print reference

    with open("/tmp/seur-label.pdf","wb") as f:
        f.write(decodestring(label))
    print "Generated PDF label in /tmp/"
