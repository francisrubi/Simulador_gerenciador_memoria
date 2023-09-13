class Pagina():
    def __init__(self, tamanho):
        self.bytes = [0] * tamanho
        self.ocupada = False
        self.processo = None
        self.parte_processo = None

    def aloca(self, p, index, qtde, full=False):
        self.ocupada = True
        self.processo = p
        self.parte_processo = index
        
        if full:
            qtde = len(self.bytes)
        
        for _ in range(qtde):
            self.bytes[_] = 1
    
    def desaloca(self):
        self.ocupada = False
        self.processo = None
        self.parte_processo = None

        tam = len(self.bytes)
        self.bytes = [0] * tam