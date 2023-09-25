# classe para os processos que o usuário insere no sistema operacional
class Processo():
    # identificador único para cada processo
    id = 1
    def __init__(self, nome, temp_chegada, temp_processo, tamanho):
        self.PID = Processo.id
        Processo.id += 1

        self.TP = temp_processo
        self.nome = nome
        self.tamanho = tamanho
        self.TC = temp_chegada
        self.TE = 0
        self.TT = None
        self.executado = False
        self.estado = 'A'
    
    def __str__(self):
        return f'{self.PID:<3} / {self.TC:<2} / {self.TE:<2} / {self.TP:<2} / {self.tamanho:<7} / {self.nome:<4} / {self.estado}'
    
    def finaliza(self, tempo):
        self.TT = tempo
        self.estado = 'F'
        self.executado = True

    def encerra(self):
        self.executado = True
        self.estado = ''