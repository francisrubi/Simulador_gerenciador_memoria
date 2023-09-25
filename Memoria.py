import math

from Pagina import Pagina

def log_base2(n):
    return math.log(n, 2)

def converte_binario(n, t = 0):
    return format(n, 'b').zfill(t)

class Memoria:
    def __init__(self, num_pag, tam_pag):
        self.paginas = [
            Pagina(tam_pag) for _ in range(num_pag)
        ]
        self.tam_pagina = tam_pag
        self.tamanho = num_pag * tam_pag

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

        return qtde_paginas_livres >= num_paginas
    
    def desaloca_processo(self, p):
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
    
    def mostra_paginas_memoria(self):
        print('NPF / BP')

        tam_bin_pag = int(log_base2(len(self.paginas)))
        form_pag = max(tam_bin_pag, 3)

        for i, p in enumerate(self.paginas):
            print(f'{i:<{tam_bin_pag}} / {str(1 if p.ocupada else 0)}')
    
    def mostra_paginas_memoria_dados(self):

        tam_bin_pag = int(log_base2(len(self.paginas)))
        deslocamento = int(log_base2(self.tam_pagina))

        form_pag = max(tam_bin_pag, 3)
        form_desl = max(deslocamento, 12)
        
        print(f"{'NPF':<{form_pag}} / {'DESLOCAMENTO':<{form_desl}} / DADOS")

        for npag, pag in enumerate(self.paginas):
            npf = f'{converte_binario(npag, tam_bin_pag)}'
            dados = f'{pag.processo.nome if pag.ocupada else ""}'

            for i, b in enumerate(pag.bytes):
                print(f'{npf:<{form_pag}} / {converte_binario(i, deslocamento):<{form_desl}} / {dados if b == 1 else ""}')