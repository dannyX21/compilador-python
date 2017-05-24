from lexico import Lexico
from simbolo import Simbolo

class Sintactico():
    def __init__(self, lexico):
        self.lexico = lexico
        self.token_actual = self.lexico.siguiente_componente_lexico()
        #print(self.token_actual)
        
    def siguiente_componente_lexico(self):
        self.token_actual = self.lexico.siguiente_componente_lexico()

    def compara(self,token_esperado):
        if token_esperado == self.token_actual.Token:
            self.siguiente_componente_lexico()
            return True
        else:
            print("Ln: {}, se esperaba: {}".format(self.lexico.Num_linea, token_esperado))
            return False

    def TIPO(self):
        actual = self.token_actual.Token
        if actual == valor_token('int') or actual == valor_token('float') or actual == valor_token('bool') or actual == valor_token('char') or actual == valor_token('string'):
            self.compara(self.token_actual.Token)
            return True
        else:
            return False

def valor_token(lexema):
    token = Simbolo.TOKENS.get(lexema.upper())
    if token:
        return token
    else:
        return None
