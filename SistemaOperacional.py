# módulo que permite executar funções assíncronas
# necessário para permitir as entradas do usuário ao mesmo tempo que são executados os processos
import threading
import time
import random

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

        # inicializa uma lista com as páginas nas memórias
        self.mem_fisica = RAM(self.num_pag_fisicas, self.num_pag_logicas, tam_pagina)

        # processo que está atualmente em execução
        self.processo_execucao = None
        self.quantum = quantum

        self.fila_aptos = []
        self.fila_aptos_historico = []

        # cria uma thread, onde serão executados os processos assincronamente
        self.processador = threading.Thread(target=self.executa_processos)
        # variável de controle para interromper a execução
        # (pode ser implementado um método pause a partir disto)
        self.executando = True
        # inicializa a execução dos processos
        self.processador.start()

    # classes internas de página para memória e de processo em fila
    #region Classes Internas
    class ProcessoFila:
        def __init__(self, processo, tempo_chegada):
            self.processo = processo
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

    # def encerra_processo(self, pid):
    #     self.fila_aptos = [p for p in self.fila_aptos if p.processo.PID != pid]
    #     if (self.processo_execucao.PID == pid):
    #         self.processo_execucao = None

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

    def executa_processos(self):
        while self.executando:
            em_execucao = self.processo_execucao

            primeiro_fila = next(iter(self.fila_aptos), None)
            if primeiro_fila is not None:
                primeiro_fila.TSF = self.tempo_programa
                em_execucao = primeiro_fila.processo
                self.fila_aptos.pop(0)

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
                        self.processo_execucao = None
                        em_execucao.TT = self.tempo_programa
                        em_execucao.executado = True
                    elif len(self.fila_aptos) > 0:
                        self.insere_processo_fila(em_execucao)