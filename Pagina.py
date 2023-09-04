class Pagina():
    def __init__(self, tamanho):
        self.bytes = [0] * tamanho
        self.ocupada = False
        self.processo = None

    def aloca(self, p, qtde, full=False):
        self.ocupada = True
        self.processo = p
        
        if full:
            qtde = len(self.bytes)
        
        for _ in range(qtde):
            self.bytes[_] = 1
    
    def desaloca(self):
        self.ocupada = False
        self.processo = None

        tam = len(self.bytes)
        self.bytes = [0] * tam