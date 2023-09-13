import math
import random

from Memoria import Memoria
from Disco import Disco

class RAM(Memoria):
    def __init__(self, num_pag_fisicas, num_pag_logicas, tam_pag):
        super().__init__(num_pag_fisicas, tam_pag)
        self.mem_logica = Disco(num_pag_logicas, tam_pag)

    def aloca_processo(self, processo):
        num_paginas_processo = math.floor(processo.tamanho / self.tam_pagina)

        draw = [random.randint(0, 2) for _ in range(num_paginas_processo - 1)]
        draw.insert(0, 1)

        pag_memoria_fisica = draw.count(1)
        if not self.existe_espaco(pag_memoria_fisica):
            return print('Sem espaço em memória física.')

        if not self.mem_logica.existe_espaco(num_paginas_processo - pag_memoria_fisica):
            return print('Sem espaço em memória lógica.')

        espaco_ultima_pagina = processo.tamanho % self.tam_pagina

        for i, valor in enumerate(draw):
            if valor == 1:
                self.busca_pagina_livre().aloca(processo, i, espaco_ultima_pagina, (i + 1) != num_paginas_processo)
            else:
                self.mem_logica.busca_pagina_livre().aloca(processo, i, espaco_ultima_pagina, (i + 1) != num_paginas_processo)