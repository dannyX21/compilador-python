from lexico import Lexico
from simbolo import Simbolo

class Sintactico():
    def __init__(self, lexico):
        self.lexico = lexico
        self.complex_actual = self.lexico.siguiente_componente_lexico()
        #print(self.complex_actual)

    def siguiente_componente_lexico(self):
        self.complex_actual = self.lexico.siguiente_componente_lexico()

    def compara(self,token_esperado):
        if self.complex_actual and token_esperado == self.complex_actual.Token:
            self.siguiente_componente_lexico()
            return True
        elif token_esperado <= 255:
            print("Ln: {}, se esperaba un: '{}'".format(self.lexico.Num_linea(),chr(token_esperado)))
        else:
            print("Ln: {}, se esperaba token# '{}'".format(self.lexico.Num_linea(),token_esperado))
            return False

    def TIPO(self):
        actual = self.get_token_actual()
        if actual == valor_token('int') or actual == valor_token('float') or actual == valor_token('bool') or actual == valor_token('char') or actual == valor_token('string') or actual == valor_token('void'):
            self.compara(actual)
            return True
        else:
            return False

    def EXPRESION(self):
        actual = self.get_token_actual()
        if actual == val_ascii('('):
            self.compara(actual)
            if self.EXPRESION():
                self.compara(val_ascii(')'))
                return True
            else:
                return False
        elif self.EXPRESION_LOGICA():
            return True
        else:
            return False

    def EXPRESION_LOGICA(self):
        if self.TERMINO_LOGICO():
            if self.EXPRESION_LOGICA_aux():
                return True
            else:
                return False
        else:
            return False

    def EXPRESION_LOGICA_aux(self):
        actual = self.get_token_actual()
        if actual == val_ascii('&') or actual == val_ascii('|'):
            self.compara(actual)
            if self.TERMINO_LOGICO():
                if self.EXPRESION_LOGICA_aux():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True #######Check

    def TERMINO_LOGICO(self):
        actual = self.get_token_actual()
        if actual == val_ascii('!'):
            self.compara(actual)
            actual = self.get_token_actual()
            if actual == val_ascii('('):
                self.compara(actual)
                if self.EXPRESION_LOGICA():
                    self.compara(val_ascii(')'))
                    return True
                elif self.EXPRESION_RELACIONAL():
                    self.compara(val_ascii(')'))
                    return True
                else:
                    return False
            else:
                return False
        elif self.EXPRESION_RELACIONAL():
            return True
        else:
            return False


##    def TERMINO_LOGICO(self):
##        actual = self.get_token_actual()
##        if actual == val_ascii('!'):
##            self.compara(actual)
##            self.compara(val_ascii('('))
##            if self.EXPRESION_LOGICA() or self.EXPRESION_RELACIONAL():
##                self.compara(val_ascii(')'))
##                return True
##            else:
##                return False
##        elif self.EXPRESION_RELACIONAL():
##            return True
##        else:
##            return False

    def EXPRESION_RELACIONAL(self):
        if self.EXPRESION_ARITMETICA():
            if self.EXPRESION_RELACIONAL_aux():
                return True
            else:
                return False
        else:
            return False

    def EXPRESION_RELACIONAL_aux(self):
        actual = self.get_token_actual()
        if actual == valor_token('MAY') or actual == valor_token('MAI') or actual == valor_token('IGU') or actual == valor_token('DIF') or actual == valor_token('MEN') or actual == valor_token('MEI'):
            self.compara(actual)
            if self.EXPRESION_ARITMETICA():
                if self.EXPRESION_RELACIONAL_aux():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def EXPRESION_ARITMETICA(self):
        if self.TERMINO_ARITMETICO():
            if self.EXPRESION_ARITMETICA_aux():
                return True
            else:
                return False
        else:
            return False

    def EXPRESION_ARITMETICA_aux(self):
        actual = self.get_token_actual()
        if actual == val_ascii('+') or actual == val_ascii('-'):
            self.compara(actual)
            if self.TERMINO_ARITMETICO():
                if self.EXPRESION_ARITMETICA_aux():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def TERMINO_ARITMETICO(self):
        if self.FACTOR_ARITMETICO():
            if self.TERMINO_ARITMETICO_aux():
                return True
            else:
                return False
        else:
            return False

    def TERMINO_ARITMETICO_aux(self):
        actual = self.get_token_actual()
        if actual == val_ascii('*') or actual == val_ascii('/') or actual == val_ascii('%') or actual == val_ascii('\\'):
            self.compara(actual)
            if self.FACTOR_ARITMETICO():
                if self.TERMINO_ARITMETICO_aux():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def FACTOR_ARITMETICO(self):
        actual = self.get_token_actual()
        if actual == val_ascii('('):
            self.compara(actual)
            if self.EXPRESION_ARITMETICA():
                self.compara(val_ascii(')'))
                return True
            else:
                return False
        elif self.OPERANDO():
            return True
        else:
            return False

    def OPERANDO(self):
        actual = self.get_token_actual()
        if actual == valor_token('num') or valor_token('numf') or valor_token('const_string') or valor_token('const_char') or valor_token('true') or valor_token('false'):
            self.compara(actual)
            return True
        elif actual == val_ascii('('):
            self.compara(actual)
            if self.EXPRESION_ARITMETICA():
                self.compara(val_ascii(')'))
                return True
            else:
                return False
        elif self.DESTINO():
            return True
        elif self.INVOCAR_FUNCION():
            return True
        else:
            return False

    def INVOCAR_FUNCION(self):
        actual = self.get_token_actual()
        if actual == valor_token('call'):
            self.compara(actual)
            self.compara(valor_token('id'))
            self.compara(valor_token('('))
            if self.ACTUALES():
                self.compara(val_ascii(')'))
                return True
            else:
                return False
        else:
            return False

    def ACTUALES (self):
        if self.ACTUAL():
            if self.ACTUALES_aux():
                return True
            else:
                return False
        else:
            return False

    def ACTUALES_aux(self):
        actual = self.get_token_actual()
        if actual == val_ascii(','):
            self.compara(actual)
            if self.ACTUAL():
                if self.ACTUALES_aux():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def ACTUAL(self):
        if self.EXPRESION():
            return True
        else:
            return False


    def DESTINO(self):
        actual = self.get_token_actual()
        if actual == valor_token('id'):
            self.compara(actual)
            if self.ELEMENTO_ARREGLO():
                return True
            else:
                return False
        else:
            return False

    def ELEMENTO_ARREGLO(self):
        actual = self.get_token_actual()
        if actual == val_ascii('['):
            self.compara(actual)
            if self.EXPRESION():
                self.compara(val_ascii(']'))
                return True
            else:
                return False
        else:
            return True

    def get_token_actual(self):
        if self.complex_actual:
            return self.complex_actual.Token
        else:
            return None

def valor_token(lexema):
    token = Simbolo.TOKENS.get(lexema.upper())
    if token:
        return token
    else:
        return None

def val_ascii(caracter):
    return ord(caracter)
