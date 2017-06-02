from lexico import Lexico
from sintactico import Sintactico
from simbolo import Simbolo

source = 'code.txt'
f = open(source,'r')
codigo_fuente = f.read()
print("Codigo fuente: {}".format(codigo_fuente))

lex = Lexico(codigo_fuente)
sin = Sintactico(lex)
print(sin.EXPRESION())

##while True:
##    s = lex.siguiente_componente_lexico()
##    print(s)
##    if not s:
##        break
