#!/usr/bin/python3
from xml.dom import minidom
import os

def processaHighlighting(language):
    print('Inicio el tractament del contingut del Highlighting')
    lists = language.getElementsByTagName('list')
    processaLists(lists)
    print('Finalitzo el tractament del contingut del Highlighting')
    
def processaLists(lists):
    print("El número de llistes és de {}".format(len(lists)))
    for llista in lists:
        if llista.hasAttribute('name'):
            nom = llista.getAttribute('name')
            if nom=='prep':
                nom = 'picBoundaryPatterns'
            if nom=='builtinfuncs':
                nom = 'm4Patterns'
            if nom=='keywords':
                nom = 'picPatterns'
            if nom=='specialvars':
                nom = 'cmPatterns'
            print("Comença la llista {}".format(nom))
        else:
            raise Exception("XML mal format: Manca un atribut al tag 'list'")
        items = llista.getElementsByTagName('item')
        processaItems(items,nom)
        print("Finalitza la llista\n")
        
def processaItems(items,nom):
    print("El número d'ítems d'aquesta llista és de {}".format(len(items)))
    with open('syntax.dat','a') as f:
        f.write("        {tipus} = [".format(tipus=nom))
        N = 0
        for item in items:
            cmd = item.firstChild.data.lstrip().rstrip()
            f.write('"\\\\b{}",'.format(cmd))
            N = N+1
            if N==6:
                f.write("\n        ")
                N=0
        f.write("]\n\n")        

if os.path.exists('syntax.dat'):
    os.remove('syntax.dat')
mydoc = minidom.parse('m4cm.xml')
processaHighlighting(mydoc)

