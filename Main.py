import threading

from SistemaOperacional import SistemaOperacional

def verifica_entrada(so, entrada):
    if(entrada[0] == '$'):

        if len(entrada) == 4:
            tamanho = int(entrada[2])
            tempo = int(entrada[3])

            so.novo_processo(entrada[1], tamanho, tempo)
            
        else:
            match entrada[1]:
                case 'kill':
                    if entrada[2] == 'pid':
                        print('1')
                    elif entrada[2] == 'all':
                        print('1')

                case 'mem':
                    print('1')

                case 'shutdown':
                    print('1')

                case 'fa':
                    so.mostra_fila_aptos()

                case 'fah':
                    so.mostra_fila_aptos_historico()
                
                case 'tp':
                    if isinstance(entrada[2], int):
                        print('1')
                    else:
                        print('1')
                
                case 'ps':
                    if isinstance(entrada[2], int):
                        print('1')
                    else:    
                        print('1')
                
                case 'psh':
                    print('1')
                
                case 'pse':
                    print('1')

def realiza_leitura(so):
    while True:
        opcao = input()

        entrada = tuple(str.split(opcao))

        verifica_entrada(so, entrada)


def main():

    sistema = SistemaOperacional(32, 64, 8, 5)
    
    leitura = threading.Thread(target=realiza_leitura, kwargs={'so': sistema})
    leitura.start()

if __name__ == '__main__':
    main()