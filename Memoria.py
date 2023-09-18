from Pagina import Pagina

def converte_binario(n, t):
    return format(n, 'b').zfill(t)

class Memoria:
    def __init__(self, num_pag, tam_pag):
        self.paginas = [
            Pagina(tam_pag) for _ in range(num_pag)
        ]
        self.tam_pagina = tam_pag

    def busca_pagina_livre(self):
        for p in self.paginas:
            if not p.ocupada:
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
    
    def calcula_porcentagem(self):
        paginas_ocupadas = len(
            list(filter(
                lambda p: p.ocupada,
                self.paginas
            ))
        )

        porcentagem_ocupadas = paginas_ocupadas / len(self.paginas) * 100
        porcentagem_livres = 100 - porcentagem_ocupadas

        return (porcentagem_ocupadas, porcentagem_livres)