from lxml import etree

NAMESPACE = "http://www.sa.dk/xmlns/diark/1.0"
NAMESPACE2 = "http://www.w3.org/1999/xhtml"
# SIARDDK = '{%s}' % SIARDDK_NAMESPACE

NSMAP = {None: NAMESPACE, 'w3c': NAMESPACE2}

tag = etree.QName(NAMESPACE, 'docIndex')
docIndex = etree.Element(tag, nsmap=NSMAP)
schemaLocation = etree.QName(NAMESPACE2, 'schemaLocation')
docIndex.set(schemaLocation, 'jhjhj')

tag_hurra = etree.QName(NAMESPACE, 'hurra')
hurra = etree.SubElement(docIndex, tag_hurra)
print(etree.QName(hurra).namespace)

print(str(etree.tostring(docIndex, pretty_print=True)))

