from simbolo import tipoDato

matrizSuma = [
[0, 6, 2, 6, 6],
[6, 6, 6, 6, 6],
[2, 6, 2, 6, 6],
[6, 6, 6, 4, 4],
[6, 6, 6, 4, 4]
]

class Semantico():
    def __init__(self):
        Semantico.temp = -1
        Semantico.label = -1
        self.code = ""

    def genTemp(self):
        Semantico.temp += 1
        return "_tmp" + str(Semantico.temp)

    def genTAC(self, code):
        self.code += (code + "\n")

    def genLabel(self):
        Semantico.label += 1
        return "_Lbl" + str(Semantico.label)

    def verificar(self, operando, operando1, operando2):
        if operando == '+':
            return self.verificaSuma(operando1, operando2)

    def verificaSuma(self, operando1, operando2):
        if operando1 > 4 or operando2 > 4:
            return tipoDato['na']
        else:
            return matrizSuma[operando1][operando2]
