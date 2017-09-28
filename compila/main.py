#!/usr/bin/python3.5
from lexico import Lexico
from sintactico import Sintactico
from simbolo import Simbolo

source = 'code.txt'
f = open(source,'r')
codigo_fuente = f.read()
print("Codigo fuente: \n\n{}".format(codigo_fuente))

lex = Lexico(codigo_fuente)
sin = Sintactico(lex)
sin.PROGRAMA()
print()
if sin.errors > 0:
    print("Se encontraron: {} erorres".format(sin.errors))
else:
    print("Compilacion exitosa!")

for s in lex.tabla_simbolos:
    print(s)
    
##while True:
##    s = lex.siguiente_componente_lexico()
##    print(s)
##    if not s:
##        break
