from simbolo import Simbolo, tipoDato

class Lexico():
    def __init__(self, codigo_fuente=''):
        self.codigo_fuente = " " +codigo_fuente + " "         #Codigo fuente a compilar
        self.tabla_simbolos = []                    #Tabla de simbolos
        self.palabras_reservadas = ['bool','call','char','do','else','float','for','function','if','int','main','read','return','string','then','to','void','while','write','false','true']  #Lista de Palabras reservadas

        self.__caracter_actual = 0
        self.__indice = 0
        self.__inicio_lexema = 1
        self.__estado = 0
        self.__inicio = 0
        self.Lexema =""
        self.__num_linea = 1
        self.CARACTERES_VALIDOS = r"()[]{}+-*\/%|&!,;"
        self.TIPODATO = tipoDato["na"]
        self.SECCION = 0
        self.FIN_PALABRAS_RESERVADAS = -1
        self.FIN_GLOBALES = -1
        self.INICIO_LOCALES = -1

        self.__cargar_palabras_reservadas()
        #self.mostrar_tabla_simbolos()

    def inserta_simbolo(self, simbolo):       #Inserta un nuevo Simbolo en la tabla de Simbolos
        if simbolo:
            self.tabla_simbolos.append(simbolo)
        else:
            raise ValueError ("Se esperaba un simbolo.")

    def __cargar_palabras_reservadas(self):         #Carga las palabras reservadas en la tabla de simbolos
        for p in self.palabras_reservadas:
            self.inserta_simbolo(Simbolo(p,Simbolo.TOKENS[p.upper()]))
        self.FIN_PALABRAS_RESERVADAS = len(self.tabla_simbolos)

    def mostrar_tabla_simbolos(self):               #Muestra la tabla de simbolos
        for s in self.tabla_simbolos:
            print(s)

    def siguiente_caracter(self):
        self.__indice+=1
        try:
            return self.codigo_fuente[self.__indice]
        except IndexError:
            return '\0'

    def saltar_caracter(self):
        self.__indice += 1
        self.__inicio_lexema = self.__indice

    def leer_lexema(self):
        self.Lexema = self.codigo_fuente[self.__inicio_lexema:self.__indice + 1]
        self.__inicio = 0
        self.__estado = 0
        self.avanza_inicio_lexema()
        return self.Lexema

    def regresa_caracter(self):
        self.__indice -= 1

    def avanza_inicio_lexema(self):
        self.__inicio_lexema = self.__indice + 1

    def buscar_lexema(self, lexema):
        simb = [s for s in self.tabla_simbolos if lexema == s.Lexema]
        return simb[0] if len(simb)>0 else None

    def buscar_globales(self, lexema):  #Seccion 0
        for i in range(0, len(self.tabla_simbolos)):
            if self.tabla_simbolos[i].Lexema == lexema:
                return self.tabla_simbolos[i]
        return None

    def buscar_locales(self, lexema):   #Seccion 1
        for i in range(self.INICIO_LOCALES, len(self.tabla_simbolos)):
            if self.tabla_simbolos[i].Lexema == lexema:
                return self.tabla_simbolos[i]

        for i in range(0, self.FIN_PALABRAS_RESERVADAS):
            if self.tabla_simbolos[i].Lexema == lexema:
                return self.tabla_simbolos[i]
        return None

    def buscar_funcion(self, lexema):   #Seccion 2
        for i in range(self.INICIO_LOCALES, len(self.tabla_simbolos)):
            if self.tabla_simbolos[i].Lexema == lexema:
                return self.tabla_simbolos[i]

        for i in range(0, self.FIN_GLOBALES):
            if self.tabla_simbolos[i].Lexema == lexema:
                return self.tabla_simbolos[i]
        return None

    def buscar_principal(self, lexema):     #Seccion 3
        for i in range(0, self.FIN_GLOBALES):
            if self.tabla_simbolos[i].Lexema == lexema:
                return self.tabla_simbolos[i]
        return None






##        for s in self.tabla_simbolos:
##            if lexema == s.Lexema:
##                return s
##        return None

    def siguiente_componente_lexico(self):
        while(True):
            if self.__estado == 0:
                c = self.siguiente_caracter()
                if c ==' ' or c =='\t' or c == '\n':
                    if c == '\t' or c == '\n':
                        self.__num_linea += 1
                    self.avanza_inicio_lexema()
                elif c == '\0':
                    return None
                elif c == '<':
                    self.__estado = 1
                elif c == '=':
                    self.__estado = 5
                elif c == '>':
                    self.__estado = 6
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 1:
                c = self.siguiente_caracter()
                if c == '=':
                    self.__estado = 2
                elif c == '>':
                    self.__estado = 3
                else:
                    self.__estado = 4
            elif self.__estado == 2:
                self.leer_lexema()
                return(Simbolo(self.Lexema,Simbolo.TOKENS['MEI']))
            elif self.__estado == 3:
                self.leer_lexema()
                return(Simbolo(self.Lexema,Simbolo.TOKENS['DIF']))
            elif self.__estado == 4:
                self.regresa_caracter()
                self.leer_lexema()
                return(Simbolo(self.Lexema,Simbolo.TOKENS['MEN']))
            elif self.__estado == 5:
                self.leer_lexema()
                return(Simbolo(self.Lexema,Simbolo.TOKENS['IGU']))
            elif self.__estado == 6:
                c = self.siguiente_caracter()
                if c == '=':
                    self.__estado = 7
                else:
                    self.__estado = 8
            elif self.__estado == 7:
                self.leer_lexema()
                return Simbolo(self.Lexema, Simbolo.TOKENS['MAI'])
            elif self.__estado == 8:
                self.regresa_caracter()
                self.leer_lexema()
                return Simbolo(self.Lexema, Simbolo.TOKENS['MAY'])
            elif self.__estado == 9:
                if c.isalpha():
                    self.__estado = 10
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 10:
                c = self.siguiente_caracter()
                if c.isalnum():
                    pass
                else:
                    self.__estado = 11
            elif self.__estado == 11:
                self.regresa_caracter()
                self.leer_lexema()
                #s = self.buscar_lexema(self.Lexema)
                if self.SECCION == 0:     #Definicion de variables Globales.
                    s = self.buscar_globales(self.Lexema)
                    if s:
                        if s.Token != Simbolo.TOKENS['ID']:
                            return s
                        else:
                            self.register_error("La variable: '{}' ya estaba declarada.".format(s.Lexema))
                    else:
                        s = Simbolo(self.Lexema, Simbolo.TOKENS['ID'], self.TIPODATO)
                        self.inserta_simbolo(s)
                    return s
                elif self.SECCION == 1:     #Definicion de variables Locales.
                    s = self.buscar_locales(self.Lexema)
                    if s:
                        if s.Token != Simbolo.TOKENS['ID']:
                            return s
                        else:
                            self.register_error("La variable: '{}' ya estaba declarada en el ambito actual.".format(s.Lexema))
                    else:
                        s = Simbolo(self.Lexema, Simbolo.TOKENS['ID'], self.TIPODATO)
                        self.inserta_simbolo(s)
                    return s
                elif self.SECCION == 2:     #Cuerpo de funcion.
                    s = self.buscar_funcion(self.Lexema)
                    if not s:
                        self.register_error("La variable '{}' no esta definida.".format(self.Lexema))
                        s = Simbolo(self.Lexema, Simbolo.TOKENS['ID'], tipoDato["na"])
                        self.inserta_simbolo(s)
                    return s
                elif self.SECCION == 3:     #Cuerpo principal.
                    s = self.buscar_principal(self.Lexema)
                    if not s:
                        self.register_error("La variable '{}' no esta definida".format(self.Lexema))
                        s = Simbolo(self.Lexema, Simbolo.TOKENS['ID'], tipoDato["na"])
                        self.inserta_simbolo(s)
                    return s
            elif self.__estado == 12:
                if c.isnumeric():
                    self.__estado = 13
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 13:
                c=self.siguiente_caracter()
                if c.isnumeric():
                    pass
                elif c=='.':
                    self.__estado = 14
                elif c.upper()=='E':
                    self.__estado = 16
                else:
                    self.__estado = 20
            elif self.__estado == 14:
                c=self.siguiente_caracter()
                if c.isnumeric():
                    self.__estado = 15
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 15:
                c=self.siguiente_caracter()
                if c.isnumeric():
                    pass    #self.__estado = 15
                elif c.upper() == 'E':
                    self.__estado = 16
                else:
                    self.__estado = 21
            elif self.__estado == 16:
                c=self.siguiente_caracter()
                if c=='+' or c=='-':
                    self.__estado = 17
                elif c.isnumeric():
                    self.__estado = 18
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 17:
                c=self.siguiente_caracter()
                if c.isnumeric():
                    self.__estado = 18
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 18:
                c=self.siguiente_caracter()
                if c.isnumeric():
                    pass    #self.__estado = 18
                else:
                    self.__estado = 19
            elif self.__estado == 19:
                self.regresa_caracter()
                self.leer_lexema()
                return Simbolo(self.Lexema, Simbolo.TOKENS['NUMF'])
            elif self.__estado == 20:
                self.regresa_caracter()
                self.leer_lexema()
                simb = Simbolo(self.Lexema, Simbolo.TOKENS['NUM'],tipoDato['int'])
                self.inserta_simbolo(simb)
                return simb
            elif self.__estado == 21:
                self.regresa_caracter()
                self.leer_lexema()
                return Simbolo(self.Lexema, Simbolo.TOKENS['NUMF'])
            elif self.__estado == 22:
                if c == '"':
                    self.__estado = 23
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 23:
                c = self.siguiente_caracter()
                if c == '\\':
                    self.__estado = 24
                elif c == '"':
                    self.__estado = 25
                else:
                    pass
            elif self.__estado == 24:
                c = self.siguiente_caracter()
                if c in r'\ntra"':
                    self.__estado = 23
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 25:
                self.leer_lexema()
                return Simbolo(self.Lexema, Simbolo.TOKENS['CONST_STRING'])
            elif self.__estado == 26:
                if c =="'":
                    self.__estado = 27
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 27:
                c =self.siguiente_caracter()
                if c == '\\':
                    self.__estado = 28
                elif c == "'":
                    self.__estado = self.fallo()
                else:
                    self.__estado = 29
            elif self.__estado == 28:
                c = self.siguiente_caracter()
                if c in r'\"ntra':
                    self.__estado = 29
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 29:
                c = self.siguiente_caracter()
                if c == "'":
                    self.__estado = 30
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 30:
                self.leer_lexema()
                return Simbolo(self.Lexema, Simbolo.TOKENS['CONST_CHAR'])
            elif self.__estado == 31:
                if c == '/':
                    self.__estado = 32
                else:
                    self.__estado = self.fallo()
            elif self.__estado == 32:
                c= self.siguiente_caracter()
                if c == '/':
                    self.__estado = 33
                elif c == '*':
                    self.__estado = 35
                else:
                    c = self.deshacer()
                    self.__estado = self.fallo()
            elif self.__estado == 33:
                c= self.siguiente_caracter()
                if c == '\n' or c == '\r' or c == '\0':
                    self.__estado = 34
                else:
                    pass
            elif self.__estado == 34:
                self.leer_lexema()
                self.__estado = 0
                self.__inicio = 0
            elif self.__estado == 35:
                c = self.siguiente_caracter()
                if c == '*':
                    self.__estado = 36
                else:
                    pass
            elif self.__estado == 36:
                c= self.siguiente_caracter()
                if c == '/':
                    self.__estado = 34
                else:
                    self.__estado = 35
            elif self.__estado == 37:
                if c in self.CARACTERES_VALIDOS:
                    self.leer_lexema()
                    return Simbolo(self.Lexema, ord(c))
                else:
                    self.leer_lexema()
                    print("El simbolo '{}' no esta permitido.".format(c))
                    self.__estado = self.fallo()
            else:
                return None

    def fallo(self):
        if self.__inicio == 0:
            self.__inicio = 9
        elif self.__inicio == 9:
            self.__inicio = 12
        elif self.__inicio== 12:
            self.__inicio = 22
        elif self.__inicio == 22:
            self.__inicio = 26
        elif self.__inicio == 26:
            self.__inicio = 31
        elif self.__inicio == 31:
            self.__inicio = 37
        elif self.__inicio == 37:
            self.__inicio = 0
        return self.__inicio

    def deshacer(self):
        self.__indice = self.__inicio_lexema
        return self.codigo_fuente[self.__indice]

    def Num_linea(self):
        return self.__num_linea

    def register_error(self,message):
        print("Ln: {}, {}".format(self.Num_linea(),message))
