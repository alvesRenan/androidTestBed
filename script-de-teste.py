import time

# importa a API
from DeviceManagerAPI import DeviceManager

# instancia a classe da API passando o nome do cenario e o ip da cloudlet
DM = DeviceManager("cenario-2", "10.0.0.2")

# guarda os dispositivos do cénario em uma variavel
dispositivos = DM.getDevices()

# inicia a app desejada nos dispositivos
for android in dispositivos:
	DM.start_app(android, "br.ufc.great.matrixoperation/.MainActivity")
	time.sleep(5)

# execucao de um exeprimento 30 vezes
cont = 0
while cont < 30:
	print("\n Iniciando o teste numero {}".format(cont))

	# para todos os dispositivos da lista
	for android in dispositivos:
		# executa o metodo da API passando o dispositivo, a activity e os extras
		DM.exec_activity(android, "br.ufc.great.matrixoperation/.MainActivity", "--es 'operation' 'mul' --ei 'size' 500")

	time.sleep(10)

	cont += 1

# coleta resultados
for android in dispositivos:
	android.getResults()
