from simbolo import Simbolo

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
            
##        for s in self.tabla_simbolos:
##            if lexema == s.Lexema:
##                return s
##        return None

    def siguiente_componente_lexico(self):
        while(True):
            if self.__estado == 0:
                c = self.siguiente_caracter()
                if c ==' ' or c =='\t' or c == '\n':
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
                s = self.buscar_lexema(self.Lexema)
                if not s:                    
                    s = Simbolo(self.Lexema, Simbolo.TOKENS['ID'])
                    self.inserta_simbolo(s)
                return s               
            else:
                return None

    def fallo(self):
        if self.__inicio == 0:
            self.__inicio = 9
            return self.__inicio
        elif self.__inicio == 9:
            self.__inicio = 12
            return self.__inicio
                
