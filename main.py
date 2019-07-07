import sys
import time

# CONTRUINDO...

while True:
	try:
		print("""
    ______                                                              ______                _           _ 
   |  ____|                                                            |  ____|              (_)         | |
   | |__    __  __  _ __    _ __    ___   ___   ___    __ _    ___     | |__    __ _    ___   _    __ _  | |
   |  __|   \ \/ / | '_ \  | '__|  / _ \ / __| / __|  / _` |  / _ \    |  __|  / _` |  / __| | |  / _` | | |
   | |____   >  <  | |_) | | |    |  __/ \__ \ \__ \ | (_| | | (_) |   | |    | (_| | | (__  | | | (_| | | |
   |______| /_/\_\ | .__/  |_|     \___| |___/ |___/  \__,_|  \___/    |_|     \__,_|  \___| |_|  \__,_| |_|
                   | |                                                                                        
                   |_|                                                                                        

		+-------------------------------------------------------------------------------+
		|                            Selecione uma Opção                                |
		+-------------------------------------------------------------------------------+

		+--------------------------------------+ +--------------------------------------+
		| [1] Reconhecer expressão             | | [6] Espelhar fotos                   |
		+--------------------------------------+ +--------------------------------------+
		| [2] Ver expressões                   | | [7] Renomear fotos                   |
		+--------------------------------------+ +--------------------------------------+
		| [3] Criar dados com a Webcam         | | [8] Treinar rede do início           |
		+--------------------------------------+ +--------------------------------------+
		| [4] Criar dados com fotos            | | [9] Retreinar rede com checkpoint    |
		+--------------------------------------+ +--------------------------------------+
		| [5] Carregar database                | | [10] Calcular erro da rede           |
		+--------------------------------------+ +--------------------------------------+
		+--------------------------------------+ +--------------------------------------+
		| [0] Sair do programa                 | | [99] Ajuda                           |
		+--------------------------------------+ +--------------------------------------+
			
		    """)

		opcao = int(input("	Digite a opção escolhida: "))

		if (opcao == 1):
			from menu.reconhecer import reconhecer
			break	

		elif (opcao == 2):
			from menu.mostrar_tudo import mostrar_tudo
			break

		elif (opcao == 3):
			from menu.criar_web import criar_web
			break

		elif (opcao == 4):
			from menu.criar_local import criar_local
			break

		elif (opcao == 5):
			from menu.dados_img import dados_img
			break

		elif (opcao == 6):
			from menu.espelhar import espelhar
			break

		elif (opcao == 7):
			from menu.renomear import renomear
			break

		elif (opcao == 8):
			from menu.treinar import treinar
			break

		elif (opcao == 9):
			from menu.retreinar import retreinar
			break

		elif (opcao == 10):
			from modelo.erro import erro
			break

		elif (opcão == 0):
			print("Finalizando o programa...")
			sys.exit(0)	

		elif (opcão == 99):
			print("Menu de ajuda:")
			print("""

					ESCREVER AQUI

					""")
				
	except:
		print("Ops! Ocorreu um erro. Tente novamente!")
		print("3...")
		time.sleep(1)
		print("2...")
		time.sleep(1)
		print("1...")
		time.sleep(1)
		print("")
