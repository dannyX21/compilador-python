tipoDato = {
"int": 0,
"bool": 1,
"float":2,
"char":3,
"string":4,
"void": 5,
"na": 6
}

tipoDatoText = { value: key for key, value in tipoDato.items()}

class Simbolo:
    def __init__(self, lexema, token, tipoDato=tipoDato["na"]):
        self.Lexema = lexema
        self.Token = token
        self.TipoDato = tipoDato

    def __repr__(self):
        return "Lexema: '{}', Token: {}, TipoDato: {}".format(self.Lexema, self.Token, tipoDatoText[self.TipoDato])

    TOKENS = {
    'BOOL': 256,
    'CALL': 257,
    'CHAR': 258,
    'CONST_CHAR': 259,
    'CONST_STRING' : 260,
    'DIF' : 261,
    'DO' : 262,
    'ELSE' : 263,
    'FLOAT' : 264,
    'FOR' : 265,
    'FUNCTION' : 266,
    'ID' : 267,
    'IF' : 268,
    'IGU' : 269,
    'INT' : 270,
    'MAI' : 271,
    'MAIN' : 272,
    'MAY' : 273,
    'MEI' : 274,
    'MEN' : 275,
    'NUM' : 276,
    'NUMF' : 277,
    'READ' : 278,
    'RETURN' : 279,
    'STRING' : 280,
    'THEN' : 281,
    'TO' : 282,
    'VOID' : 283,
    'WHILE' : 284,
    'WRITE' : 285,
    'FALSE' : 286,
    'TRUE' : 287
    }
