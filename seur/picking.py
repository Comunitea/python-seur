#This file is part of seur. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from seur.api import API

from xml.dom.minidom import parseString
import os
import genshi
import genshi.template

loader = genshi.template.TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'template'),
    auto_reload=True)


class Picking(API):
    """
    Picking API
    """
    __slots__ = ()

    def create(self, data):
        """
        Create a picking using the given data

        :param data: Dictionary of values
        :return: reference (str), label (pdf), error (str)
        """
        reference = None
        label = None
        error = None

        tmpl = loader.load('picking_send.xml')

        vals = {
            'username': self.username,
            'password': self.password,
            'vat': self.vat,
            'in5': self.in5,
            'in7': self.in7,
            'ci': self.ci,
            'ccc': self.ccc,
            'servicio': data.get('servicio', '1'),
            'product': data.get('product', '2'),
            'total_bultos': data.get('total_bultos', '1'),
            'total_kilos': data.get('total_kilos', '0.1'),
            'observaciones': data.get('observaciones', ''),
            'referencia_expedicion': data.get('referencia_expedicion', ''),
            'ref_bulto': data.get('ref_bulto', ''),
            'clave_portes': data.get('clave_portes', 'F'),
            'clave_reembolso': data.get('clave_reembolso', 'F'),
            'valor_reembolso': data.get('valor_reembolso', '1'),
            'cliente_nombre': data.get('cliente_nombre', ''),
            'cliente_direccion': data.get('cliente_direccion', ''),
            'cliente_tipovia': data.get('cliente_tipovia', 'CL'),
            'cliente_tnumvia': data.get('cliente_tnumvia', 'N'),
            'cliente_numvia': data.get('cliente_numvia', '.'),
            'cliente_escalera': data.get('cliente_escalera', '.'),
            'cliente_piso': data.get('cliente_piso', '.'),
            'cliente_puerta': data.get('cliente_puerta', ''),
            'cliente_poblacion': data.get('cliente_poblacion', ''),
            'cliente_cpostal': data.get('cliente_cpostal', ''),
            'cliente_pais': data.get('cliente_pais', ''),
            'cliente_telefono': data.get('cliente_telefono', ''),
            'cliente_atencion': data.get('cliente_atencion', ''),
            }

        url = 'http://cit.seur.com/CIT-war/services/ImprimirECBWebService'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        dom = parseString(result)

        #Get message error from XML
        mensaje = dom.getElementsByTagName('mensaje')
        if mensaje:
            if mensaje[0].firstChild.data == 'ERROR':
                error = 'Seur return an error when send shipment %s' % vals.get('ref_bulto')
                return reference, label, error

        #Get reference from XML
        ecb = dom.getElementsByTagName('ECB')
        if ecb:
            reference = ecb[0].childNodes[0].firstChild.data

        #Get PDF file from XML
        pdf = dom.getElementsByTagName('PDF')
        if pdf:
            label = pdf[0].firstChild.data

        return reference, label, error

    def info(self, data):
        """
        Picking info using the given data

        :param data: Dictionary of values
        :return: info dict
        """
        tmpl = loader.load('picking_info.xml')

        vals = {
            'username': self.username,
            'password': self.password,
            'expedicion': data.get('expedicion', 'S'),
            'reference': data.get('reference'),
            'service': data.get('service', '0'),
            'public': data.get('public', 'N'),
            }

        url = 'https://ws.seur.com/webseur/services/WSConsultaExpediciones'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        dom = parseString(result)

        #Get info
        info = dom.getElementsByTagName('out')
        return info[0].firstChild.data
