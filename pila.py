class Pila():
    def __init__(self):
        self.pila = []
        self.tope = -1

    def push(self, item):
        self.tope += 1
        self.pila[self.tope] = item

    def pop(self):
        if self.tope > 0:
            item = self.pila[self.tope]
            self.tope -= 1
            return item
        else:
            raise IndexError("Indice fuera de rango")
