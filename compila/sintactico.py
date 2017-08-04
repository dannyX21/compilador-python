from lexico import Lexico
from simbolo import Simbolo

class Sintactico():
    def __init__(self, lexico):
        self.lexico = lexico
        self.complex_actual = self.lexico.siguiente_componente_lexico()
        self.errors = 0
        #print(self.complex_actual)

    def siguiente_componente_lexico(self):
        self.complex_actual = self.lexico.siguiente_componente_lexico()

    def compara(self,token_esperado):
        if self.complex_actual and token_esperado == self.complex_actual.Token:
            self.siguiente_componente_lexico()
            return True
        elif token_esperado <= 255:
            self.register_error(chr(token_esperado))
        else:
            self.register_error(token_esperado)
        return False

    def PROGRAMA(self):
        if self.DEFINIR_VARIABLES():
            if self.DEFINIR_FUNCIONES():
                if self.PRINCIPAL():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def DEFINIR_VARIABLES(self):
        self.VARIABLES()
        return True

    def VARIABLES(self):
        if self.VARIABLE():
            if self.VARIABLES_PRIMA():
                return True
            else:
                return False
        else:
            return False

    def VARIABLES_PRIMA(self):
        if self.VARIABLE():
            if self.VARIABLES_PRIMA():
                return True
            else:
                return False
        else:
            return True

    def VARIABLE(self):
        if self.TIPO():
            if self.IDENTIFICADORES():
                self.compara(val_ascii(';'))
                return True
            else:
                return False
        else:
            return False

    def TIPO(self):
        actual = self.get_token_actual()
        if actual == valor_token('int') or actual == valor_token('float') or actual == valor_token('bool') or actual == valor_token('char') or actual == valor_token('string') or actual == valor_token('void'):
            self.compara(actual)
            return True
        else:
            return False

    def IDENTIFICADORES(self):
        if self.IDENTIFICADOR():
            if self.IDENTIFICADORES_PRIMA():
                return True
            else:
                return False
        else:
            return False

    def IDENTIFICADORES_PRIMA(self):
        actual = self.get_token_actual()
        if actual == val_ascii(','):
            self.compara(actual)
            if self.IDENTIFICADOR():
                if self.IDENTIFICADORES_PRIMA():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def IDENTIFICADOR(self):
        actual = self.get_token_actual()
        if actual == valor_token('id'):
            self.compara(actual)
            if self.ES_ARREGLO():
                return True
            else:
                return False
        else:
            return False

    def ES_ARREGLO(self):
        actual = self.get_token_actual()
        if actual == val_ascii('['):
            self.compara(actual)
            self.compara(valor_token('num'))
            self.compara(val_ascii(']'))
            return True
        else:
            return True

    def DEFINIR_FUNCIONES(self):
        self.FUNCIONES()
        return True

    def FUNCIONES(self):
        if self.FUNCION():
            if self.FUNCIONES_PRIMA():
                return True
            else:
                return False
        else:
            return False

    def FUNCIONES_PRIMA(self):
        if self.FUNCION():
            if self.FUNCIONES_PRIMA():
                return True
            else:
                return False
        else:
            return True

    def FUNCION(self):
        actual = self.get_token_actual()
        if actual == valor_token('function'):
            self.compara(actual)
            if self.TIPO():
                self.compara(valor_token('id'))
                self.compara(val_ascii('('))
                if self.PARAMETROS_FORMALES():
                    self.compara(val_ascii(')'))
                    if self.DEFINIR_VARIABLES():
                        if self.CUERPO_FUNCION():
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def PARAMETROS_FORMALES(self):
        self.PARAMETROS()
        return True

    def PARAMETROS(self):
        if self.PARAMETRO():
            if self. PARAMETROS_PRIMA():
                return True
            else:
                return False
        else:
            return False

    def PARAMETROS_PRIMA(self):
        actual = self.get_token_actual()
        if actual == val_ascii(','):
            self.compara(actual)
            if self.PARAMETRO():
                if self.PARAMETROS_PRIMA():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def PARAMETRO(self):
        if self.TIPO():
            self.compara(valor_token('id'))
            return True
        else:
            return False

    def CUERPO_FUNCION(self):
        if self.BLOQUE():
            return True
        else:
            return False

    def BLOQUE(self):
        actual = self.get_token_actual()
        if actual == val_ascii('{'):
            self.compara(actual)
            if self.ORDENES():
                self.compara(val_ascii('}'))
                return True
            else:
                return False
        else:
            return False

    def ORDENES(self):
        if self.ORDEN():
            if self.ORDENES_PRIMA():
                return True
            else:
                return False
        else:
            return False

    def ORDENES_PRIMA(self):
        if self.ORDEN():
            if self.ORDENES_PRIMA():
                return True
            else:
                return False
        else:
            return True

    def ORDEN(self):
        if self.ASIGNACION() or self.DECISION() or self.ITERACION() or self.ENTRADA_SALIDA() or self.BLOQUE() or self.RETORNO():
            return True
        else:
            return False

    def ASIGNACION(self):
        if self.DESTINO():
            self.compara(valor_token('igu'))
            if self.FUENTE():
                self.compara(val_ascii(';'))
                return True
            else:
                return False
        else:
            return False

    def FUENTE(self):
        if self.EXPRESION():
            return True
        else:
            self.register_error('EXPRESION')
            return False

    def DECISION(self):
        actual = self.get_token_actual()
        if actual == valor_token('if'):
            self.compara(actual)
            self.compara(val_ascii('('))
            if self.EXPRESION():
                self.compara(val_ascii(')'))
                self.compara(valor_token('then'))
                if self.ORDEN():
                    if self.TIENE_ELSE():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                self.register_error('EXPRESION')
                return False
        else:
            return False

    def TIENE_ELSE(self):
        actual = self.get_token_actual()
        if actual == valor_token('else'):
            self.compara(actual)
            if self.ORDEN():
                return True
            else:
                return False
        else:
            return True

    def ITERACION(self):
        actual = self.get_token_actual()
        if actual == valor_token('for'):
            self.compara(actual)
            self.compara(valor_token('id'))
            self.compara(valor_token('igu'))
            self.compara(valor_token('num'))
            self.compara(valor_token('to'))
            self.compara(valor_token('num'))
            if self.ORDEN():
                return True
            else:
                return False
        elif actual == valor_token('while'):
            self.compara(actual)
            self.compara(val_ascii('('))
            if self.EXPRESION_LOGICA():
                self.compara(val_ascii(')'))
                self.compara(valor_token('do'))
                if self.ORDEN():
                    return True
                else:
                    return False
            else:
                return False
        elif actual == valor_token('do'):
            self.compara(actual)
            if self.ORDEN():
                self.compara(valor_token('while'))
                self.compara(val_ascii('('))
                if self.EXPRESION_LOGICA():
                    self.compara(val_ascii(')'))
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def ENTRADA_SALIDA(self):
        actual = self.get_token_actual()
        if actual == valor_token('read'):
            self.compara(actual)
            self.compara(val_ascii('('))
            if self.DESTINO():
                self.compara(val_ascii(')'))
                self.compara(val_ascii(';'))
                return True
            else:
                return False
        elif actual == valor_token('write'):
            self.compara(actual)
            self.compara(val_ascii('('))
            if self.EXPRESION():
                self.compara(val_ascii(')'))
                self.compara(val_ascii(';'))
                return True
            else:
                self.register_error('EXPRESION')
                return False
        else:
            return False

    def RETORNO(self):
        actual = self.get_token_actual()
        if actual == valor_token('return'):
            self.compara(actual)
            if self.EXPRESION():
                self.compara(val_ascii(';'))
                return True
            else:
                self.register_error('EXPRESION')
                return False
        else:
            return False

    def PRINCIPAL(self):
        actual = self.get_token_actual()
        if actual == valor_token('main'):
            self.compara(actual)
            self.compara(val_ascii('('))
            if self.PARAMETROS_FORMALES():
                self.compara(val_ascii(')'))
                if self.BLOQUE():
                    return True
                else:
                    return False
            else:
                return False
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
        if actual == valor_token('num') or actual == valor_token('numf') or actual == valor_token('const_string') or actual == valor_token('const_char') or actual == valor_token('true') or actual == valor_token('false'):
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
                self.register_error('EXPRESION')
                return False
        else:
            return True

    def get_token_actual(self):
        if self.complex_actual:
            return self.complex_actual.Token
        else:
            return None

    def register_error(self,item):
        self.errors += 1
        if type(item) == str:
            print("Ln: {}, se esperaba un(a): '{}'".format(self.lexico.Num_linea(),item))
        elif type(item) == int:
            print("Ln: {}, se esperaba token# {}".format(self.lexico.Num_linea(),item))


def valor_token(lexema):
    token = Simbolo.TOKENS.get(lexema.upper())
    if token:
        return token
    else:
        return None

def val_ascii(caracter):
    return ord(caracter)
