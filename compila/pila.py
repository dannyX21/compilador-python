class Pila():
    def __init__(self):
        self.pila = []

    def push(self, item):
        self.pila.append(item)

    def pop(self):
        if len(self.pila) > 0:
            return self.pila.pop()
        else:
            raise IndexError("Indice fuera de rango")
