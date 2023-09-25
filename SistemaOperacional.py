# módulo que permite executar funções assíncronas
# necessário para permitir as entradas do usuário ao mesmo tempo que são executados os processos
import threading
import time

from Processo import Processo
from RAM import RAM
from Disco import Disco

class SistemaOperacional:
    def __init__(self, tam_ram, tam_disco, tam_pagina, quantum):
        # controla o tempo corrido desde o início da execução dos processos
        self.tempo_programa = 0

        # verifica se o tamanho das memórias física e lógica é múltiplo do tamanho das páginas
        if tam_ram % tam_pagina != 0:
            raise Exception('Tamanho da memória física não comporta o tamanho da página.')
        self.num_pag_fisicas = int(tam_ram / tam_pagina)

        if tam_disco % tam_pagina != 0:
            raise Exception('Tamanho da memória lógica não comporta o tamanho da página.')
        self.num_pag_logicas = int(tam_disco / tam_pagina)

        # inicializa as memórias física e lógica
        self.mem_fisica = RAM(self.num_pag_fisicas, self.num_pag_logicas, tam_pagina)

        # processo que está atualmente em execução
        self.processo_execucao = None
        self.quantum = quantum

        self.fila_aptos = []
        self.fila_aptos_historico = []

        # cria uma thread, onde serão executados os processos assincronamente
        self.processador = threading.Thread(target=self.executa_processos)
        # variável de controle para interromper a execução
        self.executando = True
        # inicializa a execução dos processos
        self.processador.start()

    # classes internas de página para memória e de processo em fila
    #region Classes Internas
    class ProcessoFila:
        def __init__(self, processo, tempo_chegada):
            self.processo = processo
            processo.estado = 'A'
            self.TCF = tempo_chegada
            self.TSF = None
    #endregion
    
    #region Manipulação de processos

    def insere_processo_fila(self, processo):
        pf = self.ProcessoFila(processo, self.tempo_programa)
        self.fila_aptos.append(pf)
        self.fila_aptos_historico.append(pf)
    
    def novo_processo(self, nome, tamanho, tempo_processo):
        p = Processo(nome, self.tempo_programa, tempo_processo, tamanho)
        self.mem_fisica.aloca_processo(p)
        self.insere_processo_fila(p)

    def encerra_processo_pid(self, pid):
        processo = self.busca_processo_pid(pid)

        if processo is not None and processo.estado in ['A', 'E']:
            self.encerra_processo(processo)

    def encerra_processo(self, processo):
        if (self.processo_em_execucao == processo):
            self.processo_em_execucao = None

        processo.encerra()
        self.desaloca_processo(processo)
        self.fila_aptos = [p for p in self.fila_aptos if p.processo != processo]
    
    def encerra_todos_processos(self):
        for p in reversed(self.processos):
            if p.estado in ['A', 'E']:
                print(f'Encerrando processo {p.PID}...')
                self.encerra_processo(p)

    
    def encerra_programa(self):
        if len(self.processos) > 0:
            self.encerra_todos_processos()
        self.executando = False
        self.processador.join()
    
    def desaloca_processo(self, processo):
        self.mem_fisica.desaloca_processo(processo)
        self.mem_fisica.mem_logica.desaloca_processo(processo)

    def finaliza_processo(self, processo):
        processo.finaliza(self.tempo_programa)
        self.desaloca_processo(processo)

    #endregion

    # Inserir funções de print aqui
    #region Funções Print
    def mostra_fila_aptos_historico(self, ativos=False):
        if len(self.fila_aptos_historico) == 0:
            print('FILA VAZIA')
        else:
            print('PID / TCF / TEF / TSF')
            
            for p in self.fila_aptos_historico:
                if p.processo.executado or ativos:
                    print(f'{p.processo.PID:<6}{p.TCF:<6}{(p.TSF - p.TCF):<6}{p.TSF}')

    def mostra_fila_aptos(self):
        if len(self.fila_aptos) == 0:
            print('FILA VAZIA')
        else:
            print('PID / TCF / TEF / TRE')
            
            for p in self.fila_aptos:
                print(f'{p.processo.PID:<6}{p.TCF:<6}{(self.tempo_programa - p.TCF):<6}{p.processo.TP - p.processo.TE}')
    #endregion
    
    #region Processos
    def mostra_lista_processos(self, ativos):
        processos = [
            p for p in self.processos
            if p.estado in ['A', 'E'] if ativos
        ]

        for i, p in enumerate(processos):
            self.mostra_processo(p, i == 0)

    def mostra_processo(self, processo, cabecalho = True):
        if cabecalho:
            print('PID / TC / TE / TP / TAMANHO / NOME / E')
        print(str(processo))
    
    def mostra_processo_excucao(self):
        self.mostra_processo(self.processo_em_execucao)
    
    def mostra_processo_id(self, pid):
        processo = self.busca_processo_pid(pid)

        if processo is not None:
            self.mostra_processo(processo)
    #endregion

    #region Memória
    def mostra_memoria_fisica(self):
        (porcentagem_ocupadas, porcentagem_livres) = self.mem_fisica.calcula_porcentagem()
        
        print(f'Memória física: {porcentagem_ocupadas}% ocupada, {porcentagem_livres}% livre')
        
        self.mem_fisica.mostra_memoria_fisica()

    def mostra_tabela_paginas(self):
        self.mem_fisica.mostra_paginas_memoria()
    
    def mostra_tabela_paginas_processo(self, pid):
        p = self.busca_processo_pid(pid)
        if p is not None:
            self.mem_fisica.mostra_paginas_processo(p)
    #endregion
    #endregion

    #region Execução de processos
    def busca_primeiro_fila(self):
        if len(self.fila_aptos) > 0:
            return self.fila_aptos[0]
        else:
            return None

    def executa_processos(self):
        while self.executando:
            em_execucao = self.processo_execucao

            primeiro_fila = self.busca_primeiro_fila()
            if primeiro_fila is not None:
                primeiro_fila.TSF = self.tempo_programa
                em_execucao = primeiro_fila.processo
                self.fila_aptos.remove(primeiro_fila)

            if em_execucao is None:
                time.sleep(1)
                self.tempo_programa += 1

            else:
                self.processo_execucao = em_execucao
                em_execucao.estado = 'E'

                tempo = 0
                if self.quantum < (em_execucao.TP - em_execucao.TE):
                    tempo = self.quantum
                else:
                    tempo = (em_execucao.TP - em_execucao.TE)
                
                tempo_final = self.tempo_programa + tempo
                while self.tempo_programa < tempo_final and self.processo_execucao is not None:
                    time.sleep(1)
                    em_execucao.TE += 1
                    self.tempo_programa += 1
                
                if self.processo_execucao is not None:
                    if em_execucao.TE == em_execucao.TP:
                        self.finaliza_processo(em_execucao)
                        self.processo_em_execucao = None

                    elif len(self.fila_aptos) > 0:
                        self.insere_processo_fila(em_execucao)                    
                        self.processo_em_execucao = None
    #endregion