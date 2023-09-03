import math
import random

from Pagina import Pagina
from Disco import Disco

class RAM:
    def __init__(self, num_pag_fisicas, num_pag_logicas, tam_pag):
        self.paginas = [Pagina(tam_pag)] * num_pag_fisicas
        self.mem_logica = Disco(num_pag_logicas, tam_pag)

        self.tam_pagina = tam_pag

    def pagina_livre(self):
        for p in self.paginas:
            if not p.processo.ocupada:
                return p
        
        return None

    def aloca_processo(self, processo):
        num_paginas_processo = math.floor(processo.tamanho / self.tam_pagina)

        pag_livre = self.pagina_livre()
        if pag_livre is not None:
            pag_livre.aloca(processo, full=True)

        for _ in range(num_paginas_processo - 1):
            draw = random.randint(0, 2)
            if draw == 1:
                pag_livre = self.pagina_livre()
                if pag_livre is not None:
                    pag_livre.aloca(processo, full=True)