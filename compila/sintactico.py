from lexico import Lexico
from simbolo import Simbolo, tipoDato, tipoDatoText
from semantico import Semantico
from pila import Pila


class Sintactico():
    def __init__(self, lexico):
        self.lexico = lexico
        self.complex_actual = self.lexico.siguiente_componente_lexico()
        self.errors = 0
        self.sem = Semantico()
        self.pila = Pila()
#       print(self.complex_actual)

    def siguiente_componente_lexico(self):
        self.complex_actual = self.lexico.siguiente_componente_lexico()

    def compara(self, token_esperado):
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
            tipos = list(tipoDato.keys())
            for t in tipos:
                if actual == valor_token(t):
                    self.lexico.TIPODATO = tipoDato[t]
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
            if self.lexico.FIN_GLOBALES == -1:
                self.lexico.FIN_GLOBALES = len(self.lexico.tabla_simbolos)
            self.compara(actual)
            if self.TIPO():
                self.lexico.SECCION = 1 #definicion de variables locales.
                self.lexico.INICIO_LOCALES = len(self.lexico.tabla_simbolos)
                self.compara(valor_token('id'))
                self.compara(val_ascii('('))
                if self.PARAMETROS_FORMALES():
                    self.compara(val_ascii(')'))
                    if self.DEFINIR_VARIABLES():
                        self.lexico.SECCION = 2 #cuerpo de funcion local
                        if self.CUERPO_FUNCION():
                            self.lexico.SECCION = 0
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
        tac = ""
        if self.DESTINO():
            tac = self.pila.pop().Lexema + " := "
            self.compara(valor_token('igu'))
            if self.FUENTE():
                tac += self.pila.pop().Lexema
                self.sem.genTAC(tac)
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
                self.sem.genTAC("CMP " + self.pila.pop())
                label_else = self.sem.genLabel()
                self.sem.genTAC("JNZ " + label_else)
                if self.ORDEN():
                    label_end = self.sem.genLabel()
                    self.sem.genTAC("JMP " + label_end)
                    self.sem.genTAC(label_else + ":")
                    if self.TIENE_ELSE():
                        self.sem.genTAC(label_end + ":")
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
            tac = ""
            label_inicio = self.sem.genLabel()
            label_fin = self.sem.genLabel()
            variable = self.complex_actual
            self.compara(valor_token('id'))
            self.compara(valor_token('igu'))
            num_inicio = self.complex_actual
            self.compara(valor_token('num'))
            self.compara(valor_token('to'))
            num_final = self.complex_actual
            self.compara(valor_token('num'))
            tac = variable.Lexema + " := " + num_inicio.Lexema
            self.sem.genTAC(tac)
            self.sem.genTAC(label_inicio + ": ")
            tmp = Simbolo(self.sem.genTemp(),Simbolo.TOKENS['ID'])
            self.sem.genTAC(tmp.Lexema + " := " + variable.Lexema + " < " + num_final.Lexema)
            self.sem.genTAC("CMP " + tmp.Lexema)
            self.sem.genTAC("JNZ " + label_fin)

            if self.ORDEN():
                self.sem.genTAC(variable.Lexema + " := " + variable.Lexema + " + 1")
                self.sem.genTAC("JMP " + label_inicio)
                self.sem.genTAC(label_fin + ":")
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
            if self.lexico.FIN_GLOBALES == -1:
                self.lexico.FIN_GLOBALES = len(self.lexico.tabla_simbolos)
            self.lexico.SECCION = 3 #Cuerpo principal
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
        tmp = ""
        tac = ""
        actual = self.get_token_actual()
        if actual == val_ascii('&') or actual == val_ascii('|'):
            operador = self.complex_actual.Lexema
            self.compara(actual)
            tmp = self.sem.genTemp()
            tac = tmp + " := " + self.pila.pop() + " " + operador + " "
            if self.TERMINO_LOGICO():
                tac += self.pila.pop()
                self.sem.genTAC(tac)
                self.pila.push(tmp)
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
        tmp = ""
        tac = ""
        actual = self.get_token_actual()
        if actual == valor_token('MAY') or actual == valor_token('MAI') or actual == valor_token('IGU') or actual == valor_token('DIF') or actual == valor_token('MEN') or actual == valor_token('MEI'):
            operador = self.complex_actual.Lexema
            self.compara(actual)
            tmp = Simbolo(self.sem.genTemp(), Simbolo.TOKENS['ID'])
            operando1 = self.pila.pop()
            tac = tmp.Lexema + " := " + operando1.Lexema + " " + operador + " "
            if self.EXPRESION_ARITMETICA():
                operando2 = self.pila.pop()
                tac += operando2.Lexema
                self.sem.genTAC(tac)
                self.pila.push(tmp)
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
        tmp = ""
        tac = ""
        actual = self.get_token_actual()
        if actual == val_ascii('+') or actual == val_ascii('-'):
            operador = self.complex_actual.Lexema
            self.compara(actual)
            tmp = Simbolo(self.sem.genTemp(), Simbolo.TOKENS['ID'])
            operando1 = self.pila.pop()
            tac = tmp.Lexema + " := " + operando1.Lexema + " " + operador + " "
            if self.TERMINO_ARITMETICO():
                operando2 = self.pila.pop()
                tac += operando2.Lexema
                tmp.TipoDato = self.sem.verificar(operador, operando1.TipoDato, operando2.TipoDato)
                if tmp.TipoDato == tipoDato["na"]:
                    self.register_error_tipo("No es posible aplicar el operador '{}' entre operandos de tipo '{}' y '{}'".format(operador, tipoDatoText[operando1.TipoDato], tipoDatoText[operando2.TipoDato]))
                self.sem.genTAC(tac)
                self.pila.push(tmp)
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
        tac = ""
        tmp = ""
        actual = self.get_token_actual()
        if actual == val_ascii('*') or actual == val_ascii('/') or actual == val_ascii('%') or actual == val_ascii('\\'):
            operador = self.complex_actual.Lexema
            self.compara(actual)
            tmp = self.sem.genTemp()
            tac = tmp + " := " + self.pila.pop() + " " + operador + " "
            if self.FACTOR_ARITMETICO():
                tac += self.pila.pop()
                self.sem.genTAC(tac)
                self.pila.push(tmp)
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
            self.pila.push(self.complex_actual)
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

    def ACTUALES(self):
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
            self.pila.push(self.complex_actual)
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

    def register_error(self, item):
        self.errors += 1
        if type(item) == str:
            print("Ln: {}, se esperaba un(a): '{}'".format(self.lexico.Num_linea(),item))
        elif type(item) == int:
            print("Ln: {}, se esperaba token# {}".format(self.lexico.Num_linea(),item))

    def register_error_tipo(self, msg):
        self.errors +=1
        print("Ln: {}, {}".format(self.lexico.Num_linea(), msg))

    def TAC(self):
        return self.sem.code


def valor_token(lexema):
    token = Simbolo.TOKENS.get(lexema.upper())
    if token:
        return token
    else:
        return None


def val_ascii(caracter):
    return ord(caracter)
