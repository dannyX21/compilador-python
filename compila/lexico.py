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

