class Semantico():
    def __init__(self):
        Semantico.temp = -1
        self.code = ""

    def genTemp(self):
        Semantico.temp += 1
        return "_tmp" + str(Semantico.temp)

    def genTAC(self, code):
        self.code += code
