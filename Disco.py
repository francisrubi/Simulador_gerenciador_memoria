from Pagina import Pagina

class Disco:
    def __init__(self, num_pag, tam_pag):
        self.paginas = [Pagina(tam_pag)] * num_pag