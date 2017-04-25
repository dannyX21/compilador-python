from lexico import Lexico
from simbolo import Simbolo

codigo_fuente="int main a x while for<=>=<>=><>>= if a > b then"

print("Codigo fuente: {}".format(codigo_fuente))

lex = Lexico(codigo_fuente)

while True:
    s = lex.siguiente_componente_lexico()
    print(s)
    if not s:
        break
