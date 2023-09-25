import math
import random

from Memoria import Memoria
from Memoria import converte_binario, log_base2
from Disco import Disco

class RAM(Memoria):
    def __init__(self, num_pag_fisicas, num_pag_logicas, tam_pag):
        super().__init__(num_pag_fisicas, tam_pag)
        self.mem_logica = Disco(num_pag_logicas, tam_pag)

    def aloca_processo(self, processo):
        num_sorteadas = math.ceil(processo.tamanho / self.tam_pagina) - 1

        draw = [random.randint(0, 2) for _ in range(num_sorteadas)]
        draw.insert(0, 1)

        num_paginas_processo = len(draw)
        pag_memoria_fisica = draw.count(1)
        if not self.existe_espaco(pag_memoria_fisica):
            return print('Sem espaço em memória física.')

        if not self.mem_logica.existe_espaco(num_paginas_processo - pag_memoria_fisica):
            return print('Sem espaço em memória lógica.')

        espaco_ultima_pagina = processo.tamanho % self.tam_pagina

        for i, valor in enumerate(draw):
            if valor == 1:
                self.busca_pagina_livre().aloca(processo, i, espaco_ultima_pagina, i != num_paginas_processo)
            else:
                self.mem_logica.busca_pagina_livre().aloca(processo, i, espaco_ultima_pagina, i != num_paginas_processo)
    
    def mostra_memoria_fisica(self):
        print()
        print('MEMÓRIA FÍSICA:')
        self.mostra_paginas_memoria_dados()
        print()
        self.mostra_paginas_memoria()
    
    def mostra_memoria_logica(self):
        print()
        print('MEMÓRIA LÓGICA:')
        self.mem_logica.mostra_paginas_memoria_dados()
        print()
        self.mem_logica.mostra_paginas_memoria()
    
    def mostra_paginas_processo(self, processo):
        paginas_processo = list(filter(
            lambda p: p.processo == processo,
            self.paginas
        ))

        tam_bin_pag = int(log_base2(len(self.paginas)))
        tam_bin_pag_logica = int(log_base2(len(self.mem_logica.paginas)))

        form_pag = max(tam_bin_pag_logica, 3)
        
        print(f"{'NPL':<{form_pag}} / NPF")

        for i, p in enumerate(paginas_processo):
            npf = ''

            if p in self.paginas:
                index_pag_fisica = self.paginas.index(p)
                npf = converte_binario(index_pag_fisica, tam_bin_pag)

            print(f'{converte_binario(i, tam_bin_pag_logica):<{form_pag}} / {npf}')