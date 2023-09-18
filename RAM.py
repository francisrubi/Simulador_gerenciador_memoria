import math
import random

from Memoria import Memoria
from Memoria import converte_binario
from Disco import Disco

class RAM(Memoria):
    def __init__(self, num_pag_fisicas, num_pag_logicas, tam_pag):
        super().__init__(num_pag_fisicas, tam_pag)
        self.mem_logica = Disco(num_pag_logicas, tam_pag)

    def aloca_processo(self, processo):
        num_paginas_processo = math.floor(processo.tamanho / self.tam_pagina)

        draw = [random.randint(0, 2) for _ in range(num_paginas_processo)]
        draw.insert(0, 1)

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
    
    def mostra_memoria(self):
        print()
        self.mostra_paginas_memoria_fisica()
        print()
        self.mostra_paginas_so()

    def mostra_paginas_so(self):
        print('NPF / BP')

        tam_bin_pag = int(math.log2(len(self.paginas)))
        form_pag = max(tam_bin_pag, 3)

        for i, p in enumerate(self.paginas):
            print(f'{i:<{tam_bin_pag}} / {str(1 if p.ocupada else 0)}')
    
    def mostra_paginas_memoria_fisica(self):

        tam_bin_pag = int(math.log2(len(self.paginas)))
        deslocamento = int(math.log2(self.tam_pagina))

        form_pag = max(tam_bin_pag, 3)
        form_desl = max(deslocamento, 12)
        
        print(f"{'NPF':<{tam_bin_pag}} / {'DESLOCAMENTO':<{deslocamento}} / DADOS")

        for npag, pag in enumerate(self.paginas):
            npf = f'{converte_binario(npag, tam_bin_pag)}'
            dados = f'{pag.processo.nome if pag.ocupada else ""}'

            for i, b in enumerate(pag.bytes):
                print(f'{npf:<{form_pag}} / {converte_binario(i, deslocamento):<{form_desl}} / {dados if b == 1 else ""}')