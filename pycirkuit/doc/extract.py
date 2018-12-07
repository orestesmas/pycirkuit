#!/usr/bin/python3
from xml.dom import minidom
mydoc = minidom.parse('m4cm.xml')
items = mydoc.getElementsByTagName('item')
len(items)
f = open('fitxer.dat','w')
f.write("[\n")
for i in items:
    cmd = i.firstChild.data.lstrip().rstrip()
    f.write('"\\\\b{}",'.format(cmd))
f.write("]\n")
f.close()

