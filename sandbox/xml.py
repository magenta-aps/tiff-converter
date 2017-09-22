from lxml import etree

SIARDDK_NAMESPACE = "http://www.sa.dk/xmlns/diark/1.0"
SIARDDK = '{%s}' % SIARDDK_NAMESPACE

NSMAP = {'siard': SIARDDK_NAMESPACE}

docIndex = etree.Element(SIARDDK + "docIndex", nsmap=NSMAP)

print(etree.tostring(docIndex, pretty_print=True))

