username = ''
password = ''
username_expedicion = ''
password_expedicion = ''
vat = '' #VAT company
franchise = '' # Franchise code
seurid = '' #Description ID Seur
ci = '' #Customer Code Seur
ccc = '' #Account Code Seur

context = {}
context['printer'] = 'ZEBRA'
context['printer_model'] = 'LP2844-Z'
context['ecb_code'] = '2C'

from seur.picking import *
from seur.utils import services
from base64 import decodestring

print "Seur services"
services = services()
print services

with API(username, password, vat, franchise, seurid, ci, ccc, context) as seur_api:
    print "Test connection"
    print seur_api.test_connection()

with Picking(username, password, vat, franchise, seurid, ci, ccc, context) as picking_api:
    print "Send a new shipment - Label ECB"

    data = {}
    data['servicio'] = '1'
    data['product'] = '2'
    data['total_bultos'] = 1
    #~ data['total_kilos'] = 
    data['observaciones'] = 'Testing Seur API - Create shipments'
    data['referencia_expedicion'] = 'S/OUT/0001'
    data['ref_bulto'] = 'S/OUT/0001'
    #~ data['clave_portes'] = '' # Add F to invoice
    #~ data['clave_reembolso'] = '' # Add F to invoice
    #~ data['valor_reembolso'] = ''
    data['cliente_nombre'] = 'Zikzakmedia SL'
    data['cliente_direccion'] = 'Docror Fleming, 28. Baixos'
    #~ data['cliente_tipovia'] = 'CL'
    #~ data['cliente_tnumvia'] = 'N'
    #~ data['cliente_numvia'] = '93'
    #~ data['cliente_escalera'] = 'A'
    #~ data['cliente_piso'] = '3'
    #~ data['cliente_puerta'] = '2'
    data['cliente_poblacion'] = 'Vilafranca del Penedes' # Important city exist in Seur. Get Seur values from zip method
    data['cliente_cpostal'] = '08720'
    data['cliente_pais'] = 'ES'
    data['cliente_email'] = 'zikzak@zikzakmedia.com'
    data['cliente_telefono'] = '938902108'
    data['cliente_atencion'] = 'Raimon Esteve'

    reference, label, error = picking_api.create(data)

    if error:
        print error

    print reference

    with open("/tmp/seur-label.txt","wb") as f:
        f.write(label)
    print "Generated label in /tmp/seur-label.txt"

context['pdf'] = True
with Picking(username, password, vat, franchise, seurid, ci, ccc, context) as picking_api:
    print "Send a new shipment - Label PDF"
    reference, label, error = picking_api.create(data)

    if error:
        print error

    print reference
    with open("/tmp/seur-label.pdf","wb") as f:
        f.write(decodestring(label))
    print "Generated PDF label in /tmp/seur-label.pdf"

with Picking(username_expedicion, password_expedicion, vat, franchise, seurid, ci, ccc, context) as picking_api:
    print "Get info picking"
    data = {}

    data['expedicion'] = 'S'
    data['reference'] = reference
    data['service'] = '0'
    data['public'] = 'N'

    info = picking_api.info(data)
    print info

with Picking(username_expedicion, password_expedicion, vat, franchise, seurid, ci, ccc, context) as picking_api:

    print "Get list picking"
    data = {}

    data['expedicion'] = 'S'
    data['public'] = 'N'

    info = picking_api.list(data)
    print info

context['pdf'] = True
with Picking(username, password, vat, franchise, seurid, ci, ccc, context) as picking_api:
    print "Get Label PDF"

    data = {}
    data['servicio'] = '1'
    data['product'] = '2'
    data['total_bultos'] = 2
    #~ data['total_kilos'] = 
    data['observaciones'] = 'Testing Seur API - Get Label'
    data['referencia_expedicion'] = 'S/OUT/0001'
    data['ref_bulto'] = 'S/OUT/0001'
    #~ data['clave_portes'] = '' # Add F to invoice
    #~ data['clave_reembolso'] = '' # Add F to invoice
    #~ data['valor_reembolso'] = ''
    data['cliente_nombre'] = 'Zikzakmedia SL'
    data['cliente_direccion'] = 'Sant Jaume, 9. Baixos 2'
    #~ data['cliente_tipovia'] = 'CL'
    #~ data['cliente_tnumvia'] = 'N'
    #~ data['cliente_numvia'] = '93'
    #~ data['cliente_escalera'] = 'A'
    #~ data['cliente_piso'] = '3'
    #~ data['cliente_puerta'] = '2'
    data['cliente_poblacion'] = 'Vilafranca del Penedes' # Important city exist in Seur. Get Seur values from zip method
    data['cliente_cpostal'] = '08720'
    data['cliente_pais'] = 'ES'
    data['cliente_email'] = 'zikzak@zikzakmedia.com'
    data['cliente_telefono'] = '938902108'
    data['cliente_atencion'] = 'Raimon Esteve'
    label = picking_api.label(data)

    with open("/tmp/seur-label.pdf","wb") as f:
        f.write(decodestring(label))
    print "Generated PDF label in /tmp/seur-label.pdf"

with Picking(username, password, vat, franchise, seurid, ci, ccc, context) as picking_api:
    print "Get Manifiesto"

    data = {}
    manifiesto = picking_api.manifiesto(data)

    with open("/tmp/seur-manifiesto.pdf","wb") as f:
        f.write(decodestring(manifiesto))
    print "Generated PDF label in /tmp/seur-manifiesto.pdf"

with Picking(username, password, vat, franchise, seurid, ci, ccc, context) as picking_api:
    print "Get values from Seur about city or zip"

    city = 'Granollers'
    print picking_api.city(city)

    zip = '08720'
    print picking_api.zip(zip)
