from lexico import Lexico
class Sintactico():
    def __init__(self, lexico):
        self.lexico = lexico
        self.token_actual = self.lexico.siguiente_componente_lexico()

    def compara(token_esperado):
        if token_esperado == token_actual.token:
            self.token_actual = self.lexico.siguiente_componente_lexico()
        else:
            print("Ln: {}. Se esperaba: {}".format(self.lexico.Num_linea, token_esperado))

    def TIPO(self):
        if self.token_actual.token == valor_token('int') or
        self.token_actual.token == valor_token('float') or
        self.token_actual.token == valor_token('bool') or
        self.token_actual.token == valor_token('char') or
        self.token_actual.token == valor_token('string'):
            self.compara(self.token_actual)
            return True
        else:
            return false

    def valor_token(self, lexema):
        return Simbolo.TOKENS.get(lexema)
