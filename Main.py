import threading

from SistemaOperacional import SistemaOperacional

def verifica_entrada(so, entrada):
    if(entrada[0] == '$'):

        if len(entrada) == 4:
            tamanho = int(entrada[2])
            tempo = int(entrada[3])

            so.novo_processo(entrada[1], tamanho, tempo)
            
        else:
            pid = None
            if len(entrada) == 3:
                pid = int(entrada[2])

            match entrada[1]:
                case 'kill':
                    if pid is not None:
                        so.encerra_processo_pid(pid)
                    elif entrada[2] == 'all':
                        so.encerra_programa()

                case 'mem':
                    so.mostra_memoria_fisica()

                case 'shutdown':
                    so.encerra_programa()
                case 'exit':
                    so.encerra_programa()

                case 'fa':
                    so.mostra_fila_aptos()

                case 'fah':
                    so.mostra_fila_aptos_historico()
                
                case 'tp':
                    if pid is not None:
                        None
                    else:
                        None
                
                case 'ps':
                    if isinstance(pid, int):
                        so.mostra_processo_id(pid)
                    else:    
                        so.mostra_lista_processos(True)
                
                case 'psh':
                    so.mostra_lista_processos(False)
                
                case 'pse':
                    so.mostra_processo_excucao()

def realiza_leitura(so):
    while so.executando:
        opcao = input()

        entrada = tuple(str.split(opcao))

        verifica_entrada(so, entrada)


def main():

    sistema = SistemaOperacional(32, 64, 4, 5)
    
    leitura = threading.Thread(target=realiza_leitura, kwargs={'so': sistema})
    leitura.start()

if __name__ == '__main__':
    main()