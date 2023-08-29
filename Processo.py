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
        return f'{self.PID:<5}{self.TC:<4}{self.TE:<4}{self.TP:<4}{self.tamanho:<5}{self.nome:<3}{self.estado}'