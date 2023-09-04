from SistemaOperacional import SistemaOperacional
def menu():
    print("==== Simulador de Sistema Operacional ====")
def main():
    sistema = SistemaOperacional(tam_ram=1024, tam_disco=2048, tam_pagina=256, quantum=1)
    options=[]
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        entrada = str.split(opcao)
        if(entrada[0]=='$'):
            match entrada[1]:
                case 'all':
                    print('1')
                case 'kill':
                    print("2")
                case 'mem':
                    print("1")
                case 'shutdown':
                    print("1")
                case 'fa':
                    print(sistema.mostra_fila_aptos)
                case 'fah':
                    print(sistema.mostra_fila_aptos_historico)
                case 'ps':
                    print("1")
                case 'psPid':
                    print("1")
                case 'pse':
                    print("1")

if __name__ == "__main__":
    main()
