from Pagina import Pagina

class Memoria:
    def __init__(self, num_pag, tam_pag):
        self.paginas = [Pagina(tam_pag)] * num_pag
        self.tam_pagina = tam_pag
    
    def pagina_livre(self):
        for p in self.paginas:
            if not p.processo.ocupada:
                return p
        
        return None
        
    def existe_espaco(self, num_paginas=1):
        qtde_paginas_livres = len(
            list(filter(
                lambda p: not p.ocupada,
                self.paginas
            ))
        )

        return qtde_paginas_livres > num_paginas
    
    def desaloca_processo(p):
        for pag in self.paginas:
            if pag.processo == p:
                pag.desaloca()