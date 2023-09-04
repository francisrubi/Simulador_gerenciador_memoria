import math
import random

from Memoria import Memoria
from Disco import Disco

class RAM(Memoria):
    def __init__(self, num_pag_fisicas, num_pag_logicas, tam_pag):
        super().__init__(num_pag_fisicas, tam_pag)
        self.mem_logica = Disco(num_pag_logicas, tam_pag)

    def aloca_processo(self, processo):
        if not self.existe_espaco():
            return print('Sem espaço em memória.')

        num_paginas_processo = math.floor(processo.tamanho / self.tam_pagina)

        draw = [random.randint(0, 2) for _ in range(num_paginas_processo - 1)]

        for i in draw:
            if i == 1:
                self.aloca_processo